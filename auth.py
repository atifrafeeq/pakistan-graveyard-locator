import bcrypt
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database.db_connection import get_connection

def verify_login(username: str, password: str):
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND is_active=1", (username,)
    ).fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return dict(user)
    return None

def require_login():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("🔒 Please login from the Admin Login page.")
        st.stop()
