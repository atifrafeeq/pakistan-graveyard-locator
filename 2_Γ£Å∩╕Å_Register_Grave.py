import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from modules.auth import verify_login
from modules.grave_registration import register_grave
from modules.search import get_all_graveyards
from streamlit_folium import st_folium
from modules.map_engine import generate_graveyard_map
from utils.animations import inject_page_animations
import folium

st.set_page_config(page_title="Register Grave", page_icon="✏️", layout="wide")
inject_page_animations("register")

st.markdown("""
<style>
.form-section {
  background:#161b24; border:1px solid #1e2535; border-radius:12px;
  padding:20px 22px; margin-bottom:16px;
}
.form-section-title {
  font-size:12px; font-weight:700; color:#4ECCA3;
  text-transform:uppercase; letter-spacing:.9px;
  margin-bottom:14px; padding-bottom:10px;
  border-bottom:1px solid #1e2535;
  display:flex; align-items:center; gap:8px;
}
.step-num {
  width:24px; height:24px; border-radius:50%;
  background: linear-gradient(135deg,#4ECCA3,#3ab88f);
  color:#0a0d14; font-size:11px; font-weight:700;
  display:inline-flex; align-items:center; justify-content:center;
  flex-shrink:0;
}
@keyframes successPop {
  0%  {transform:scale(.5); opacity:0;}
  70% {transform:scale(1.1);}
  100%{transform:scale(1); opacity:1;}
}
.success-icon { animation: successPop .5s cubic-bezier(.34,1.56,.64,1) both; font-size:48px; text-align:center; }
.rcode {
  font-family:monospace; background:#0a0d14; color:#4ECCA3;
  padding:6px 14px; border-radius:8px; font-size:14px;
  border:1px solid rgba(78,204,163,.3);
}
</style>
""", unsafe_allow_html=True)

# ── LOGIN GATE ────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("""
    <div style="max-width:420px; margin:60px auto;">
      <div style="
        background:#161b24; border:1px solid #1e2535; border-radius:16px;
        padding:40px 36px; box-shadow:0 20px 60px rgba(0,0,0,.5);
        animation: slideInFromGround .7s cubic-bezier(.22,1,.36,1) both;">
        <div style="font-size:52px; text-align:center; margin-bottom:14px;
             animation: popIn .6s .3s cubic-bezier(.34,1.56,.64,1) both;">🔒</div>
        <div style="font-size:22px; font-weight:700; color:#e8e4dc; text-align:center; margin-bottom:6px;">
          Admin Login Required
        </div>
        <div style="font-size:13px; color:#6b7385; text-align:center; margin-bottom:24px;">
          Only authorized admins can register graves
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        u = st.text_input("Username", placeholder="admin")
        p = st.text_input("Password", type="password", placeholder="admin123")
        submitted = st.form_submit_button("🔑  Login", type="primary", use_container_width=True)
        if submitted:
            user = verify_login(u, p)
            if user:
                st.session_state.logged_in = True
                st.session_state.admin_user = user
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Default: admin / admin123")
    st.stop()

# ── LOGGED IN ─────────────────────────────────────────
st.markdown(f"""
<div class="page-hero">
  <div class="hero-badge">Admin Panel · Authenticated</div>
  <div class="hero-title">✏️ Register New Grave</div>
  <div class="hero-sub">
    Logged in as <b style="color:#4ECCA3">{st.session_state.admin_user['full_name']}</b>
    &nbsp;·&nbsp; Fill in all required fields to register a grave
  </div>
</div>
""", unsafe_allow_html=True)

graveyards = get_all_graveyards()
gy_map = {f"{g['name']} — {g['city']}": g for g in graveyards}

