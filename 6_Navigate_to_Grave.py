import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.search import search_graves, get_all_cities, get_grave_by_code
from utils.animations import inject_page_animations

st.set_page_config(page_title="Navigate to Grave", page_icon="🧭", layout="wide")
inject_page_animations("search")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Grotesk:wght@300;400;500;600&display=swap');

:root {
  --nav-green: #4ECCA3;
  --nav-blue: #5B8DEF;
  --nav-gold: #D4AF37;
  --nav-red: #FF6B6B;
  --nav-bg: #0d1117;
  --nav-surface: #161b24;
  --nav-border: #1e2535;
  --nav-text: #e8e4dc;
  --nav-muted: #6b7385;
}

/* ── HERO BADGE ── */
.nav-hero {
  text-align: center;
  padding: 2rem 1rem 1.5rem;
  animation: fadeSlideDown .6s ease both;
}
.nav-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(78,204,163,.1); border: 1px solid rgba(78,204,163,.3);
  border-radius: 999px; padding: 6px 16px;
  font-size: 12px; color: var(--nav-green); font-weight: 600;
  letter-spacing: .06em; text-transform: uppercase; margin-bottom: 14px;
}
.pulse-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--nav-green);
  animation: pulse 1.4s ease-in-out infinite;
  box-shadow: 0 0 8px var(--nav-green);
}
@keyframes pulse {
  0%,100%{transform:scale(1);opacity:1;}
  50%{transform:scale(.5);opacity:.4;}
}

/* ── STEP CARDS ── */
.step-row {
  display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap;
}
.step-card {
  flex: 1; min-width: 140px;
  background: var(--nav-surface); border: 1px solid var(--nav-border);
  border-radius: 14px; padding: 18px 14px; text-align: center;
  transition: border-color .3s, transform .25s;
  animation: fadeSlideUp .5s ease both;
}
.step-card:hover { border-color: var(--nav-green); transform: translateY(-3px); }
.step-num {
  font-size: 28px; font-weight: 800; color: var(--nav-border);
  font-family: 'Syne', sans-serif; line-height: 1;
}
.step-card.active .step-num { color: var(--nav-green); }
.step-label { font-size: 11px; color: var(--nav-muted); margin-top: 4px; }
.step-card.active .step-label { color: var(--nav-text); }

/* ── SEARCH BOX ── */
.nav-search-wrap {
  background: var(--nav-surface); border: 1px solid var(--nav-border);
  border-radius: 16px; padding: 24px 20px; margin-bottom: 16px;
  transition: border-color .3s, box-shadow .3s;
}
.nav-search-wrap:focus-within {
  border-color: var(--nav-green);
  box-shadow: 0 0 0 3px rgba(78,204,163,.1);
}

/* ── RESULT CARD ── */
.grave-result-card {
  background: var(--nav-surface); border: 1px solid var(--nav-border);
  border-radius: 14px; padding: 16px 18px; margin-bottom: 10px;
  cursor: pointer; transition: all .25s;
  animation: popIn .35s cubic-bezier(.34,1.56,.64,1) both;
}
.grave-result-card:hover {
  border-color: var(--nav-green);
  box-shadow: 0 4px 20px rgba(78,204,163,.12);
  transform: translateX(4px);
}
.grave-name { font-size: 16px; font-weight: 600; color: var(--nav-text); margin-bottom: 4px; }
.grave-meta { font-size: 12px; color: var(--nav-muted); }
.grave-code { font-size: 11px; color: var(--nav-green); font-family: monospace; }
.grave-distance {
  background: rgba(78,204,163,.1); border: 1px solid rgba(78,204,163,.2);
  border-radius: 8px; padding: 4px 10px; font-size: 12px; color: var(--nav-green);
  font-weight: 600; display: inline-block; margin-top: 6px;
}

/* ── NAV PANEL ── */
.nav-panel {
  background: var(--nav-surface); border: 1px solid var(--nav-border);
  border-radius: 18px; padding: 20px;
  animation: curtainReveal .6s ease both;
}
.nav-destination {
  border-left: 3px solid var(--nav-green);
  padding: 12px 16px; margin-bottom: 14px;
  background: rgba(78,204,163,.04); border-radius: 0 10px 10px 0;
}
.nav-dest-label { font-size: 11px; color: var(--nav-muted); text-transform: uppercase; letter-spacing:.06em; }
.nav-dest-name { font-size: 18px; font-weight: 700; color: var(--nav-text); margin: 2px 0; }
.nav-dest-meta { font-size: 12px; color: var(--nav-muted); }

