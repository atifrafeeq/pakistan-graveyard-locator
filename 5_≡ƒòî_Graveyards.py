import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from modules.auth import verify_login
from modules.graveyard_mgmt import add_graveyard
from modules.search import get_all_graveyards
from modules.map_engine import generate_graveyard_map
from streamlit_folium import st_folium
from utils.animations import inject_page_animations
import pandas as pd

st.set_page_config(page_title="Manage Graveyards", page_icon="🕌", layout="wide")
inject_page_animations("graveyards")

st.markdown("""
<style>
/* Animated graveyard cards */
.gy-card {
  background:#161b24; border:1px solid #1e2535; border-radius:12px;
  padding:18px 20px; margin-bottom:8px;
  transition: transform .25s, border-color .25s, box-shadow .25s;
  animation: fadeSlideUp .5s ease both;
  display:flex; align-items:center; gap:16px;
}
.gy-card:hover {
  transform:translateX(6px); border-color:#4ECCA3;
  box-shadow:0 6px 20px rgba(78,204,163,.12);
}
.gy-icon { font-size:28px; flex-shrink:0; }
.gy-name { font-size:15px; font-weight:600; color:#e8e4dc; margin-bottom:3px; }
.gy-detail { font-size:12px; color:#6b7385; line-height:1.6; }
.gy-badge {
  margin-left:auto; flex-shrink:0;
  background:rgba(78,204,163,.1); border:1px solid rgba(78,204,163,.25);
  border-radius:20px; padding:4px 12px;
  font-size:11px; color:#4ECCA3; font-weight:600;
}

/* Map reveal */
.map-wrap { border-radius:12px; overflow:hidden; animation: curtainReveal .7s ease both; }

/* Form box */
.add-form-box {
  background:#161b24; border:1px solid #1e2535; border-radius:14px;
  padding:28px; animation:fadeSlideUp .5s ease both;
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
             animation: popIn .6s .3s cubic-bezier(.34,1.56,.64,1) both;">🕌</div>
        <div style="font-size:22px; font-weight:700; color:#e8e4dc; text-align:center; margin-bottom:6px;">
          Graveyard Management
        </div>
        <div style="font-size:13px; color:#6b7385; text-align:center; margin-bottom:28px;">
          Admin access required to manage graveyards
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    with st.form("login_gy"):
        u = st.text_input("Username", placeholder="admin")
        p = st.text_input("Password", type="password", placeholder="admin123")
        if st.form_submit_button("🔑  Login", type="primary", use_container_width=True):
            user = verify_login(u, p)
            if user:
                st.session_state.logged_in = True
                st.session_state.admin_user = user
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Default: admin / admin123")
    st.stop()

# ── MAIN ──────────────────────────────────────────────
st.markdown(f"""
<div class="page-hero">
  <div class="hero-badge">Admin Panel · Authenticated</div>
  <div class="hero-title">🕌 Manage Graveyards</div>
  <div class="hero-sub">
    Register new graveyards across Pakistan or browse existing ones on the interactive map.
  </div>
</div>
""", unsafe_allow_html=True)

if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

tab1, tab2 = st.tabs(["📋  All Graveyards", "➕  Add New Graveyard"])

with tab1:
    graveyards = get_all_graveyards()

    # Map
    st.markdown("<div class='section-title'>🗺️ All Graveyards on Map</div>", unsafe_allow_html=True)
    st.markdown("<div class='map-wrap'>", unsafe_allow_html=True)
    m = generate_graveyard_map()
    st_folium(m, width="100%", height=420, returned_objects=[])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='section-title'>🏛️ Registered Graveyards ({len(graveyards)})</div>",
                unsafe_allow_html=True)

    if graveyards:
        for i, g in enumerate(graveyards):
            cap = g.get("total_capacity", 0) or 0
            reg = g.get("registered_count", 0) or 0
            pct = int((reg / cap * 100)) if cap > 0 else 0
            st.markdown(f"""
            <div class="gy-card" style="animation-delay:{i*0.06:.2f}s">
              <div class="gy-icon">🕌</div>
              <div style="flex:1;">
                <div class="gy-name">{g['name']}</div>
                <div class="gy-detail">
                  📍 {g['city']} &nbsp;·&nbsp;
                  🪦 {reg:,} graves &nbsp;·&nbsp;
                  📦 Capacity: {cap:,}
                  {'&nbsp;·&nbsp; 🔴 ' + str(pct) + '% full' if pct > 80 else ''}
                </div>
              </div>
              <div class="gy-badge">{pct}% full</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No graveyards registered yet.")

with tab2:
    st.markdown("<div class='section-title'>➕ Register a New Graveyard</div>", unsafe_allow_html=True)
    st.markdown("<div class='add-form-box'>", unsafe_allow_html=True)

    with st.form("add_gy_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            gy_name  = st.text_input("Graveyard Name *", placeholder="e.g. Miani Sahib Graveyard")
            city     = st.text_input("City *", placeholder="e.g. Lahore")
            address  = st.text_input("Address", placeholder="Full address")
        with c2:
            lat      = st.number_input("Latitude *", value=31.5204, format="%.6f", step=0.0001)
            lng      = st.number_input("Longitude *", value=74.3587, format="%.6f", step=0.0001)
            capacity = st.number_input("Total Capacity (graves)", min_value=0, value=10000, step=1000)

        st.info("💡 Get GPS coordinates from Google Maps — right-click on location → copy coordinates.")
        submitted = st.form_submit_button("🕌  Register Graveyard", type="primary", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        if not gy_name.strip() or not city.strip():
            st.error("❌ Graveyard name and city are required.")
        else:
            add_graveyard(gy_name.strip(), city.strip(), address.strip(), lat, lng, capacity)
            st.markdown(f"""
            <div style="text-align:center;padding:24px;animation:popIn .5s ease both;">
              <div style="font-size:48px;margin-bottom:10px;">✅</div>
              <div style="font-size:18px;font-weight:700;color:#e8e4dc;margin-bottom:6px;">Graveyard Registered!</div>
              <div style="font-size:14px;color:#6b7385;">
                <b style="color:#4ECCA3">{gy_name}</b> in <b style="color:#e8e4dc">{city}</b>
                has been added to the system.
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.rerun()
