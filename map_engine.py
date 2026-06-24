import folium
from folium.plugins import MarkerCluster, MiniMap
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database.db_connection import get_connection

def generate_graveyard_map(graveyard_id: int = None, highlight_code: str = None, graves: list = None):
    conn = get_connection()

    if graveyard_id:
        gy = conn.execute("SELECT * FROM graveyards WHERE id=?", (graveyard_id,)).fetchone()
        center = [gy["latitude"], gy["longitude"]]
        zoom = 17
    else:
        center = [30.3753, 69.3451]
        zoom = 6

    m = folium.Map(location=center, zoom_start=zoom, tiles="OpenStreetMap")
    MiniMap(toggle_display=True).add_to(m)

    if graves:
        cluster = MarkerCluster(name="Graves").add_to(m)
        for g in graves:
            is_highlighted = (highlight_code and g["unique_code"] == highlight_code)
            color = "red" if is_highlighted else "green"
            icon = "star" if is_highlighted else "plus-sign"

            popup_html = f"""
            <div style='font-family:Arial;min-width:200px'>
              <h4 style='margin:0 0 6px;color:#1a1a1a'>{g['full_name']}</h4>
              <b>Father:</b> {g.get('father_name','N/A')}<br>
              <b>Died:</b> {g['date_of_death']}<br>
              <b>Age:</b> {g.get('age_at_death','N/A')} years<br>
              <b>Section:</b> {g.get('section','N/A')} | Row: {g.get('row_number','N/A')}<br>
              <b>Grave No:</b> {g.get('grave_number','N/A')}<br>
              <b>Code:</b> <code>{g['unique_code']}</code><br>
              <b>Graveyard:</b> {g.get('graveyard_name','')}<br>
            </div>
            """
            folium.Marker(
                location=[g["latitude"], g["longitude"]],
                popup=folium.Popup(popup_html, max_width=280),
                tooltip=f"🕌 {g['full_name']}",
                icon=folium.Icon(color=color, icon=icon, prefix="glyphicon")
            ).add_to(cluster)
    else:
        # Show all graveyards as overview
        gyards = conn.execute("SELECT * FROM graveyards").fetchall()
        for gy in gyards:
            popup_html = f"""
            <div style='font-family:Arial'>
              <h4 style='margin:0 0 5px'>{gy['name']}</h4>
              <b>City:</b> {gy['city']}<br>
              <b>Registered Graves:</b> {gy['registered_count']}<br>
              <b>Capacity:</b> {gy['total_capacity']:,}<br>
            </div>
            """
            folium.Marker(
                location=[gy["latitude"], gy["longitude"]],
                popup=folium.Popup(popup_html, max_width=220),
                tooltip=f"🕌 {gy['name']}",
                icon=folium.Icon(color="darkgreen", icon="home", prefix="glyphicon")
            ).add_to(m)

    conn.close()
    return m
