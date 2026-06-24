import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from modules.auth import verify_login
from modules.analytics import get_stats, burials_per_month_chart, graves_per_graveyard_chart, age_distribution_chart, gender_chart
from modules.grave_registration import get_all_graves, delete_grave
from modules.search import get_all_graveyards
from database.db_connection import get_connection
from utils.animations import inject_page_animations, metric_card_html
import pandas as pd

st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")
inject_page_animations("admin")

st.markdown("""
<style>
.admin-header {
  background: linear-gradient(135deg, #111622 0%, #0e1520 100%);
  border:1px solid #1e2535; border-radius:16px;
  padding:28px 28px 20px; margin-bottom:20px;
  position:relative; overflow:hidden;
  animation: fadeSlideDown .6s ease both;
}
.admin-header::before {
  content:''; position:absolute; top:0; left:0; right:0; height:3px;
  background: linear-gradient(90deg, #4ECCA3 0%, #5B8DEF 33%, #D4AF37 66%, #4ECCA3 100%);
  background-size:200% 100%;
  animation: shimmer 2.5s linear infinite;
}
.chart-card {
  background:#161b24; border:1px solid #1e2535; border-radius:12px;
  padding:8px; transition:box-shadow .3s;
  animation: fadeSlideUp .5s ease both;
}
.chart-card:hover { box-shadow:0 8px 28px rgba(78,204,163,.1); }
.welcome-pill {
  display:inline-flex; align-items:center; gap:8px;
  background:rgba(78,204,163,.1); border:1px solid rgba(78,204,163,.25);
  border-radius:30px; padding:6px 18px; font-size:14px; color:#e8e4dc;
  margin-bottom:16px;
  animation: fadeSlideLeft .5s .2s ease both;
}
.welcome-avatar {
  width:28px; height:28px; border-radius:50%;
  background:linear-gradient(135deg,#4ECCA3,#3ab88f);
  display:inline-flex; align-items:center; justify-content:center;
  font-size:14px; color:#0a0d14; font-weight:700;
}
.logout-btn button {
  background:#161b24 !important; color:#EF5B5B !important;
  border:1px solid #2d1515 !important;
}
.logout-btn button:hover { border-color:#EF5B5B !important; }
.delete-btn button {
  background:#1a0a0a !important; color:#EF5B5B !important;
  border:1px solid #3d1515 !important; font-size:12px !important;
  padding:4px 10px !important;
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
        animation: slideInFromGround .7s cubic-bezier(.22,1,.36,1) both;
        position:relative; overflow:hidden;">
        <div style="position:absolute;top:0;left:0;right:0;height:3px;
          background:linear-gradient(90deg,#4ECCA3,#5B8DEF,#D4AF37,#4ECCA3);
          background-size:200% 100%; animation:shimmer 2.5s linear infinite;"></div>
        <div style="font-size:52px; text-align:center; margin-bottom:14px;
             animation: popIn .6s .3s cubic-bezier(.34,1.56,.64,1) both;">📊</div>
        <div style="font-size:22px; font-weight:700; color:#e8e4dc; text-align:center; margin-bottom:6px;">
          Admin Dashboard
        </div>
        <div style="font-size:13px; color:#6b7385; text-align:center; margin-bottom:28px;">
          Enter your credentials to access the control panel
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    with st.form("login_dash"):
        u = st.text_input("Username", placeholder="admin")
        p = st.text_input("Password", type="password", placeholder="admin123")
        if st.form_submit_button("🔑  Enter Dashboard", type="primary", use_container_width=True):
            user = verify_login(u, p)
            if user:
                st.session_state.logged_in = True
                st.session_state.admin_user = user
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Default: admin / admin123")
    st.stop()

# ── DASHBOARD ─────────────────────────────────────────
admin = st.session_state.admin_user
initials = "".join(w[0].upper() for w in admin['full_name'].split()[:2])

st.markdown(f"""
<div class="admin-header">
  <div class="welcome-pill">
    <span class="welcome-avatar">{initials}</span>
    Welcome back, <b style="color:#4ECCA3">{admin['full_name']}</b>
  </div>
  <div style="font-size:28px; font-weight:700; color:#e8e4dc; margin-bottom:4px;">
    📊 Admin Dashboard
  </div>
  <div style="font-size:14px; color:#6b7385;">
    Real-time analytics and data management — Pakistan &amp; USA Graveyard Locator
  </div>
</div>
""", unsafe_allow_html=True)

col_main, col_logout = st.columns([6, 1])
with col_logout:
    st.markdown("<div class='logout-btn'>", unsafe_allow_html=True)
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ── STATS ─────────────────────────────────────────────
st.markdown("<div class='section-title'>📈 Live Statistics</div>", unsafe_allow_html=True)
stats = get_stats()
METRICS = [
    (stats["total_graves"],     "Total Graves",  "🪦", "#4ECCA3", 1),
    (stats["total_graveyards"], "Graveyards",    "🕌", "#5B8DEF", 2),
    (stats["cities_covered"],   "Cities",        "🌆", "#D4AF37", 3),
    (stats["total_searches"],   "Searches",      "🔍", "#4ECCA3", 4),
    (stats["male_graves"],      "Male Graves",   "👨", "#5B8DEF", 5),
    (stats["female_graves"],    "Female Graves", "👩", "#D4AF37", 6),
]
cols = st.columns(6)
for col, (val, lbl, icon, color, delay) in zip(cols, METRICS):
    with col:
        st.markdown(metric_card_html(val, lbl, icon, delay, color), unsafe_allow_html=True)

st.divider()

# ── CHARTS ────────────────────────────────────────────
st.markdown("<div class='section-title'>📊 Analytics</div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.plotly_chart(burials_per_month_chart(), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='chart-card' style='animation-delay:.1s'>", unsafe_allow_html=True)
    st.plotly_chart(graves_per_graveyard_chart(), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

c3, c4 = st.columns(2)
with c3:
    st.markdown("<div class='chart-card' style='animation-delay:.2s'>", unsafe_allow_html=True)
    st.plotly_chart(age_distribution_chart(), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
with c4:
    st.markdown("<div class='chart-card' style='animation-delay:.3s'>", unsafe_allow_html=True)
    st.plotly_chart(gender_chart(), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ── GRAVES TABLE ──────────────────────────────────────
st.markdown("<div class='section-title'>📋 All Registered Graves</div>", unsafe_allow_html=True)
graveyards = get_all_graveyards()
gy_options = ["All Graveyards"] + [f"{g['name']} — {g['city']}" for g in graveyards]

col_filter, col_search = st.columns([2, 2])
with col_filter:
    gy_filter = st.selectbox("Filter by Graveyard", gy_options)
with col_search:
    name_filter = st.text_input("🔍 Search by Name", placeholder="Filter by name...")

selected_gy_id = None
if gy_filter != "All Graveyards":
    for g in graveyards:
        if f"{g['name']} — {g['city']}" == gy_filter:
            selected_gy_id = g["id"]; break

graves = get_all_graves(selected_gy_id)

# Apply name filter
if name_filter.strip():
    nf = name_filter.strip().lower()
    graves = [g for g in graves if nf in g.get("full_name","").lower()
              or nf in g.get("father_name","").lower()]

if graves:
    df = pd.DataFrame(graves)
    cols_show = ["unique_code","full_name","father_name","gender","age_at_death",
                 "date_of_death","date_of_burial","section","row_number","grave_number",
                 "graveyard_name","city"]
    df_show = df[[c for c in cols_show if c in df.columns]]
    df_show.columns = ["Code","Name","Father","Gender","Age","Died","Buried",
                       "Section","Row","Grave#","Graveyard","City"][:len(df_show.columns)]
    st.dataframe(df_show, use_container_width=True, height=400)

    col_dl, col_count = st.columns([2, 1])
    with col_dl:
        csv = df_show.to_csv(index=False).encode()
        st.download_button("⬇️ Export as CSV", csv, "graves_export.csv", "text/csv")
    with col_count:
        st.markdown(f"""
        <div style="text-align:right; padding:8px; color:#6b7385; font-size:13px;">
          Showing <b style="color:#4ECCA3">{len(graves):,}</b> graves
        </div>""", unsafe_allow_html=True)

    # ── DELETE SECTION ─────────────────────────────────
    st.markdown("<div class='section-title' style='margin-top:16px;'>🗑️ Delete a Grave Record</div>",
                unsafe_allow_html=True)
    st.warning("⚠️ Deletion is permanent and cannot be undone.")

    del_col1, del_col2 = st.columns([3, 1])
    with del_col1:
        del_code = st.text_input("Enter Grave Unique Code to Delete",
                                  placeholder="e.g. PKG-003-2024-0042")
    with del_col2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='delete-btn'>", unsafe_allow_html=True)
        if st.button("🗑️ Delete Grave", use_container_width=True):
            if del_code.strip():
                conn = get_connection()
                row = conn.execute(
                    "SELECT id, full_name FROM graves WHERE unique_code=?",
                    (del_code.strip(),)
                ).fetchone()
                conn.close()
                if row:
                    delete_grave(row["id"])
                    st.success(f"✅ Deleted: **{row['full_name']}** (`{del_code.strip()}`)")
                    st.rerun()
                else:
                    st.error(f"❌ Code `{del_code.strip()}` not found.")
            else:
                st.error("❌ Please enter a grave code.")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No graves found.")

st.divider()

# ── RECENT SEARCHES ───────────────────────────────────
st.markdown("<div class='section-title'>🔍 Recent Searches</div>", unsafe_allow_html=True)
conn = get_connection()
searches = conn.execute(
    "SELECT search_query, results_found, searched_at FROM search_logs ORDER BY searched_at DESC LIMIT 20"
).fetchall()
conn.close()
if searches:
    sdf = pd.DataFrame([dict(s) for s in searches])
    sdf.columns = ["Query", "Results Found", "Time"]
    st.dataframe(sdf, use_container_width=True, height=300)
else:
    st.info("No searches yet.")
