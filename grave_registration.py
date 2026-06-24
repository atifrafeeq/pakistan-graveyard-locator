import uuid, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database.db_connection import get_connection
from modules.qr_generator import generate_qr


def register_grave(graveyard_id, full_name, father_name="", gender="Male",
                   age_at_death=None, date_of_death=None, date_of_burial=None,
                   latitude=0.0, longitude=0.0, section=None, row_number=None,
                   grave_number=None, notes=None, family_name=None,
                   family_phone=None, family_relation=None) -> dict:
    """Register a new grave. Accepts keyword args directly (no dict wrapper)."""
    unique_code = _generate_code(graveyard_id)
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO graves (
            graveyard_id, unique_code, full_name, father_name,
            date_of_death, date_of_burial, age_at_death, gender,
            section, row_number, grave_number,
            latitude, longitude, notes,
            family_name, family_phone, family_relation
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        graveyard_id, unique_code,
        full_name, father_name or "",
        date_of_death, date_of_burial,
        age_at_death or 0, gender or "Male",
        section or "", row_number or "",
        grave_number or "",
        latitude, longitude,
        notes or "",
        family_name or "", family_phone or "",
        family_relation or ""
    ))

    grave_id = c.lastrowid
    c.execute(
        "UPDATE graveyards SET registered_count=registered_count+1 WHERE id=?",
        (graveyard_id,)
    )
    conn.commit()
    conn.close()

    # Generate QR
    qr_path = generate_qr(grave_id, unique_code, full_name)

    return {"grave_id": grave_id, "unique_code": unique_code, "qr_path": qr_path}


def _generate_code(graveyard_id: int) -> str:
    """Generate a clean unique code like PKG-003-2024-0042."""
    from datetime import datetime
    conn = get_connection()
    count = conn.execute(
        "SELECT COUNT(*) FROM graves WHERE graveyard_id=?", (graveyard_id,)
    ).fetchone()[0]
    conn.close()
    yr = datetime.now().year
    return f"PKG-{graveyard_id:03d}-{yr}-{count + 1:04d}"


def get_all_graves(graveyard_id: int = None):
    conn = get_connection()
    if graveyard_id:
        rows = conn.execute("""
            SELECT g.*, gr.name as graveyard_name, gr.city
            FROM graves g JOIN graveyards gr ON g.graveyard_id=gr.id
            WHERE g.graveyard_id=? ORDER BY g.full_name
        """, (graveyard_id,)).fetchall()
    else:
        rows = conn.execute("""
            SELECT g.*, gr.name as graveyard_name, gr.city
            FROM graves g JOIN graveyards gr ON g.graveyard_id=gr.id
            ORDER BY g.full_name
        """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_grave(grave_id: int):
    conn = get_connection()
    gy_id = conn.execute("SELECT graveyard_id FROM graves WHERE id=?", (grave_id,)).fetchone()
    conn.execute("DELETE FROM graves WHERE id=?", (grave_id,))
    if gy_id:
        conn.execute(
            "UPDATE graveyards SET registered_count=MAX(0,registered_count-1) WHERE id=?",
            (gy_id[0],)
        )
    conn.commit()
    conn.close()
