import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from modules.search import search_graves, get_all_cities, get_all_graveyards
from modules.map_engine import generate_graveyard_map
from streamlit_folium import st_folium
from utils.animations import inject_page_animations

st.set_page_config(page_title="Search Graves", page_icon="🔍", layout="wide")
inject_page_animations("search")

st.markdown("""
<style>
@keyframes searchBounce {
  0%,100%{transform:scale(1) rotate(0deg);}
  25%{transform:scale(1.15) rotate(-8deg);}
  75%{transform:scale(1.1) rotate(6deg);}
}
.search-icon-anim { display:inline-block; animation: searchBounce 2.5s ease-in-out infinite; }
.search-wrap {
  background:#161b24; border:1px solid #1e2535; border-radius:14px;
  padding:24px 20px; margin-bottom:16px;
  animation: fadeSlideDown .6s ease both;
  transition: border-color .3s, box-shadow .3s;
}
.search-wrap:focus-within {
  border-color:#4ECCA3;
  box-shadow: 0 0 0 3px rgba(78,204,163,.12), 0 8px 30px rgba(0,0,0,.3);
}
.result-item { animation: popIn .45s cubic-bezier(.34,1.56,.64,1) both; }
@keyframes shakeX {
  0%,100%{transform:translateX(0);}
  20%{transform:translateX(-10px);}
  40%{transform:translateX(10px);}
  60%{transform:translateX(-6px);}
  80%{transform:translateX(6px);}
}
.shake { animation: shakeX .5s ease both; }
.map-container { animation: curtainReveal .7s ease both; border-radius:12px; overflow:hidden; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-hero">
  <div class="hero-badge">Public Access · No Login Required</div>
  <div class="hero-title">
    <span class="search-icon-anim">🔍</span> Search for a Grave
  </div>
  <div class="hero-sub">
    Find a loved one by their name, father's name, or unique grave code.<br>
    Records available across all registered graveyards in Pakistan and the USA.
  </div>
</div>
""", unsafe_allow_html=True)