/* ── ETA BOX ── */
.eta-row {
  display: flex; gap: 10px; margin-bottom: 14px;
}
.eta-box {
  flex: 1; background: rgba(78,204,163,.07); border: 1px solid rgba(78,204,163,.15);
  border-radius: 12px; padding: 14px; text-align: center;
}
.eta-val { font-size: 22px; font-weight: 700; color: var(--nav-green); font-family:'Syne',sans-serif; }
.eta-lbl { font-size: 11px; color: var(--nav-muted); }

/* ── DIRECTION STEPS ── */
.dir-step {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 10px 0; border-bottom: 1px solid var(--nav-border);
}
.dir-icon {
  width: 32px; height: 32px; border-radius: 8px;
  background: rgba(91,141,239,.15); border: 1px solid rgba(91,141,239,.3);
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; flex-shrink: 0;
}
.dir-text { font-size: 13px; color: var(--nav-text); line-height: 1.5; }
.dir-dist { font-size: 11px; color: var(--nav-muted); }

/* ── STATUS BAR ── */
.status-bar {
  display: flex; align-items: center; gap: 10px;
  background: rgba(78,204,163,.06); border: 1px solid rgba(78,204,163,.15);
  border-radius: 10px; padding: 10px 14px; margin-bottom: 14px;
  font-size: 13px; color: var(--nav-text);
}
.status-ok { color: var(--nav-green); font-weight: 600; }
.status-warn { color: var(--nav-gold); font-weight: 600; }
.status-err { color: var(--nav-red); font-weight: 600; }

/* ── SHARE CARD ── */
.share-card {
  background: rgba(91,141,239,.08); border: 1px solid rgba(91,141,239,.2);
  border-radius: 12px; padding: 14px 18px;
}

/* ── COPY BTN ── */
.copy-hint { font-size: 11px; color: var(--nav-muted); text-align: center; margin-top: 6px; }

