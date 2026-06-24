import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database.db_connection import get_connection
import bcrypt

def initialize_database():
    conn = get_connection()
    c = conn.cursor()

    # Create tables if not exist
    c.executescript("""
        CREATE TABLE IF NOT EXISTS graveyards (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            name             TEXT NOT NULL,
            city             TEXT NOT NULL,
            address          TEXT,
            latitude         REAL NOT NULL,
            longitude        REAL NOT NULL,
            total_capacity   INTEGER DEFAULT 0,
            registered_count INTEGER DEFAULT 0,
            created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS graves (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            graveyard_id     INTEGER NOT NULL,
            unique_code      TEXT UNIQUE NOT NULL,
            full_name        TEXT NOT NULL,
            father_name      TEXT,
            date_of_death    TEXT NOT NULL,
            date_of_burial   TEXT NOT NULL,
            age_at_death     INTEGER,
            gender           TEXT DEFAULT 'Male',
            section          TEXT,
            row_number       TEXT,
            grave_number     TEXT,
            latitude         REAL NOT NULL,
            longitude        REAL NOT NULL,
            photo_path       TEXT,
            qr_code_path     TEXT,
            notes            TEXT,
            family_name      TEXT,
            family_phone     TEXT,
            family_relation  TEXT,
            created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (graveyard_id) REFERENCES graveyards(id)
        );

        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name     TEXT,
            role          TEXT DEFAULT 'admin',
            is_active     INTEGER DEFAULT 1,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS search_logs (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            search_query  TEXT,
            results_found INTEGER,
            searched_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Seed default admin only if not exists
    pw_hash = bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode()
    c.execute("""
        INSERT OR IGNORE INTO users (username, password_hash, full_name, role)
        VALUES ('admin', ?, 'Super Admin', 'superadmin')
    """, (pw_hash,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    print("✅ Database initialized.")