with st.form("register_form", clear_on_submit=True):
    # ── Section 1: Graveyard ─────────────────────────
    st.markdown("""<div class="form-section">
    <div class="form-section-title"><span class="step-num">1</span> Select Graveyard</div>""",
    unsafe_allow_html=True)
    gy_choice = st.selectbox("Graveyard", list(gy_map.keys()))
    selected_gy = gy_map[gy_choice]
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 2: Deceased Info ─────────────────────
    st.markdown("""<div class="form-section">
    <div class="form-section-title"><span class="step-num">2</span> Deceased Information</div>""",
    unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        full_name   = st.text_input("Full Name *", placeholder="Muhammad Ali")
        father_name = st.text_input("Father's Name", placeholder="Abdul Karim")
        gender      = st.selectbox("Gender", ["Male", "Female", "Unknown"])
    with c2:
        age_at_death   = st.number_input("Age at Death", min_value=0, max_value=150, value=0, step=1)
        date_of_death  = st.date_input("Date of Death *")
        date_of_burial = st.date_input("Date of Burial *")
    with c3:
        notes = st.text_area("Notes / Additional Info", height=120,
                              placeholder="e.g. martyred, notable person, etc.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 3: Location ──────────────────────────
    st.markdown("""<div class="form-section">
    <div class="form-section-title"><span class="step-num">3</span> Grave Location</div>""",
    unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        section    = st.text_input("Section", placeholder="e.g. A, B, North")
        row_number = st.text_input("Row Number", placeholder="e.g. 12")
    with c2:
        grave_number = st.text_input("Grave Number", placeholder="e.g. 45")
        latitude     = st.number_input("Latitude *", value=float(selected_gy.get("latitude", 31.5204)),
                                        format="%.6f", step=0.0001)
    with c3:
        longitude = st.number_input("Longitude *", value=float(selected_gy.get("longitude", 74.3587)),
                                     format="%.6f", step=0.0001)
    st.info("💡 Tip: Get GPS from Google Maps — right-click on the exact grave spot → copy coordinates.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Section 4: Family ────────────────────────────
    st.markdown("""<div class="form-section">
    <div class="form-section-title"><span class="step-num">4</span> Family Contact (Optional)</div>""",
    unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        family_name     = st.text_input("Contact Name", placeholder="e.g. Ahmed Ali")
    with c2:
        family_relation = st.text_input("Relation", placeholder="e.g. Son, Daughter")
    with c3:
        family_phone    = st.text_input("Phone (hidden from public)", placeholder="03XX-XXXXXXX")
    st.markdown("</div>", unsafe_allow_html=True)

    submitted = st.form_submit_button("🪦  Register Grave", type="primary", use_container_width=True)

if submitted:
    if not full_name.strip():
        st.error("❌ Full name is required.")
    else:
        result = register_grave(
            graveyard_id=selected_gy["id"],
            full_name=full_name.strip(),
            father_name=father_name.strip(),
            gender=gender,
            age_at_death=age_at_death if age_at_death > 0 else None,
            date_of_death=str(date_of_death),
            date_of_burial=str(date_of_burial),
            latitude=latitude,
            longitude=longitude,
            section=section.strip() or None,
            row_number=row_number.strip() or None,
            grave_number=grave_number.strip() or None,
            notes=notes.strip() or None,
            family_name=family_name.strip() or None,
            family_relation=family_relation.strip() or None,
            family_phone=family_phone.strip() or None,
        )
        if result:
            st.markdown(f"""
            <div style="text-align:center; padding:30px;">
              <div class="success-icon">✅</div>
              <div style="font-size:20px;font-weight:700;color:#e8e4dc;margin:14px 0 8px;">Grave Registered!</div>
              <div style="font-size:14px;color:#6b7385;">
                <b style="color:#4ECCA3">{full_name}</b> has been successfully added to the registry.
              </div>
              <div style="margin-top:12px;">
                Unique Code: <span class="rcode">{result.get('unique_code','')}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Registration failed. Please try again.")

if st.button("🚪 Logout", key="logout"):
    st.session_state.logged_in = False
    st.rerun()
