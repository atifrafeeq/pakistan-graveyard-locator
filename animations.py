"""
animations.py — Cinematic UI layer for Pakistan Graveyard Locator
Inject once per page via inject_page_animations(page_name)
"""

import streamlit as st

# ═══════════════════════════════════════════════════════
#  SHARED DESIGN TOKENS
# ═══════════════════════════════════════════════════════
_COLORS = {
    "bg":        "#0a0d14",
    "surface":   "#111622",
    "card":      "#161b24",
    "border":    "#1e2535",
    "accent":    "#4ECCA3",
    "accent2":   "#5B8DEF",
    "gold":      "#D4AF37",
    "text":      "#e8e4dc",
    "muted":     "#6b7385",
    "danger":    "#EF5B5B",
}


# ═══════════════════════════════════════════════════════
#  GLOBAL BASE STYLES  (injected on every page)
# ═══════════════════════════════════════════════════════
_BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
  font-family: 'IBM Plex Sans', sans-serif;
  background: #0a0d14;
  color: #e8e4dc;
}
.stApp { background: #0a0d14 !important; }
.main  { background: #0a0d14 !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: #080b11 !important;
  border-right: 1px solid #1e2535;
}
section[data-testid="stSidebar"] * { color: #9ca3af !important; }
section[data-testid="stSidebar"] a:hover { color: #4ECCA3 !important; }

/* ── Inputs ── */
.stTextInput input, .stNumberInput input, .stDateInput input,
.stSelectbox > div > div, .stTextArea textarea {
  background: #161b24 !important;
  color: #e8e4dc !important;
  border-color: #1e2535 !important;
  border-radius: 8px !important;
  transition: border-color .25s, box-shadow .25s;
}
.stTextInput input:focus, .stNumberInput input:focus,
.stTextArea textarea:focus {
  border-color: #4ECCA3 !important;
  box-shadow: 0 0 0 2px rgba(78,204,163,.15) !important;
}
label, .stSelectbox label { color: #9ca3af !important; font-size: 13px !important; }

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, #4ECCA3 0%, #3ab88f 100%) !important;
  color: #0a0d14 !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  letter-spacing: .3px !important;
  transition: transform .2s, box-shadow .2s, filter .2s !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(78,204,163,.35) !important;
  filter: brightness(1.1) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Download button ── */
.stDownloadButton > button {
  background: #161b24 !important;
  color: #4ECCA3 !important;
  border: 1px solid #1e2535 !important;
  border-radius: 8px !important;
  font-weight: 500 !important;
  transition: all .2s !important;
}
.stDownloadButton > button:hover {
  border-color: #4ECCA3 !important;
  box-shadow: 0 0 10px rgba(78,204,163,.2) !important;
}

/* ── Divider ── */
hr { border-color: #1e2535 !important; }

/* ── Data table ── */
.stDataFrame { background: #161b24 !important; border-radius: 10px !important; overflow: hidden !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
  background: #161b24 !important;
  border: 1px solid #1e2535 !important;
  border-radius: 8px !important;
  color: #e8e4dc !important;
  transition: background .2s;
}
.streamlit-expanderHeader:hover { background: #1a2130 !important; }

/* ── Alerts ── */
.stSuccess { background: rgba(78,204,163,.1) !important; border-left: 3px solid #4ECCA3 !important; }
.stError   { background: rgba(239,91,91,.1)  !important; border-left: 3px solid #EF5B5B !important; }
.stWarning { background: rgba(212,175,55,.1)  !important; border-left: 3px solid #D4AF37 !important; }
.stInfo    { background: rgba(91,141,239,.1)  !important; border-left: 3px solid #5B8DEF !important; }

/* ── Tabs ── */
button[data-baseweb="tab"] {
  background: transparent !important;
  color: #6b7385 !important;
  border-bottom: 2px solid transparent !important;
  font-weight: 500 !important;
  transition: all .2s !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
  color: #4ECCA3 !important;
  border-bottom-color: #4ECCA3 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0d14; }
::-webkit-scrollbar-thumb { background: #1e2535; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #4ECCA3; }

/* ══════════════════════════════════════
   KEYFRAMES
══════════════════════════════════════ */
@keyframes fadeSlideDown {
  from { opacity:0; transform:translateY(-28px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeSlideUp {
  from { opacity:0; transform:translateY(28px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeSlideLeft {
  from { opacity:0; transform:translateX(40px); }
  to   { opacity:1; transform:translateX(0); }
}
@keyframes fadeSlideRight {
  from { opacity:0; transform:translateX(-40px); }
  to   { opacity:1; transform:translateX(0); }
}
@keyframes popIn {
  0%   { opacity:0; transform:scale(.6) translateY(20px); }
  70%  { transform:scale(1.04) translateY(-3px); }
  100% { opacity:1; transform:scale(1) translateY(0); }
}
@keyframes curtainReveal {
  from { clip-path: inset(0 0 100% 0); opacity:0; }
  to   { clip-path: inset(0 0 0% 0);   opacity:1; }
}
@keyframes glowPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(78,204,163,0); }
  50%       { box-shadow: 0 0 24px 4px rgba(78,204,163,.25); }
}
@keyframes countUp {
  from { opacity:0; transform:translateY(12px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes shimmer {
  0%   { background-position: -1000px 0; }
  100% { background-position:  1000px 0; }
}
@keyframes orbit {
  from { transform: rotate(0deg) translateX(18px) rotate(0deg); }
  to   { transform: rotate(360deg) translateX(18px) rotate(-360deg); }
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
@keyframes blink {
  0%, 100% { opacity:1; } 50% { opacity:0; }
}
@keyframes graveDig {
  0%   { transform: translateY(60px) rotate(-8deg); opacity:0; }
  40%  { transform: translateY(-8px) rotate(2deg);  opacity:1; }
  70%  { transform: translateY(4px)  rotate(-1deg); }
  100% { transform: translateY(0)    rotate(0deg);  opacity:1; }
}
@keyframes slideInFromGround {
  0%   { transform: translateY(100px); opacity:0; }
  60%  { transform: translateY(-10px); opacity:1; }
  100% { transform: translateY(0);     opacity:1; }
}
@keyframes typewriter {
  from { width:0; }
  to   { width:100%; }
}
@keyframes borderDraw {
  from { clip-path: inset(0 100% 0 0); }
  to   { clip-path: inset(0 0 0 0); }
}
@keyframes starFall {
  0%   { transform: translateY(-10px) scale(0); opacity:0; }
  50%  { opacity:1; }
  100% { transform: translateY(300px) scale(1); opacity:0; }
}

/* ══════════════════════════════════════
   UTILITY ANIMATION CLASSES
══════════════════════════════════════ */
.anim-fade-down  { animation: fadeSlideDown  .6s cubic-bezier(.22,1,.36,1) both; }
.anim-fade-up    { animation: fadeSlideUp    .6s cubic-bezier(.22,1,.36,1) both; }
.anim-fade-left  { animation: fadeSlideLeft  .6s cubic-bezier(.22,1,.36,1) both; }
.anim-fade-right { animation: fadeSlideRight .6s cubic-bezier(.22,1,.36,1) both; }
.anim-pop        { animation: popIn          .55s cubic-bezier(.34,1.56,.64,1) both; }
.anim-curtain    { animation: curtainReveal  .7s ease both; }
.anim-glow       { animation: glowPulse      2s ease-in-out infinite; }
.anim-dig        { animation: graveDig       .8s cubic-bezier(.22,1,.36,1) both; }
.anim-ground     { animation: slideInFromGround .7s cubic-bezier(.22,1,.36,1) both; }

/* Delay helpers */
.d1 { animation-delay:.1s; } .d2 { animation-delay:.2s; }
.d3 { animation-delay:.3s; } .d4 { animation-delay:.4s; }
.d5 { animation-delay:.5s; } .d6 { animation-delay:.6s; }
.d7 { animation-delay:.7s; } .d8 { animation-delay:.8s; }

/* ══════════════════════════════════════
   COMPONENT STYLES
══════════════════════════════════════ */
.page-hero {
  position: relative; overflow: hidden;
  background: linear-gradient(135deg, #111622 0%, #0e1520 60%, #0a0d14 100%);
  border: 1px solid #1e2535; border-radius: 16px;
  padding: 2.5rem 2rem; margin-bottom: 1.5rem;
}
.page-hero::before {
  content:''; position:absolute; top:-60px; right:-60px;
  width:220px; height:220px; border-radius:50%;
  background: radial-gradient(circle, rgba(78,204,163,.12) 0%, transparent 70%);
  pointer-events:none;
}
.page-hero::after {
  content:''; position:absolute; bottom:-40px; left:10%;
  width:300px; height:2px;
  background: linear-gradient(90deg, transparent, #4ECCA3, transparent);
  opacity:.4;
}
.hero-badge {
  display:inline-flex; align-items:center; gap:6px;
  background: rgba(78,204,163,.12); border:1px solid rgba(78,204,163,.3);
  border-radius:20px; padding:4px 14px; font-size:12px;
  color:#4ECCA3; font-weight:500; margin-bottom:14px;
  animation: fadeSlideDown .5s ease both;
}
.hero-title {
  font-size:clamp(22px,3.5vw,36px); font-weight:700;
  color:#e8e4dc; line-height:1.25; margin-bottom:10px;
  animation: fadeSlideDown .6s .1s ease both;
}
.hero-sub {
  font-size:15px; color:#6b7385; line-height:1.75; max-width:600px;
  animation: fadeSlideDown .6s .2s ease both;
}

.metric-card {
  background: #161b24; border: 1px solid #1e2535;
  border-radius: 12px; padding: 20px 16px; text-align: center;
  transition: transform .25s, border-color .25s, box-shadow .25s;
  position: relative; overflow: hidden;
}
.metric-card::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background: linear-gradient(90deg, transparent, #4ECCA3, transparent);
  opacity:0; transition: opacity .3s;
}
.metric-card:hover { transform:translateY(-4px); border-color:#4ECCA3; box-shadow:0 8px 28px rgba(78,204,163,.15); }
.metric-card:hover::before { opacity:1; }
.metric-val { font-size:34px; font-weight:700; color:#4ECCA3; font-variant-numeric:tabular-nums; }
.metric-lbl { font-size:12px; color:#6b7385; margin-top:5px; letter-spacing:.5px; text-transform:uppercase; }

.feature-card {
  background: #161b24; border:1px solid #1e2535; border-radius:12px;
  padding:20px; height:100%; transition:all .3s;
  position:relative; overflow:hidden;
}
.feature-card::after {
  content:''; position:absolute; bottom:0; left:0; right:0; height:1px;
  background: linear-gradient(90deg, transparent, #4ECCA3, transparent);
  transform: scaleX(0); transition: transform .3s;
}
.feature-card:hover { border-color:#4ECCA3; transform:translateY(-3px); box-shadow:0 12px 30px rgba(78,204,163,.12); }
.feature-card:hover::after { transform: scaleX(1); }
.feature-icon { font-size:30px; margin-bottom:10px; }
.feature-title { font-size:14px; font-weight:600; color:#e8e4dc; margin-bottom:6px; }
.feature-desc  { font-size:12px; color:#6b7385; line-height:1.6; }

.result-card {
  background:#161b24; border:1px solid #1e2535; border-radius:12px;
  padding:18px; margin-bottom:10px;
  transition: border-color .25s, box-shadow .25s, transform .25s;
}
.result-card:hover {
  border-color:#4ECCA3; box-shadow:0 6px 20px rgba(78,204,163,.12);
  transform:translateX(4px);
}
.rname   { font-size:16px; font-weight:600; color:#e8e4dc; margin-bottom:5px; }
.rdetail { font-size:13px; color:#6b7385; line-height:1.75; }
.rcode   { font-family:'IBM Plex Mono',monospace; font-size:11px;
           background:#0a0d14; color:#4ECCA3;
           padding:3px 9px; border-radius:5px; display:inline-block; margin-top:7px; }

.section-title {
  font-size:16px; font-weight:600; color:#e8e4dc;
  border-left:3px solid #4ECCA3; padding-left:12px;
  margin:28px 0 16px; letter-spacing:.2px;
  animation: fadeSlideRight .5s ease both;
}

/* Loading skeleton shimmer */
.skeleton {
  background: linear-gradient(90deg, #161b24 25%, #1e2535 50%, #161b24 75%);
  background-size: 1000px 100%;
  animation: shimmer 1.6s infinite;
  border-radius: 8px;
}

/* Particle dot */
.particle {
  position: absolute; width:4px; height:4px;
  background:#4ECCA3; border-radius:50%; pointer-events:none;
  animation: starFall linear infinite;
  opacity: 0;
}

/* Typing cursor */
.cursor {
  display:inline-block; width:2px; height:1em;
  background:#4ECCA3; margin-left:2px; vertical-align:middle;
  animation: blink .9s step-end infinite;
}

/* Login box */
.login-box {
  max-width:420px; margin:40px auto;
  background:#161b24; border:1px solid #1e2535;
  border-radius:16px; padding:40px 36px;
  box-shadow: 0 20px 60px rgba(0,0,0,.5);
  animation: slideInFromGround .7s cubic-bezier(.22,1,.36,1) both;
}
.login-icon {
  font-size:48px; text-align:center; margin-bottom:16px;
  animation: popIn .6s .3s cubic-bezier(.34,1.56,.64,1) both;
}
.login-title { font-size:22px; font-weight:700; color:#e8e4dc; text-align:center; margin-bottom:6px; }
.login-sub   { font-size:13px; color:#6b7385; text-align:center; margin-bottom:28px; }

/* QR pulse ring */
.qr-ring {
  display:inline-block; padding:20px;
  border:2px solid rgba(78,204,163,.5); border-radius:16px;
  animation: glowPulse 2s ease-in-out infinite;
}

/* Status badge */
.badge {
  display:inline-block; padding:3px 10px; border-radius:20px;
  font-size:11px; font-weight:600; letter-spacing:.4px;
}
.badge-green { background:rgba(78,204,163,.15); color:#4ECCA3; border:1px solid rgba(78,204,163,.3); }
.badge-blue  { background:rgba(91,141,239,.15);  color:#5B8DEF;  border:1px solid rgba(91,141,239,.3); }
.badge-gold  { background:rgba(212,175,55,.15);  color:#D4AF37;  border:1px solid rgba(212,175,55,.3); }

/* Grave dig man animation */
.dig-scene {
  position:relative; text-align:center; padding:20px 0;
  overflow:hidden; height:90px;
}
.dig-ground {
  position:absolute; bottom:0; left:0; right:0; height:3px;
  background: linear-gradient(90deg, transparent, #4ECCA3, transparent);
}
.dig-man {
  font-size:36px; display:inline-block;
  animation: graveDig .9s cubic-bezier(.22,1,.36,1) .2s both;
}
.dig-particles {
  position:absolute; bottom:3px; left:50%; transform:translateX(-50%);
  font-size:12px; animation: fadeSlideUp .5s .8s ease both; opacity:0;
  animation-fill-mode:forwards;
}
</style>
"""


# ═══════════════════════════════════════════════════════
#  PAGE-SPECIFIC CSS EXTENSIONS
# ═══════════════════════════════════════════════════════
_HOME_CSS = """
<style>
/* Floating particles in hero */
.hero-particles { position:relative; }
.hero-dot {
  position:absolute; width:3px; height:3px; border-radius:50%;
  background:#4ECCA3; opacity:.4; animation: starFall 4s ease-in infinite;
}
/* Animated counter */
.stat-counter { font-variant-numeric: tabular-nums; }

/* Mosque silhouette line */
.mosque-line {
  text-align:center; font-size:24px; letter-spacing:8px;
  color:#1e2535; margin:8px 0;
  animation: fadeSlideUp .8s .5s ease both; opacity:0;
  animation-fill-mode: forwards;
}
</style>
"""

_ADMIN_CSS = """
<style>
/* Admin panel glow header */
.admin-header {
  background: linear-gradient(135deg, #161b24, #111622);
  border:1px solid #1e2535; border-radius:14px;
  padding:24px 28px; margin-bottom:20px;
  position:relative; overflow:hidden;
}
.admin-header::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background: linear-gradient(90deg, #4ECCA3, #5B8DEF, #D4AF37, #4ECCA3);
  background-size:200% 100%;
  animation: shimmer 2s linear infinite;
}

/* Chart cards */
.chart-wrap {
  background:#161b24; border:1px solid #1e2535; border-radius:12px;
  padding:8px; transition: box-shadow .3s;
}
.chart-wrap:hover { box-shadow: 0 8px 28px rgba(78,204,163,.1); }

/* User welcome badge */
.welcome-pill {
  display:inline-flex; align-items:center; gap:8px;
  background:rgba(78,204,163,.1); border:1px solid rgba(78,204,163,.25);
  border-radius:30px; padding:6px 18px; font-size:14px;
  animation: fadeSlideLeft .5s ease both;
}
</style>
"""

_SEARCH_CSS = """
<style>
/* Search bar glow on focus */
.search-wrap {
  background:#161b24; border:1px solid #1e2535; border-radius:14px;
  padding:20px; margin-bottom:16px;
  transition: border-color .3s, box-shadow .3s;
  animation: fadeSlideDown .5s ease both;
}
.search-wrap:focus-within {
  border-color:#4ECCA3;
  box-shadow:0 0 0 3px rgba(78,204,163,.12);
}

/* Result pop animation */
.result-item { animation: popIn .45s cubic-bezier(.34,1.56,.64,1) both; }
.result-item:nth-child(2) { animation-delay:.08s; }
.result-item:nth-child(3) { animation-delay:.16s; }
.result-item:nth-child(4) { animation-delay:.24s; }
</style>
"""

_QR_CSS = """
<style>
/* QR scanner animate in */
.qr-panel {
  background:#161b24; border:1px solid #1e2535; border-radius:14px;
  padding:28px; text-align:center;
  animation: popIn .6s cubic-bezier(.34,1.56,.64,1) both;
}
/* Scanning line effect */
.scan-line-wrap {
  position:relative; display:inline-block;
  border:2px solid #4ECCA3; border-radius:12px;
  padding:12px; overflow:hidden;
}
.scan-line {
  position:absolute; left:0; right:0; height:2px;
  background:linear-gradient(90deg, transparent, #4ECCA3, transparent);
  animation: scanMove 2s ease-in-out infinite;
}
@keyframes scanMove {
  0%   { top:0%; opacity:1; }
  49%  { opacity:1; }
  50%  { top:100%; opacity:0; }
  51%  { top:0%; opacity:0; }
  52%  { opacity:1; }
  100% { top:100%; opacity:1; }
}
</style>
"""

_GRAVEYARDS_CSS = """
<style>
.gy-card {
  background:#161b24; border:1px solid #1e2535; border-radius:12px;
  padding:18px; margin-bottom:8px;
  transition: transform .25s, border-color .25s, box-shadow .25s;
  animation: fadeSlideUp .5s ease both;
}
.gy-card:hover {
  transform:translateX(6px); border-color:#4ECCA3;
  box-shadow:0 6px 20px rgba(78,204,163,.12);
}
.gy-name   { font-size:15px; font-weight:600; color:#e8e4dc; margin-bottom:4px; }
.gy-detail { font-size:12px; color:#6b7385; }
</style>
"""

_REGISTER_CSS = """
<style>
/* Form section cards */
.form-section {
  background:#161b24; border:1px solid #1e2535; border-radius:12px;
  padding:20px; margin-bottom:16px;
  animation: fadeSlideUp .5s ease both;
}
.form-section-title {
  font-size:13px; font-weight:600; color:#4ECCA3;
  text-transform:uppercase; letter-spacing:.8px;
  margin-bottom:14px; padding-bottom:8px;
  border-bottom:1px solid #1e2535;
}
</style>
"""


# ═══════════════════════════════════════════════════════
#  RUNNING CHARACTER PAGE TRANSITION  (JS + CSS)
# ═══════════════════════════════════════════════════════
_TRANSITION_HTML = """
<style>
/* ── TRANSITION OVERLAY ── */
#gl-transition-overlay {
  position: fixed;
  inset: 0;
  z-index: 99999;
  pointer-events: none;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* The dark curtain that gets pulled in */
#gl-curtain {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #0a0d14 0%, #0e1520 50%, #080b11 100%);
  transform: translateX(-110%);
  will-change: transform;
}

/* Rope the character holds */
#gl-rope {
  position: absolute;
  top: 50%;
  left: 0;
  height: 3px;
  width: 0;
  background: linear-gradient(90deg, transparent, #4ECCA3, #D4AF37, #4ECCA3);
  transform: translateY(-50%);
  transform-origin: left center;
  will-change: width;
  box-shadow: 0 0 8px rgba(78,204,163,.6);
  border-radius: 2px;
}

/* Running character wrapper */
#gl-runner {
  position: absolute;
  top: 50%;
  left: -120px;
  transform: translateY(-60%);
  display: flex;
  flex-direction: column;
  align-items: center;
  will-change: left;
  z-index: 2;
}

#gl-char {
  font-size: 52px;
  line-height: 1;
  display: block;
  filter: drop-shadow(0 0 12px rgba(78,204,163,.5));
}

#gl-label {
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 11px;
  font-weight: 600;
  color: #4ECCA3;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  margin-top: 6px;
  opacity: 0;
  background: rgba(10,13,20,.8);
  padding: 2px 8px;
  border-radius: 10px;
  border: 1px solid rgba(78,204,163,.3);
  white-space: nowrap;
}

/* Dust particles left behind the runner */
.gl-dust {
  position: absolute;
  font-size: 14px;
  opacity: 0;
  animation: glDustFly 0.6s ease-out forwards;
  pointer-events: none;
}

@keyframes glDustFly {
  0%   { opacity: .9; transform: translate(0, 0) scale(1); }
  100% { opacity: 0; transform: translate(var(--dx), var(--dy)) scale(.3); }
}

/* Star sparkles on curtain */
.gl-spark {
  position: absolute;
  font-size: 18px;
  opacity: 0;
  animation: glSparkPop .5s cubic-bezier(.34,1.56,.64,1) forwards;
}

@keyframes glSparkPop {
  0%   { opacity: 0; transform: scale(0) rotate(0deg); }
  60%  { opacity: 1; transform: scale(1.3) rotate(20deg); }
  100% { opacity: .7; transform: scale(1) rotate(15deg); }
}

/* Page content slides in from the right after curtain */
#gl-content-slide {
  position: absolute;
  inset: 0;
  background: transparent;
  transform: translateX(100%);
  will-change: transform;
}

/* Arrival flash effect */
#gl-flash {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 50%, rgba(78,204,163,.18) 0%, transparent 70%);
  opacity: 0;
  pointer-events: none;
}

/* Running leg keyframe on the emoji */
@keyframes glRunBob {
  0%   { transform: translateY(0px)   rotate(-2deg) scale(1); }
  25%  { transform: translateY(-8px)  rotate(3deg)  scale(1.05); }
  50%  { transform: translateY(0px)   rotate(-2deg) scale(1); }
  75%  { transform: translateY(-5px)  rotate(2deg)  scale(1.03); }
  100% { transform: translateY(0px)   rotate(-2deg) scale(1); }
}

@keyframes glPull {
  0%   { transform: rotate(-5deg) scaleX(1); }
  50%  { transform: rotate(5deg) scaleX(0.95); }
  100% { transform: rotate(-5deg) scaleX(1); }
}

/* Exit: runner throws page and runs off */
@keyframes glRunOff {
  0%   { left: var(--runner-stop); }
  100% { left: 110vw; }
}

/* Page settle bounce */
@keyframes glPageSettle {
  0%   { transform: translateX(0) scaleX(1.02); }
  40%  { transform: translateX(-6px) scaleX(1); }
  70%  { transform: translateX(3px); }
  100% { transform: translateX(0) scaleX(1); }
}

/* Curtain exit */
@keyframes glCurtainExit {
  0%   { transform: translateX(0); }
  100% { transform: translateX(110%); }
}

/* Speed lines behind the runner */
#gl-speedlines {
  position: absolute;
  top: 0; bottom: 0;
  pointer-events: none;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 6px;
  opacity: 0;
  transition: opacity .2s;
}

.gl-speedline {
  height: 2px;
  border-radius: 1px;
  background: linear-gradient(90deg, transparent, rgba(78,204,163,.4), transparent);
  animation: glSpeedLine .4s ease-in-out infinite;
}

@keyframes glSpeedLine {
  0%   { transform: scaleX(.3) translateX(-30%); opacity: 0; }
  50%  { opacity: 1; }
  100% { transform: scaleX(1.2) translateX(10%); opacity: 0; }
}
.gl-speedline:nth-child(2) { animation-delay: .08s; width: 60px; }
.gl-speedline:nth-child(3) { animation-delay: .16s; width: 40px; }
.gl-speedline:nth-child(4) { animation-delay: .04s; width: 80px; }
.gl-speedline:nth-child(5) { animation-delay: .12s; width: 50px; }

</style>

<!-- Transition DOM -->
<div id="gl-transition-overlay">
  <div id="gl-curtain"></div>
  <div id="gl-flash"></div>
  <div id="gl-rope"></div>
  <div id="gl-runner">
    <div id="gl-speedlines">
      <div class="gl-speedline" style="width:70px"></div>
      <div class="gl-speedline"></div>
      <div class="gl-speedline"></div>
      <div class="gl-speedline"></div>
      <div class="gl-speedline"></div>
    </div>
    <span id="gl-char">🏃</span>
    <span id="gl-label">Loading page…</span>
  </div>
</div>

<script>
(function() {
  // ── Configuration ──────────────────────────────────────
  var CHARS     = ['🏃', '🧟', '🕵️', '👷', '🧑‍🦯', '🏇'];
  var DUSTS     = ['💨','✨','⭐','🌟','💫','•','·'];
  var SPARKS    = ['✦','✧','★','☽','🌙','⭐'];
  var PAGE_LABELS = {
    'Public_Search': '🔍 Search',
    'Register_Grave': '✏️ Register',
    'Admin_Dashboard': '📊 Dashboard',
    'QR_Scanner': '📱 QR Scanner',
    'Graveyards': '🕌 Graveyards',
    'Navigate': '🗺️ Navigate',
    'app': '🏠 Home',
  };

  // ── DOM refs ──────────────────────────────────────────
  var overlay   = document.getElementById('gl-transition-overlay');
  var curtain   = document.getElementById('gl-curtain');
  var rope      = document.getElementById('gl-rope');
  var runner    = document.getElementById('gl-runner');
  var charEl    = document.getElementById('gl-char');
  var labelEl   = document.getElementById('gl-label');
  var flash     = document.getElementById('gl-flash');
  var speedlines = document.getElementById('gl-speedlines');

  if (!overlay) return;

  // ── Pick page label ──────────────────────────────────
  var pageName = 'Page';
  var pathStr  = window.location.pathname + window.location.href;
  for (var key in PAGE_LABELS) {
    if (pathStr.indexOf(key) !== -1) { pageName = PAGE_LABELS[key]; break; }
  }
  labelEl.textContent = pageName;

  // ── Pick a random runner character ──────────────────
  charEl.textContent = CHARS[Math.floor(Math.random() * CHARS.length)];

  // ── Detect if this is a fresh page navigation ───────
  var navKey = 'gl_last_nav';
  var now    = Date.now();
  var lastNav = parseInt(sessionStorage.getItem(navKey) || '0', 10);
  var isNewNav = (now - lastNav) > 800;   // ignore re-renders < 800ms
  sessionStorage.setItem(navKey, now);

  if (!isNewNav) {
    overlay.style.display = 'none';
    return;
  }

  // ── Helper: easing ───────────────────────────────────
  function easeOutExpo(t) {
    return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
  }
  function easeInExpo(t) {
    return t === 0 ? 0 : Math.pow(2, 10 * t - 10);
  }
  function easeOutBack(t) {
    var c1 = 1.70158, c3 = c1 + 1;
    return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
  }

  // ── Animate helper ───────────────────────────────────
  function animate(duration, onTick, onDone) {
    var start = null;
    function tick(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      onTick(p);
      if (p < 1) requestAnimationFrame(tick);
      else if (onDone) onDone();
    }
    requestAnimationFrame(tick);
  }

  // ── Dust particle spawner ────────────────────────────
  var dustInterval = null;
  function spawnDust(x, y) {
    var d = document.createElement('div');
    d.className = 'gl-dust';
    d.textContent = DUSTS[Math.floor(Math.random() * DUSTS.length)];
    var dx = -(20 + Math.random() * 30);
    var dy = (Math.random() - .5) * 28;
    d.style.setProperty('--dx', dx + 'px');
    d.style.setProperty('--dy', dy + 'px');
    d.style.left = (x - 30 + Math.random() * 20) + 'px';
    d.style.top  = (y + Math.random() * 20 - 10) + 'px';
    d.style.animationDuration = (.4 + Math.random() * .3) + 's';
    overlay.appendChild(d);
    setTimeout(function() { d.parentNode && d.parentNode.removeChild(d); }, 700);
  }

  // ── Spark spawner on curtain ─────────────────────────
  function spawnSparks() {
    for (var i = 0; i < 6; i++) {
      (function(i) {
        setTimeout(function() {
          var s = document.createElement('div');
          s.className = 'gl-spark';
          s.textContent = SPARKS[Math.floor(Math.random() * SPARKS.length)];
          s.style.left  = (10 + Math.random() * 80) + '%';
          s.style.top   = (10 + Math.random() * 80) + '%';
          s.style.animationDelay = (Math.random() * .2) + 's';
          s.style.fontSize = (14 + Math.random() * 12) + 'px';
          s.style.color = ['#4ECCA3','#D4AF37','#5B8DEF','#e8e4dc'][Math.floor(Math.random()*4)];
          curtain.appendChild(s);
        }, i * 80);
      })(i);
    }
  }

  // ── PHASE 1: Runner charges from left, pulling rope ──
  var VW       = window.innerWidth;
  var VH       = window.innerHeight;
  var stopX    = VW * 0.52;   // where runner stops (center-ish)
  var startX   = -120;
  var runnerY  = VH * 0.5;

  // Show overlay
  overlay.style.display = 'flex';
  overlay.style.pointerEvents = 'all';

  // Start leg-bob animation
  charEl.style.animation = 'glRunBob 0.22s ease-in-out infinite';
  speedlines.style.opacity = '1';

  // Phase 1 duration
  var PHASE1 = 620;

  animate(PHASE1, function(p) {
    var ep = easeOutExpo(p);
    var cx = startX + (stopX - startX) * ep;
    runner.style.left  = cx + 'px';
    runner.style.top   = '50%';

    // Rope stretches as runner moves right
    rope.style.width = Math.max(0, cx + 60) + 'px';

    // Curtain follows the rope — pulled from left edge
    var curtainP = easeOutExpo(Math.max(0, p - .15));
    curtain.style.transform = 'translateX(' + (-110 + curtainP * 110) + '%)';

    // Spawn dust particles
    if (p > .05 && Math.random() < .35) {
      spawnDust(cx, runnerY);
    }
  }, function() {
    // Phase 1 done — runner stops, show label, spawn sparks
    speedlines.style.opacity = '0';
    charEl.style.animation = 'glPull .25s ease-in-out infinite';
    labelEl.style.opacity = '1';
    labelEl.style.transition = 'opacity .3s';

    // Curtain now fully covers screen
    curtain.style.transform = 'translateX(0)';
    rope.style.opacity = '0';

    spawnSparks();

    // Flash effect
    flash.style.opacity = '1';
    flash.style.transition = 'opacity .3s';
    setTimeout(function() {
      flash.style.opacity = '0';
    }, 300);

    // Phase 2: runner bounces then sprints off screen to the right
    setTimeout(function() {
      runPhase2();
    }, 420);
  });


  // ── PHASE 2: Content is here, runner kicks it & runs off ──
  function runPhase2() {
    charEl.style.animation = 'glRunBob 0.18s ease-in-out infinite';
    speedlines.style.opacity = '1';
    labelEl.style.opacity = '0';

    var runoffDuration = 480;
    var px0 = stopX;

    animate(runoffDuration, function(p) {
      var ep = easeInExpo(p);
      var cx = px0 + (VW * 1.3 - px0) * ep;
      runner.style.left = cx + 'px';
    }, function() {
      // Phase 3: Curtain pulls back to the right (reveals page)
      runPhase3();
    });
  }


  // ── PHASE 3: Curtain sweeps off to the right ──────────
  function runPhase3() {
    speedlines.style.opacity = '0';
    runner.style.display = 'none';
    rope.style.display   = 'none';

    var PHASE3 = 520;
    animate(PHASE3, function(p) {
      var ep = easeOutBack(p);
      curtain.style.transform = 'translateX(' + (ep * 110) + '%)';
    }, function() {
      // All done — kill overlay
      overlay.style.transition = 'opacity .2s';
      overlay.style.opacity = '0';
      setTimeout(function() {
        overlay.style.display = 'none';
        overlay.style.pointerEvents = 'none';
      }, 220);
    });
  }

})();
</script>
"""

# ═══════════════════════════════════════════════════════
#  DIG SCENE  — appears at top of admin/register pages
# ═══════════════════════════════════════════════════════
def dig_scene_html(icon="🧑‍💼", label="Loading..."):
    return f"""
<div class="dig-scene">
  <div class="dig-man">{icon}</div>
  <div class="dig-ground"></div>
  <div class="dig-particles">✦ ✦ ✦</div>
</div>
"""

# ═══════════════════════════════════════════════════════
#  ANIMATED HERO
# ═══════════════════════════════════════════════════════
def hero_html(badge, title, subtitle, icon="🕌"):
    return f"""
<div class="page-hero">
  <div class="hero-badge">
    <span style="animation: spin 3s linear infinite; display:inline-block">✦</span>
    {badge}
  </div>
  <div class="hero-title">{icon} {title}</div>
  <div class="hero-sub">{subtitle}</div>
</div>
"""

# ═══════════════════════════════════════════════════════
#  ANIMATED METRIC CARD
# ═══════════════════════════════════════════════════════
def metric_card_html(value, label, icon="", delay=0, color="#4ECCA3"):
    return f"""
<div class="metric-card anim-pop d{delay}" style="--accent:{color}">
  <div style="font-size:20px;margin-bottom:4px;">{icon}</div>
  <div class="metric-val stat-counter" style="color:{color};">{value:,}</div>
  <div class="metric-lbl">{label}</div>
</div>
"""

# ═══════════════════════════════════════════════════════
#  RESULT CARD
# ═══════════════════════════════════════════════════════
def result_card_html(name, detail_lines, code, idx=0):
    details = "".join(f"<div>{d}</div>" for d in detail_lines)
    return f"""
<div class="result-card anim-pop d{min(idx+1,8)}">
  <div class="rname">🕌 {name}</div>
  <div class="rdetail">{details}</div>
  <div class="rcode">{code}</div>
</div>
"""

# ═══════════════════════════════════════════════════════
#  LOGIN BOX
# ═══════════════════════════════════════════════════════
def login_box_open_html(icon, title, subtitle):
    return f"""
<div class="login-box">
  <div class="login-icon">{icon}</div>
  <div class="login-title">{title}</div>
  <div class="login-sub">{subtitle}</div>
"""

LOGIN_BOX_CLOSE = "</div>"

# ═══════════════════════════════════════════════════════
#  COUNTER JS  (animates numbers up on load)
# ═══════════════════════════════════════════════════════
_COUNTER_JS = """
<script>
(function(){
  function animateCounter(el, target, duration) {
    var start = 0, startTime = null;
    function step(ts) {
      if (!startTime) startTime = ts;
      var progress = Math.min((ts - startTime) / duration, 1);
      var ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(ease * target).toLocaleString();
      if (progress < 1) requestAnimationFrame(step);
      else el.textContent = target.toLocaleString();
    }
    requestAnimationFrame(step);
  }
  setTimeout(function(){
    document.querySelectorAll('.stat-counter').forEach(function(el){
      var raw = el.textContent.replace(/,/g,'');
      var target = parseInt(raw, 10);
      if (!isNaN(target)) animateCounter(el, target, 1200);
    });
  }, 400);
})();
</script>
"""

# ═══════════════════════════════════════════════════════
#  MAIN INJECT FUNCTION
# ═══════════════════════════════════════════════════════
_PAGE_EXTRA = {
    "home":       _HOME_CSS,
    "admin":      _ADMIN_CSS,
    "search":     _SEARCH_CSS,
    "qr":         _QR_CSS,
    "graveyards": _GRAVEYARDS_CSS,
    "register":   _REGISTER_CSS,
}

def inject_page_animations(page: str = "home"):
    """Call once at the top of each page (after set_page_config)."""
    extra = _PAGE_EXTRA.get(page, "")
    st.markdown(_BASE_CSS + extra, unsafe_allow_html=True)
    st.markdown(_TRANSITION_HTML, unsafe_allow_html=True)
    st.markdown(_COUNTER_JS, unsafe_allow_html=True)