# ── SEARCH FORM ───────────────────────────────────────
st.markdown("<div class='search-wrap'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([3, 1.5, 1.2])
with col1:
    query = st.text_input("🔤 Name, Father's Name, or Grave Code",
                           placeholder="e.g. Muhammad Ali, Ahmed Khan, PKG-003-2024-0001…")
with col2:
    cities = get_all_cities()
    city_filter = st.selectbox("🌆 Filter by City", cities)
with col3:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    search_btn = st.button("🔍  Search", use_container_width=True, type="primary")
st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ── RESULTS ───────────────────────────────────────────
if query and (search_btn or query):
    results = search_graves(query.strip(), city=city_filter)

    if not results:
        st.markdown(f"""
        <div class="shake" style="text-align:center; padding:40px 20px;">
          <div style="font-size:48px; margin-bottom:12px;">😔</div>
          <div style="font-size:18px; color:#e8e4dc; font-weight:600; margin-bottom:8px;">No results found</div>
          <div style="font-size:14px; color:#6b7385;">
            No graves matched <b style="color:#4ECCA3">'{query}'</b>. Try a different name or spelling.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="anim-pop" style="
          background:rgba(78,204,163,.08); border:1px solid rgba(78,204,163,.2);
          border-radius:10px; padding:14px 18px; margin-bottom:16px;
          display:flex; align-items:center; gap:12px;">
          <span style="font-size:24px;">✅</span>
          <span>Found <b style="color:#4ECCA3">{len(results)}</b> grave(s) matching
          <b style="color:#e8e4dc">'{query}'</b></span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='section-title'>🗺️ Results on Map</div>", unsafe_allow_html=True)
        st.markdown("<div class='map-container'>", unsafe_allow_html=True)
        m = generate_graveyard_map(graves=results, highlight_code=None)
        st_folium(m, width="100%", height=400, returned_objects=[])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-title'>📋 All Results ({len(results)})</div>",
                    unsafe_allow_html=True)

        for i, g in enumerate(results):
            with st.expander(
                f"🕌  {g['full_name']}  ·  {g['graveyard_name']}, {g['city']}",
                expanded=(i == 0)
            ):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"**Full Name:** {g['full_name']}")
                    st.markdown(f"**Father's Name:** {g.get('father_name') or 'N/A'}")
                    st.markdown(f"**Age at Death:** {g.get('age_at_death') or 'N/A'} yrs")
                    st.markdown(f"**Gender:** {g.get('gender','N/A')}")
                with c2:
                    st.markdown(f"**Date of Death:** {g['date_of_death']}")
                    st.markdown(f"**Date of Burial:** {g['date_of_burial']}")
                    st.markdown(f"**Graveyard:** {g['graveyard_name']}")
                    st.markdown(f"**City:** {g['city']}")
                with c3:
                    st.markdown(f"**Section:** {g.get('section') or 'N/A'}")
                    st.markdown(f"**Row:** {g.get('row_number') or 'N/A'}")
                    st.markdown(f"**Grave No:** {g.get('grave_number') or 'N/A'}")
                    st.markdown(f"**Unique Code:** `{g['unique_code']}`")
                if g.get('notes'):
                    st.info(f"📝 {g['notes']}")
                btn_col1, btn_col2 = st.columns(2)
                with btn_col2:
                    if st.button(f"🧭 Navigate Here", key=f"nav_{g['id']}", use_container_width=True, type="primary"):
                        st.session_state["nav_selected_grave"] = g
                        st.switch_page("pages/6_Navigate_to_Grave.py")
                with btn_col1:
                    if st.button(f"📍 Show on Map", key=f"map_{g['id']}", use_container_width=True):
                        m2 = generate_graveyard_map(
                            graveyard_id=g["graveyard_id"],
                            highlight_code=g["unique_code"],
                            graves=[g]
                        )
                        st_folium(m2, width="100%", height=350, returned_objects=[])
                qr_path = g.get("qr_code_path")
                if qr_path and os.path.exists(qr_path):
                    st.image(qr_path, width=150, caption=f"QR: {g['unique_code']}")
else:
    st.markdown("""
    <div style="text-align:center; padding:20px 0 10px; animation:fadeSlideDown .5s .2s ease both; opacity:0; animation-fill-mode:forwards;">
      <div style="font-size:13px; color:#6b7385; margin-bottom:16px;">
        🗺️ &nbsp;Graveyards Overview
      </div>
    </div>
    """, unsafe_allow_html=True)
    m = generate_graveyard_map()
    st_folium(m, width="100%", height=450, returned_objects=[])

    st.markdown("""
    <div style="display:flex; gap:12px; margin-top:16px; flex-wrap:wrap; animation:fadeSlideUp .5s .4s ease both; opacity:0; animation-fill-mode:forwards;">
      <div style="flex:1; min-width:160px; background:#161b24; border:1px solid #1e2535; border-radius:10px; padding:14px; text-align:center;">
        <div style="font-size:20px; margin-bottom:6px;">🔤</div>
        <div style="font-size:12px; color:#6b7385;">Search by <b style="color:#e8e4dc">Name</b></div>
      </div>
      <div style="flex:1; min-width:160px; background:#161b24; border:1px solid #1e2535; border-radius:10px; padding:14px; text-align:center;">
        <div style="font-size:20px; margin-bottom:6px;">👨</div>
        <div style="font-size:12px; color:#6b7385;">Search by <b style="color:#e8e4dc">Father's Name</b></div>
      </div>
      <div style="flex:1; min-width:160px; background:#161b24; border:1px solid #1e2535; border-radius:10px; padding:14px; text-align:center;">
        <div style="font-size:20px; margin-bottom:6px;">🔑</div>
        <div style="font-size:12px; color:#6b7385;">Search by <b style="color:#e8e4dc">Grave Code</b></div>
      </div>
      <div style="flex:1; min-width:160px; background:#161b24; border:1px solid #1e2535; border-radius:10px; padding:14px; text-align:center;">
        <div style="font-size:20px; margin-bottom:6px;">🌆</div>
        <div style="font-size:12px; color:#6b7385;">Filter by <b style="color:#e8e4dc">City</b></div>
      </div>
    </div>
    """, unsafe_allow_html=True)
