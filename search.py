import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database.db_connection import get_connection

def search_graves(query: str, city: str = None, graveyard_id: int = None):
    conn = get_connection()
    sql = """
        SELECT g.*, gr.name as graveyard_name, gr.city,
               gr.latitude as gy_lat, gr.longitude as gy_lng
        FROM graves g
        JOIN graveyards gr ON g.graveyard_id = gr.id
        WHERE (
            g.full_name LIKE ? OR
            g.father_name LIKE ? OR
            g.unique_code LIKE ? OR
            g.family_name LIKE ?
        )
    """
    params = [f"%{query}%"] * 4

    if city and city != "All Cities":
        sql += " AND gr.city = ?"
        params.append(city)
    if graveyard_id:
        sql += " AND g.graveyard_id = ?"
        params.append(graveyard_id)

    sql += " ORDER BY g.full_name ASC"
    results = conn.execute(sql, params).fetchall()

    conn.execute(
        "INSERT INTO search_logs (search_query, results_found) VALUES (?,?)",
        (query, len(results))
    )
    conn.commit()
    conn.close()
    return [dict(r) for r in results]

def get_grave_by_code(code: str):
    conn = get_connection()
    r = conn.execute("""
        SELECT g.*, gr.name as graveyard_name, gr.city,
               gr.latitude as gy_lat, gr.longitude as gy_lng
        FROM graves g JOIN graveyards gr ON g.graveyard_id=gr.id
        WHERE g.unique_code=?
    """, (code,)).fetchone()
    conn.close()
    return dict(r) if r else None

def get_all_graveyards():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM graveyards ORDER BY city, name").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_cities():
    conn = get_connection()
    rows = conn.execute("SELECT DISTINCT city FROM graveyards ORDER BY city").fetchall()
    conn.close()
    return ["All Cities"] + [r["city"] for r in rows]
