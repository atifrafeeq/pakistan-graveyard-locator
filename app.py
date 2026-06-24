import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from database.db_setup import initialize_database
from modules.analytics import get_stats
from utils.animations import (
    inject_page_animations, metric_card_html
)

st.set_page_config(
    page_title="Graveyard Locator",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_page_animations("home")

st.markdown("""
<style>
@keyframes floatMosque {
  0%, 100% { transform: translateY(0px); }
  50%       { transform: translateY(-8px); }
}
.mosque-float {
  font-size: 80px; text-align:center; display:block;
  animation: floatMosque 4s ease-in-out infinite, popIn .7s ease both;
  filter: drop-shadow(0 0 20px rgba(78,204,163,.3));
}
@keyframes liveDot {
  0%, 100% { opacity:1; transform:scale(1); }
  50%       { opacity:.4; transform:scale(.6); }
}
.live-dot {
  display:inline-block; width:8px; height:8px; border-radius:50%;
  background:#4ECCA3; margin-right:6px;
  animation: liveDot 1.2s ease-in-out infinite;
  box-shadow: 0 0 6px #4ECCA3;
}
.footer-bar {
  text-align:center; color:#2d3441; font-size:12px; padding:16px 0;
  border-top:1px solid #1e2535; margin-top:20px;
  animation: fadeSlideUp .5s .8s ease both; opacity:0; animation-fill-mode:forwards;
}
.home-bg {
  position:fixed; inset:0; z-index:0; pointer-events:none;
  background-image:
    linear-gradient(rgba(78,204,163,.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(78,204,163,.03) 1px, transparent 1px);
  background-size: 40px 40px;
}
.pak-dots { letter-spacing:12px; font-size:18px; text-align:center;
            animation:fadeSlideUp .6s .4s ease both; opacity:0;
            animation-fill-mode:forwards; }
</style>
""", unsafe_allow_html=True)

initialize_database()

st.markdown("<div class='home-bg'></div>", unsafe_allow_html=True)

st.markdown("""
<div class="page-hero" style="text-align:center; padding: 3rem 2rem;">
  <span class="mosque-float">🕌</span>
  <div style="margin-top:16px">
    <div class="hero-badge" style="margin:0 auto 16px">
      <span class="live-dot"></span>Digital Grave Registry — Pakistan &amp; USA
    </div>
    <div class="hero-title" style="font-size:clamp(24px,4vw,42px); margin:0 auto 12px">
      Graveyard Locator
    </div>
    <div class="hero-sub" style="margin:0 auto; text-align:center; max-width:520px">
      Helping families locate their loved ones — by name, GPS coordinates, or QR code.<br>
      Covering graveyards across Pakistan and the United States.
    </div>
  </div>
  <div class="pak-dots" style="margin-top:20px; color:#1e2535">✦ ✦ ✦ ✦ ✦ ✦ ✦ ✦</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""<div class="section-title">
  <span class="live-dot"></span>Live Statistics
</div>""", unsafe_allow_html=True)

stats = get_stats()
METRICS = [
    (stats["total_graves"],     "Graves Registered",    "🪦", "#4ECCA3", 1),
    (stats["total_graveyards"], "Graveyards Digitized", "🕌", "#5B8DEF", 2),
    (stats["cities_covered"],   "Cities Covered",       "🌆", "#D4AF37", 3),
    (stats["total_searches"],   "Searches Performed",   "🔍", "#4ECCA3", 4),
    (stats["male_graves"],      "Male Graves",          "👨", "#5B8DEF", 5),
    (stats["female_graves"],    "Female Graves",        "👩", "#D4AF37", 6),
]
cols = st.columns(6)
for col, (val, lbl, icon, color, delay) in zip(cols, METRICS):
    with col:
        st.markdown(metric_card_html(val, lbl, icon, delay, color), unsafe_allow_html=True)

st.markdown("<div class='section-title'>Platform Features</div>", unsafe_allow_html=True)

FEATURES = [
    ("🔍", "Public Search",        "Search any grave by name, father's name, or unique code"),
    ("🗺️", "Live GPS Map",         "View exact grave location pinned on an interactive satellite map"),
    ("📱", "QR Code per Grave",    "Every grave gets a unique scannable QR card for on-site access"),
    ("✏️", "Admin Registration",   "Graveyard admins register new graves with GPS and full details"),
    ("📊", "Analytics Dashboard",  "Charts, trends and stats for researchers and administrators"),
    ("🕌", "Graveyard Management", "Register new graveyards anywhere with map coordinates"),
]
cols = st.columns(3)
for i, (icon, title, desc) in enumerate(FEATURES):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="feature-card anim-pop d{i+1}" style="margin-bottom:12px">
          <div class="feature-icon">{icon}</div>
          <div class="feature-title">{title}</div>
          <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='section-title'>How It Works</div>", unsafe_allow_html=True)
steps = [
    ("01","Search","Enter the deceased's name or father's name in the public search bar"),
    ("02","Locate","View GPS-pinned grave location on the interactive map"),
    ("03","Scan QR","Use the QR code at the grave or enter the code manually for instant lookup"),
    ("04","Admin Add","Authorized admins register new graves and graveyards into the system"),
]
cols = st.columns(4)
for col, (num, title, desc) in zip(cols, steps):
    with col:
        st.markdown(f"""
        <div style="text-align:center; padding:16px; animation:fadeSlideUp .5s ease both;">
          <div style="font-size:32px;font-weight:700;color:#1e2535;margin-bottom:6px;">{num}</div>
          <div style="font-size:14px;font-weight:600;color:#4ECCA3;margin-bottom:6px;">{title}</div>
          <div style="font-size:12px;color:#6b7385;line-height:1.6;">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="footer-bar">
  🕌 Graveyard Locator System &nbsp;·&nbsp; Built with Python &amp; Streamlit &nbsp;·&nbsp;
  Pakistan &amp; USA — Digitizing graveyards, one grave at a time
</div>
""", unsafe_allow_html=True)
