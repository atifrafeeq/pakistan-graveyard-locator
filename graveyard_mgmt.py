import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database.db_connection import get_connection

def add_graveyard(name, city, address, lat, lng, capacity):
    conn = get_connection()
    conn.execute("""
        INSERT INTO graveyards (name, city, address, latitude, longitude, total_capacity)
        VALUES (?,?,?,?,?,?)
    """, (name, city, address, lat, lng, capacity))
    conn.commit()
    conn.close()

def get_graveyard_by_id(gid):
    conn = get_connection()
    r = conn.execute("SELECT * FROM graveyards WHERE id=?", (gid,)).fetchone()
    conn.close()
    return dict(r) if r else None
