import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from modules.search import get_grave_by_code
from modules.map_engine import generate_graveyard_map
from streamlit_folium import st_folium
from utils.animations import inject_page_animations
from database.db_connection import get_connection

st.set_page_config(page_title="QR Scanner", page_icon="📱", layout="wide")
inject_page_animations("qr")

st.markdown("""
<style>
@keyframes qrPulse {
  0%,100%{transform:scale(1); filter:drop-shadow(0 0 8px rgba(78,204,163,.3));}
  50%{transform:scale(1.05); filter:drop-shadow(0 0 20px rgba(78,204,163,.6));}
}
.qr-icon { font-size:72px; animation: qrPulse 2.5s ease-in-out infinite; display:block; text-align:center; }
.scanner-frame {
  border:2px solid rgba(78,204,163,.4); border-radius:16px;
  padding:24px; position:relative; overflow:hidden;
  background:#161b24;
  animation: popIn .6s cubic-bezier(.34,1.56,.64,1) both;
}
.scanner-line {
  position:absolute; left:0; right:0; height:2px;
  background:linear-gradient(90deg, transparent, #4ECCA3, transparent);
  animation: scanMove 2.5s ease-in-out infinite;
}
@keyframes scanMove {
  0%{top:0%;opacity:0;} 5%{opacity:1;} 50%{top:100%;opacity:1;}
  51%{top:0%;opacity:0;} 55%{opacity:1;} 100%{top:100%;opacity:1;}
}
.scanner-frame::before, .scanner-frame::after {
  content:''; position:absolute; width:20px; height:20px;
  border-color:#4ECCA3; border-style:solid;
}
.scanner-frame::before { top:8px; left:8px; border-width:2px 0 0 2px; }
.scanner-frame::after  { bottom:8px; right:8px; border-width:0 2px 2px 0; }
.grave-result {
  background:#161b24; border:1px solid #1e2535; border-radius:14px;
  padding:28px; animation: slideInFromGround .6s cubic-bezier(.22,1,.36,1) both;
  position:relative; overflow:hidden;
}
.grave-result::before {
  content:''; position:absolute; top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,#4ECCA3,#5B8DEF);
}
.grave-name { font-size:22px; font-weight:700; color:#e8e4dc; margin-bottom:8px; }
.grave-code { font-family:monospace; font-size:13px; background:#0a0d14; color:#4ECCA3;
              padding:4px 10px; border-radius:6px; display:inline-block; margin-bottom:16px; }
.code-chip {
  background:#161b24; border:1px solid #1e2535; border-radius:8px;
  padding:8px 14px; font-family:monospace; font-size:12px; color:#4ECCA3;
  cursor:pointer; transition:all .2s;
  animation: popIn .4s ease both;
}
.code-chip:hover { border-color:#4ECCA3; box-shadow:0 0 10px rgba(78,204,163,.15); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-hero" style="text-align:center; padding:2.5rem 2rem;">
  <span class="qr-icon">📱</span>
  <div class="hero-badge" style="margin:16px auto 12px;">QR Lookup System</div>
  <div class="hero-title" style="font-size:28px; margin-bottom:8px;">QR Code Scanner</div>
  <div class="hero-sub" style="margin:0 auto; text-align:center; max-width:480px;">
    Scan a grave's QR code or enter the unique grave code manually<br>
    to instantly access the full burial record.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section-title'>🔑 Enter Grave Code</div>", unsafe_allow_html=True)

st.markdown("<div class='scanner-frame'><div class='scanner-line'></div>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    code_input = st.text_input(
        "Grave Code",
        placeholder="e.g.  PKG-003-2024-0001  or  USA-HFW-REAL-001",
        label_visibility="collapsed",
        help="This code is printed on the QR card at the grave"
    )
with col2:
    lookup_btn = st.button("🔎  Lookup", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# URL param support
if "code" in st.query_params:
    code_input = st.query_params["code"]

# ── RESULT ────────────────────────────────────────────
if code_input and (lookup_btn or code_input):
    grave = get_grave_by_code(code_input.strip())
    if not grave:
        st.markdown(f"""
        <div style="text-align:center; padding:40px; animation:popIn .5s ease both;">
          <div style="font-size:48px; margin-bottom:12px;">❌</div>
          <div style="font-size:18px;font-weight:600;color:#e8e4dc;margin-bottom:8px;">Code Not Found</div>
          <div style="font-size:14px;color:#6b7385;">
            No grave record matches <b style="color:#EF5B5B">{code_input}</b>. Please verify the code.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="grave-result">
          <div style="font-size:13px;color:#4ECCA3;font-weight:600;margin-bottom:10px;">✅ Record Found</div>
          <div class="grave-name">🕌 {grave['full_name']}</div>
          <div class="grave-code">{grave['unique_code']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='section-title'>👤 Grave Details</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Personal Info**")
            st.markdown(f"**Name:** {grave['full_name']}")
            st.markdown(f"**Father's Name:** {grave.get('father_name') or 'N/A'}")
            st.markdown(f"**Gender:** {grave.get('gender','N/A')}")
            st.markdown(f"**Age at Death:** {grave.get('age_at_death') or 'N/A'} yrs")
        with c2:
            st.markdown("**Burial Info**")
            st.markdown(f"**Date of Death:** {grave['date_of_death']}")
            st.markdown(f"**Date of Burial:** {grave['date_of_burial']}")
            st.markdown(f"**Graveyard:** {grave['graveyard_name']}")
            st.markdown(f"**City:** {grave['city']}")
        with c3:
            st.markdown("**Location**")
            st.markdown(f"**Section:** {grave.get('section') or 'N/A'}")
            st.markdown(f"**Row:** {grave.get('row_number') or 'N/A'}")
            st.markdown(f"**Grave No:** {grave.get('grave_number') or 'N/A'}")
            st.markdown(f"**GPS:** `{grave['latitude']:.5f}, {grave['longitude']:.5f}`")

        if grave.get("notes"):
            st.info(f"📝 {grave['notes']}")

        if grave.get("family_name"):
            with st.expander("👨‍👩‍👧 Family Contact (Admin Only)"):
                st.markdown(f"**Contact:** {grave['family_name']}")
                st.markdown(f"**Relation:** {grave.get('family_relation','N/A')}")
                if grave.get("family_phone"):
                    st.markdown(f"**Phone:** {grave['family_phone'][:5]}XXXXX (hidden for privacy)")

        st.markdown("<div class='section-title'>📍 Grave Location on Map</div>", unsafe_allow_html=True)
        m = generate_graveyard_map(
            graveyard_id=grave["graveyard_id"],
            highlight_code=grave["unique_code"],
            graves=[grave]
        )
        st_folium(m, width="100%", height=400, returned_objects=[])

        qr_path = grave.get("qr_code_path")
        if qr_path and os.path.exists(qr_path):
            st.image(qr_path, width=160, caption="QR Code for this grave")
else:
    st.markdown("""
    <div class="section-title" style="margin-top:12px;">🧪 Sample Codes to Try</div>
    """, unsafe_allow_html=True)
    st.info("💡 Enter any of these codes above to see a sample grave record:")

    # Pull real codes from DB
    conn = get_connection()
    pak_codes = [r[0] for r in conn.execute(
        "SELECT unique_code FROM graves WHERE graveyard_id NOT IN (6,17) LIMIT 3"
    ).fetchall()]
    usa_codes = [r[0] for r in conn.execute(
        "SELECT unique_code FROM graves WHERE graveyard_id IN (6,17) LIMIT 3"
    ).fetchall()]
    conn.close()

    if pak_codes:
        st.markdown("**🇵🇰 Pakistan codes:**")
        cols = st.columns(len(pak_codes))
        for col, code in zip(cols, pak_codes):
            with col:
                st.markdown(f"<div class='code-chip'>{code}</div>", unsafe_allow_html=True)

    if usa_codes:
        st.markdown("**🇺🇸 USA codes:**")
        cols = st.columns(len(usa_codes))
        for col, code in zip(cols, usa_codes):
            with col:
                st.markdown(f"<div class='code-chip'>{code}</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:28px; display:flex; gap:20px; flex-wrap:wrap; animation:fadeSlideUp .5s .5s ease both; opacity:0; animation-fill-mode:forwards;">
      <div style="flex:1;min-width:160px;background:#161b24;border:1px solid #1e2535;border-radius:10px;padding:16px;text-align:center;">
        <div style="font-size:28px;margin-bottom:8px;">📷</div>
        <div style="font-size:12px;color:#6b7385;line-height:1.6;">
          <b style="color:#e8e4dc">Scan QR</b><br>at the grave site
        </div>
      </div>
      <div style="flex:1;min-width:160px;background:#161b24;border:1px solid #1e2535;border-radius:10px;padding:16px;text-align:center;">
        <div style="font-size:28px;margin-bottom:8px;">⌨️</div>
        <div style="font-size:12px;color:#6b7385;line-height:1.6;">
          <b style="color:#e8e4dc">Type code</b><br>from QR card
        </div>
      </div>
      <div style="flex:1;min-width:160px;background:#161b24;border:1px solid #1e2535;border-radius:10px;padding:16px;text-align:center;">
        <div style="font-size:28px;margin-bottom:8px;">📋</div>
        <div style="font-size:12px;color:#6b7385;line-height:1.6;">
          <b style="color:#e8e4dc">View record</b><br>instantly
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