@keyframes curtainReveal {
  0%{clip-path:inset(0 0 100% 0);opacity:0;}
  100%{clip-path:inset(0 0 0% 0);opacity:1;}
}
</style>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────
st.markdown("""
<div class="nav-hero">
  <div class="nav-badge">
    <div class="pulse-dot"></div>
    Live GPS Navigation
  </div>
  <div class="hero-title" style="font-family:'Syne',sans-serif;">
    🧭 Navigate to Grave
  </div>
  <div class="hero-sub">
    Search for a grave, get your live location, and follow turn-by-turn walking directions —
    just like a ride-hailing app, but for finding loved ones.
  </div>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────
if "nav_selected_grave" not in st.session_state:
    st.session_state.nav_selected_grave = None
if "nav_search_results" not in st.session_state:
    st.session_state.nav_search_results = []
if "nav_query" not in st.session_state:
    st.session_state.nav_query = ""

# ── STEP INDICATORS ───────────────────────────────────────
step1_active = "active" if not st.session_state.nav_selected_grave else ""
step2_active = "active" if st.session_state.nav_selected_grave else ""
st.markdown(f"""
<div class="step-row">
  <div class="step-card {step1_active}" style="animation-delay:.05s">
    <div class="step-num">01</div>
    <div class="step-label">Search &amp; Select Grave</div>
  </div>
  <div class="step-card {step2_active}" style="animation-delay:.12s">
    <div class="step-num">02</div>
    <div class="step-label">Get Live Location</div>
  </div>
  <div class="step-card {step2_active}" style="animation-delay:.18s">
    <div class="step-num">03</div>
    <div class="step-label">Follow Directions</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── STEP 1: SEARCH ────────────────────────────────────────
st.markdown("<div class='section-title'>🔍 Step 1 — Find the Grave</div>", unsafe_allow_html=True)

st.markdown("<div class='nav-search-wrap'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([3, 1.5, 1])
with col1:
    query = st.text_input("🔤 Name, Father's Name, or Grave Code",
                          placeholder="e.g. Muhammad Ali, Ahmed Khan, PKG-001-2024-0001…",
                          value=st.session_state.nav_query,
                          key="nav_search_input")
with col2:
    cities = get_all_cities()
    city_filter = st.selectbox("🌆 City", cities, key="nav_city")
with col3:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    search_clicked = st.button("🔍 Search", use_container_width=True, type="primary", key="nav_search_btn")
st.markdown("</div>", unsafe_allow_html=True)

if search_clicked and query.strip():
    st.session_state.nav_query = query.strip()
    st.session_state.nav_search_results = search_graves(query.strip(), city=city_filter)
    st.session_state.nav_selected_grave = None

results = st.session_state.nav_search_results

if results:
    st.markdown(f"""
    <div style="margin-bottom:12px; font-size:13px; color:var(--nav-muted);">
      Found <b style="color:#4ECCA3">{len(results)}</b> grave(s). Click one to start navigation.
    </div>
    """, unsafe_allow_html=True)

    for i, g in enumerate(results[:8]):
        col_card, col_btn = st.columns([5, 1])
        with col_card:
            st.markdown(f"""
            <div class="grave-result-card" style="animation-delay:{i*0.06}s">
              <div class="grave-name">🪦 {g['full_name']}</div>
              <div class="grave-meta">
                👨 Father: {g.get('father_name','N/A')} &nbsp;·&nbsp;
                🕌 {g.get('graveyard_name','N/A')}, {g.get('city','N/A')} &nbsp;·&nbsp;
                📅 Died: {g.get('date_of_death','N/A')}
              </div>
              <div class="grave-code">🔑 {g['unique_code']}</div>
              {'<div class="grave-distance">📍 Section ' + str(g.get("section","?")) + ' · Row ' + str(g.get("row_number","?")) + ' · Grave ' + str(g.get("grave_number","?")) + '</div>' if g.get("section") else ''}
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
            if st.button("🧭 Navigate", key=f"nav_select_{g['id']}", use_container_width=True):
                st.session_state.nav_selected_grave = g
                st.rerun()

elif st.session_state.nav_query and not results:
    st.markdown("""
    <div style="text-align:center; padding:32px 20px; color:var(--nav-muted);">
      😔 No graves matched your search. Try a different name or spelling.
    </div>
    """, unsafe_allow_html=True)

# ── STEP 2 & 3: NAVIGATION MAP ────────────────────────────
if st.session_state.nav_selected_grave:
    g = st.session_state.nav_selected_grave
    grave_lat = g["latitude"]
    grave_lng = g["longitude"]

    st.markdown("<div class='section-title'>🧭 Step 2 & 3 — Live Navigation</div>", unsafe_allow_html=True)

    col_info, col_reset = st.columns([5, 1])
    with col_info:
        st.markdown(f"""
        <div class="nav-destination">
          <div class="nav-dest-label">🎯 Navigating To</div>
          <div class="nav-dest-name">🪦 {g['full_name']}</div>
          <div class="nav-dest-meta">
            {g.get('graveyard_name','N/A')} · {g.get('city','N/A')} &nbsp;|&nbsp;
            Section: {g.get('section','N/A')} · Row: {g.get('row_number','N/A')} · Grave No: {g.get('grave_number','N/A')}
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_reset:
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("✖ Reset", use_container_width=True):
            st.session_state.nav_selected_grave = None
            st.session_state.nav_search_results = []
            st.session_state.nav_query = ""
            st.rerun()

    # ── THE NAVIGATION MAP (full live GPS + routing) ────────
    nav_map_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
      <link rel="stylesheet" href="https://unpkg.com/leaflet-routing-machine@3.2.12/dist/leaflet-routing-machine.css"/>
      <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
      <script src="https://unpkg.com/leaflet-routing-machine@3.2.12/dist/leaflet-routing-machine.min.js"></script>
      <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ background:#0d1117; font-family:'Segoe UI',sans-serif; overflow:hidden; }}

        #map {{ width:100%; height:420px; border-radius:14px 14px 0 0; }}

        /* ── BOTTOM HUD ── */
        #hud {{
          background:#161b24; border-top:2px solid #1e2535;
          padding:14px 18px; border-radius:0 0 14px 14px;
          display:flex; gap:14px; align-items:stretch; flex-wrap:wrap;
        }}
        .hud-box {{
          flex:1; min-width:100px;
          background:#0d1117; border:1px solid #1e2535; border-radius:12px;
          padding:12px; text-align:center;
        }}
        .hud-val {{ font-size:24px; font-weight:700; color:#4ECCA3; line-height:1; }}
        .hud-lbl {{ font-size:10px; color:#6b7385; margin-top:3px; text-transform:uppercase; letter-spacing:.06em; }}

        /* ── STATUS BAR ── */
        #status-bar {{
          position:absolute; top:14px; left:50%; transform:translateX(-50%);
          background:rgba(13,17,23,.92); border:1px solid #1e2535; border-radius:999px;
          padding:8px 18px; font-size:12px; color:#e8e4dc;
          display:flex; align-items:center; gap:8px; z-index:1000; white-space:nowrap;
          backdrop-filter:blur(8px);
        }}
        #status-dot {{ width:8px; height:8px; border-radius:50%; background:#D4AF37;
                       animation:pulse 1.2s infinite; flex-shrink:0; }}
        @keyframes pulse {{ 0%,100%{{transform:scale(1);opacity:1;}} 50%{{transform:scale(.4);opacity:.3;}} }}

        /* ── LOCATE BTN ── */
        #locate-btn {{
          position:absolute; bottom:170px; right:16px; z-index:1000;
          background:#4ECCA3; color:#0d1117; border:none; border-radius:50%;
          width:48px; height:48px; font-size:22px; cursor:pointer;
          box-shadow:0 4px 16px rgba(78,204,163,.4);
          display:flex; align-items:center; justify-content:center;
          transition:transform .2s, box-shadow .2s;
        }}
        #locate-btn:hover {{ transform:scale(1.1); box-shadow:0 6px 24px rgba(78,204,163,.5); }}
        #locate-btn:active {{ transform:scale(.95); }}

        /* ── NEXT TURN CARD ── */
        #next-turn {{
          position:absolute; top:58px; left:50%; transform:translateX(-50%);
          background:rgba(13,17,23,.95); border:1px solid #4ECCA3; border-radius:14px;
          padding:12px 20px; z-index:1000; display:none;
          min-width:260px; backdrop-filter:blur(10px);
          animation:slideDown .3s ease;
        }}
        @keyframes slideDown {{ from{{opacity:0;transform:translateX(-50%) translateY(-10px);}} to{{opacity:1;transform:translateX(-50%) translateY(0);}} }}
        .turn-arrow {{ font-size:28px; display:inline-block; margin-right:10px; }}
        .turn-text {{ font-size:13px; color:#e8e4dc; display:inline; vertical-align:middle; }}
        .turn-dist {{ font-size:11px; color:#4ECCA3; margin-top:3px; }}

        /* ── ARRIVAL BANNER ── */
        #arrival {{
          position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
          background:rgba(13,17,23,.97); border:2px solid #4ECCA3; border-radius:20px;
          padding:28px 36px; z-index:2000; display:none; text-align:center;
          backdrop-filter:blur(16px); animation:popIn .4s cubic-bezier(.34,1.56,.64,1);
        }}
        @keyframes popIn {{ 0%{{transform:translate(-50%,-50%) scale(.6);opacity:0;}} 100%{{transform:translate(-50%,-50%) scale(1);opacity:1;}} }}
        .arrival-icon {{ font-size:56px; margin-bottom:10px; }}
        .arrival-title {{ font-size:20px; font-weight:700; color:#4ECCA3; margin-bottom:6px; }}
        .arrival-sub {{ font-size:13px; color:#6b7385; }}
        #close-arrival {{ margin-top:16px; background:#4ECCA3; color:#0d1117; border:none;
                          border-radius:8px; padding:8px 24px; font-size:13px; font-weight:600;
                          cursor:pointer; }}

        /* ── GRAVE MARKER PULSE ── */
        .grave-pulse-outer {{
          width:40px; height:40px; border-radius:50%;
          background:rgba(255,107,107,.15); border:2px solid rgba(255,107,107,.5);
          display:flex; align-items:center; justify-content:center;
          animation:graveRing 2s ease-in-out infinite;
        }}
        @keyframes graveRing {{
          0%,100%{{box-shadow:0 0 0 0 rgba(255,107,107,.4);}}
          50%{{box-shadow:0 0 0 12px rgba(255,107,107,0);}}
        }}

        /* ── USER MARKER ── */
        .user-marker-wrap {{
          position:relative; width:36px; height:36px;
        }}
        .user-dot {{
          width:16px; height:16px; border-radius:50%; background:#4ECCA3;
          border:3px solid #fff; position:absolute; top:50%; left:50%;
          transform:translate(-50%,-50%); z-index:2;
          box-shadow:0 2px 8px rgba(78,204,163,.6);
        }}
        .user-ring {{
          width:36px; height:36px; border-radius:50%;
          background:rgba(78,204,163,.15); border:2px solid rgba(78,204,163,.4);
          position:absolute; top:0; left:0;
          animation:userPing 2s ease-in-out infinite;
        }}
        @keyframes userPing {{
          0%,100%{{transform:scale(1);opacity:.8;}}
          50%{{transform:scale(1.4);opacity:.1;}}
        }}
      </style>
    </head>
    <body>
      <div style="position:relative;">
        <div id="map"></div>
        <div id="status-bar">
          <div id="status-dot"></div>
          <span id="status-text">Requesting your location…</span>
        </div>
        <button id="locate-btn" onclick="centerOnUser()" title="My Location">📍</button>
        <div id="next-turn">
          <div>
            <span class="turn-arrow" id="turn-icon">➡️</span>
            <span class="turn-text" id="turn-text">Calculating route…</span>
          </div>
          <div class="turn-dist" id="turn-dist"></div>
        </div>
        <div id="arrival">
          <div class="arrival-icon">🪦</div>
          <div class="arrival-title">You have arrived!</div>
          <div class="arrival-sub">
            You are now at the grave of<br>
            <b style="color:#e8e4dc">{g['full_name']}</b>
          </div>
          <button id="close-arrival" onclick="document.getElementById('arrival').style.display='none'">✓ Done</button>
        </div>
      </div>
      <div id="hud">
        <div class="hud-box">
          <div class="hud-val" id="eta-val">—</div>
          <div class="hud-lbl">⏱ ETA</div>
        </div>
        <div class="hud-box">
          <div class="hud-val" id="dist-val">—</div>
          <div class="hud-lbl">📏 Distance</div>
        </div>
        <div class="hud-box">
          <div class="hud-val" id="speed-val">—</div>
          <div class="hud-lbl">🚶 Speed</div>
        </div>
        <div class="hud-box">
          <div class="hud-val" id="acc-val">—</div>
          <div class="hud-lbl">🎯 Accuracy</div>
        </div>
      </div>

      <script>
        const GRAVE_LAT = {grave_lat};
        const GRAVE_LNG = {grave_lng};
        const GRAVE_NAME = `{g['full_name']}`;

        let map, userMarker, routingControl, userLat, userLng;
        let routeInstructions = [];
        let arrived = false;
        let watchId = null;

        // ── INIT MAP ──────────────────────────────────────────
        map = L.map('map', {{ zoomControl: false }}).setView([GRAVE_LAT, GRAVE_LNG], 17);

        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
          attribution: '© OpenStreetMap',
          maxZoom: 20
        }}).addTo(map);

        L.control.zoom({{ position: 'bottomright' }}).addTo(map);

        // ── GRAVE MARKER ─────────────────────────────────────
        const graveIcon = L.divIcon({{
          html: `<div style="text-align:center;">
                   <div style="font-size:32px;filter:drop-shadow(0 2px 8px rgba(255,107,107,.8));">🪦</div>
                   <div style="background:#FF6B6B;color:#fff;font-size:10px;font-weight:700;
                               padding:2px 8px;border-radius:999px;margin-top:2px;white-space:nowrap;
                               box-shadow:0 2px 8px rgba(255,107,107,.5);">${{GRAVE_NAME}}</div>
                 </div>`,
          className: '',
          iconAnchor: [20, 36],
          iconSize: [40, 52]
        }});

        const graveMarker = L.marker([GRAVE_LAT, GRAVE_LNG], {{ icon: graveIcon }})
          .addTo(map)
          .bindPopup(`<b>🪦 ${{GRAVE_NAME}}</b><br>
            Father: {g.get('father_name','N/A')}<br>
            Section: {g.get('section','N/A')} · Row: {g.get('row_number','N/A')} · Grave: {g.get('grave_number','N/A')}<br>
            Code: <code>{g['unique_code']}</code>`);

        // ── USER LOCATION ICON ────────────────────────────────
        const userIcon = L.divIcon({{
          html: `<div class="user-marker-wrap">
                   <div class="user-ring"></div>
                   <div class="user-dot"></div>
                 </div>`,
          className: '',
          iconAnchor: [18, 18],
          iconSize: [36, 36]
        }});

        // ── STATUS HELPERS ────────────────────────────────────
        function setStatus(text, color='#4ECCA3') {{
          document.getElementById('status-text').textContent = text;
          document.getElementById('status-dot').style.background = color;
        }}

        function fmtDist(m) {{
          return m < 1000 ? Math.round(m) + ' m' : (m/1000).toFixed(1) + ' km';
        }}

        function fmtETA(sec) {{
          if (sec < 60) return sec + 's';
          const m = Math.round(sec / 60);
          if (m < 60) return m + ' min';
          return Math.floor(m/60) + 'h ' + (m%60) + 'm';
        }}

        // ── BUILD ROUTE ───────────────────────────────────────
        function buildRoute(lat, lng) {{
          if (routingControl) {{ map.removeControl(routingControl); routingControl = null; }}

          routingControl = L.Routing.control({{
            waypoints: [
              L.latLng(lat, lng),
              L.latLng(GRAVE_LAT, GRAVE_LNG)
            ],
            routeWhileDragging: false,
            show: false,
            addWaypoints: false,
            fitSelectedRoutes: true,
            lineOptions: {{
              styles: [
                {{ color: '#4ECCA3', weight: 5, opacity: .85 }},
                {{ color: '#fff', weight: 2, opacity: .2, dashArray: '6 10' }}
              ]
            }},
            createMarker: () => null,
            router: L.Routing.osrmv1({{
              serviceUrl: 'https://router.project-osrm.org/route/v1',
              profile: 'foot'
            }})
          }}).addTo(map);

          routingControl.on('routesfound', function(e) {{
            const route = e.routes[0];
            const dist = route.summary.totalDistance;
            const time = route.summary.totalTime;
            routeInstructions = route.instructions || [];

            document.getElementById('dist-val').textContent = fmtDist(dist);
            document.getElementById('eta-val').textContent = fmtETA(time);

            if (routeInstructions.length > 0) {{
              showNextTurn(routeInstructions[0]);
            }}

            setStatus('🧭 Route found — follow the green path', '#4ECCA3');
          }});

          routingControl.on('routingerror', function() {{
            setStatus('⚠️ Routing failed — showing straight line', '#D4AF37');
            // Draw straight line fallback
            L.polyline([[lat, lng],[GRAVE_LAT, GRAVE_LNG]], {{
              color:'#4ECCA3', weight:4, dashArray:'8 12'
            }}).addTo(map);
            const d = map.distance([lat, lng], [GRAVE_LAT, GRAVE_LNG]);
            document.getElementById('dist-val').textContent = fmtDist(d);
            document.getElementById('eta-val').textContent = fmtETA(d / 1.2);
          }});
        }}

        // ── NEXT TURN DISPLAY ─────────────────────────────────
        function showNextTurn(instr) {{
          const card = document.getElementById('next-turn');
          const arrows = {{
            'Straight':     '⬆️', 'SlightLeft': '↖️', 'SlightRight': '↗️',
            'Left':         '⬅️', 'Right':      '➡️', 'SharpLeft':  '↙️',
            'SharpRight':   '↘️', 'UTurn':      '🔄', 'Head':       '⬆️',
            'Roundabout':   '🔄', 'DestinationReached': '🏁'
          }};
          const arrow = arrows[instr.type] || '➡️';
          document.getElementById('turn-icon').textContent = arrow;
          document.getElementById('turn-text').textContent = instr.text || 'Continue';
          document.getElementById('turn-dist').textContent = fmtDist(instr.distance);
          card.style.display = 'block';
        }}

        // ── UPDATE USER POSITION ──────────────────────────────
        function updateUserPosition(pos) {{
          userLat = pos.coords.latitude;
          userLng = pos.coords.longitude;
          const acc = Math.round(pos.coords.accuracy);
          const speed = pos.coords.speed;

          document.getElementById('acc-val').textContent = acc + 'm';
          document.getElementById('speed-val').textContent =
            speed != null ? (speed * 3.6).toFixed(1) + ' km/h' : '0 km/h';

          if (!userMarker) {{
            userMarker = L.marker([userLat, userLng], {{ icon: userIcon }}).addTo(map);
            map.setView([userLat, userLng], 17);
            buildRoute(userLat, userLng);
            setStatus('📍 Location found — building route…', '#D4AF37');
          }} else {{
            userMarker.setLatLng([userLat, userLng]);
          }}

          // Live distance check
          const distToGrave = map.distance([userLat, userLng], [GRAVE_LAT, GRAVE_LNG]);
          document.getElementById('dist-val').textContent = fmtDist(distToGrave);
          document.getElementById('eta-val').textContent = fmtETA(distToGrave / 1.2);

          // Arrival detection (within 10m)
          if (distToGrave < 10 && !arrived) {{
            arrived = true;
            document.getElementById('arrival').style.display = 'block';
            setStatus('✅ Arrived!', '#4ECCA3');
            if (watchId) navigator.geolocation.clearWatch(watchId);
          }}

          // Rebuild route every 30m moved
          if (routingControl && distToGrave > 10) {{
            buildRoute(userLat, userLng);
          }}
        }}

        function onLocationError(err) {{
          const msgs = {{
            1: 'Location permission denied. Enable GPS in browser settings.',
            2: 'GPS signal unavailable. Try outdoors.',
            3: 'Location request timed out. Retrying…'
          }};
          setStatus('⚠️ ' + (msgs[err.code] || 'GPS error'), '#FF6B6B');
        }}

        function centerOnUser() {{
          if (userLat && userLng) {{
            map.flyTo([userLat, userLng], 18, {{ animate:true, duration:1 }});
          }} else {{
            setStatus('⏳ Still finding your location…', '#D4AF37');
          }}
        }}

        // ── START GPS ─────────────────────────────────────────
        if ('geolocation' in navigator) {{
          setStatus('📡 Requesting GPS permission…', '#D4AF37');
          watchId = navigator.geolocation.watchPosition(
            updateUserPosition,
            onLocationError,
            {{ enableHighAccuracy: true, maximumAge: 5000, timeout: 15000 }}
          );
        }} else {{
          setStatus('❌ GPS not available in this browser', '#FF6B6B');
        }}

      </script>
    </body>
    </html>
    """

    st.components.v1.html(nav_map_html, height=530, scrolling=False)

    # ── ETA + SHARE INFO ──────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col_share, col_info2 = st.columns([3, 2])

    with col_share:
        st.markdown("<div class='section-title'>📤 Share Location</div>", unsafe_allow_html=True)
        google_maps_url = f"https://www.google.com/maps/dir/?api=1&destination={grave_lat},{grave_lng}&travelmode=walking"
        waze_url = f"https://waze.com/ul?ll={grave_lat},{grave_lng}&navigate=yes"
        apple_url = f"https://maps.apple.com/?daddr={grave_lat},{grave_lng}&dirflg=w"
        st.markdown(f"""
        <div class="share-card">
          <div style="font-size:12px; color:#6b7385; margin-bottom:10px;">Open in external navigation app:</div>
          <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <a href="{google_maps_url}" target="_blank" style="
              background:rgba(78,204,163,.1); border:1px solid rgba(78,204,163,.2);
              border-radius:8px; padding:8px 14px; color:#4ECCA3; text-decoration:none;
              font-size:13px; font-weight:600; transition:all .2s;">
              🗺️ Google Maps
            </a>
            <a href="{waze_url}" target="_blank" style="
              background:rgba(91,141,239,.1); border:1px solid rgba(91,141,239,.2);
              border-radius:8px; padding:8px 14px; color:#5B8DEF; text-decoration:none;
              font-size:13px; font-weight:600;">
              🚗 Waze
            </a>
            <a href="{apple_url}" target="_blank" style="
              background:rgba(212,175,55,.1); border:1px solid rgba(212,175,55,.2);
              border-radius:8px; padding:8px 14px; color:#D4AF37; text-decoration:none;
              font-size:13px; font-weight:600;">
              🍎 Apple Maps
            </a>
          </div>
          <div class="copy-hint" style="margin-top:10px; text-align:left;">
            GPS Coordinates: <code style="color:#4ECCA3">{grave_lat:.6f}, {grave_lng:.6f}</code>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_info2:
        st.markdown("<div class='section-title'>📋 Grave Details</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="nav-panel" style="padding:16px;">
          <div style="display:flex; flex-direction:column; gap:6px; font-size:13px;">
            <div><span style="color:#6b7385;">🪦 Name:</span> <b style="color:#e8e4dc">{g['full_name']}</b></div>
            <div><span style="color:#6b7385;">👨 Father:</span> {g.get('father_name','N/A')}</div>
            <div><span style="color:#6b7385;">🕌 Graveyard:</span> {g.get('graveyard_name','N/A')}</div>
            <div><span style="color:#6b7385;">🏙️ City:</span> {g.get('city','N/A')}</div>
            <div><span style="color:#6b7385;">📐 Section:</span> {g.get('section','N/A')} · Row {g.get('row_number','N/A')} · Grave {g.get('grave_number','N/A')}</div>
            <div><span style="color:#6b7385;">🔑 Code:</span> <code style="color:#4ECCA3">{g['unique_code']}</code></div>
            <div><span style="color:#6b7385;">📅 Died:</span> {g.get('date_of_death','N/A')}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── WALKING TIPS ───────────────────────────────────────
    st.markdown("<div class='section-title'>🚶 Navigation Tips</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:16px;">
      <div style="flex:1;min-width:180px;background:#161b24;border:1px solid #1e2535;
                  border-radius:12px;padding:14px;font-size:12px;color:#6b7385;line-height:1.7;">
        <b style="color:#4ECCA3">📡 Enable GPS</b><br>
        Allow location access when your browser asks. This powers the live blue dot tracking.
      </div>
      <div style="flex:1;min-width:180px;background:#161b24;border:1px solid #1e2535;
                  border-radius:12px;padding:14px;font-size:12px;color:#6b7385;line-height:1.7;">
        <b style="color:#4ECCA3">🟢 Follow Green Path</b><br>
        The green route line shows the walking path from your location to the grave.
      </div>
      <div style="flex:1;min-width:180px;background:#161b24;border:1px solid #1e2535;
                  border-radius:12px;padding:14px;font-size:12px;color:#6b7385;line-height:1.7;">
        <b style="color:#4ECCA3">📍 Re-center Button</b><br>
        Tap the green 📍 button on the map to jump back to your current position anytime.
      </div>
      <div style="flex:1;min-width:180px;background:#161b24;border:1px solid #1e2535;
                  border-radius:12px;padding:14px;font-size:12px;color:#6b7385;line-height:1.7;">
        <b style="color:#4ECCA3">🔊 Directions Panel</b><br>
        The top card shows your next turn. A banner appears automatically when you arrive.
      </div>
    </div>
    """, unsafe_allow_html=True)

else:
    # ── EMPTY STATE ───────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding:48px 20px; animation:fadeSlideUp .6s .3s ease both;
                opacity:0; animation-fill-mode:forwards;">
      <div style="font-size:64px; margin-bottom:14px; animation:float 3s ease-in-out infinite;">🧭</div>
      <div style="font-size:16px; color:#e8e4dc; font-weight:600; margin-bottom:8px;">Ready to Navigate</div>
      <div style="font-size:13px; color:#6b7385; max-width:380px; margin:0 auto; line-height:1.7;">
        Search for a grave above, then tap <b style="color:#4ECCA3">🧭 Navigate</b> to open the live
        GPS map — just like calling a ride, but for finding loved ones.
      </div>
    </div>
    <style>
    @keyframes float {{ 0%,100%{{transform:translateY(0);}} 50%{{transform:translateY(-10px);}} }}
    </style>
    """, unsafe_allow_html=True)
