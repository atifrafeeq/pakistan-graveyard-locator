import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database.db_connection import get_connection
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def get_stats():
    conn = get_connection()
    stats = {
        "total_graves":     conn.execute("SELECT COUNT(*) FROM graves").fetchone()[0],
        "total_graveyards": conn.execute("SELECT COUNT(*) FROM graveyards").fetchone()[0],
        "cities_covered":   conn.execute("SELECT COUNT(DISTINCT city) FROM graveyards").fetchone()[0],
        "total_searches":   conn.execute("SELECT COUNT(*) FROM search_logs").fetchone()[0],
        "male_graves":      conn.execute("SELECT COUNT(*) FROM graves WHERE gender='Male'").fetchone()[0],
        "female_graves":    conn.execute("SELECT COUNT(*) FROM graves WHERE gender='Female'").fetchone()[0],
    }
    conn.close()
    return stats

def burials_per_month_chart():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT strftime('%Y-%m', date_of_burial) as month, COUNT(*) as burials
        FROM graves GROUP BY month ORDER BY month
    """, conn)
    conn.close()
    if df.empty:
        return go.Figure()
    fig = px.bar(df, x="month", y="burials", title="Burials Registered Per Month",
                 color="burials", color_continuous_scale="Greens",
                 labels={"month":"Month","burials":"Burials"})
    fig.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                      font_color="#e8e4dc", title_font_size=14)
    return fig

def graves_per_graveyard_chart():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT gr.name, COUNT(g.id) as graves
        FROM graveyards gr LEFT JOIN graves g ON g.graveyard_id=gr.id
        GROUP BY gr.id ORDER BY graves DESC
    """, conn)
    conn.close()
    if df.empty:
        return go.Figure()
    fig = px.pie(df, values="graves", names="name",
                 title="Graves by Graveyard", hole=0.4,
                 color_discrete_sequence=px.colors.sequential.Greens_r)
    fig.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                      font_color="#e8e4dc", title_font_size=14)
    return fig

def age_distribution_chart():
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT age_at_death FROM graves WHERE age_at_death > 0", conn
    )
    conn.close()
    if df.empty:
        return go.Figure()
    fig = px.histogram(df, x="age_at_death", nbins=15,
                       title="Age at Death Distribution",
                       labels={"age_at_death":"Age"},
                       color_discrete_sequence=["#4ECCA3"])
    fig.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                      font_color="#e8e4dc", title_font_size=14)
    return fig

def gender_chart():
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT gender, COUNT(*) as count FROM graves GROUP BY gender", conn
    )
    conn.close()
    if df.empty:
        return go.Figure()
    fig = px.bar(df, x="gender", y="count", title="Graves by Gender",
                 color="gender",
                 color_discrete_map={"Male":"#7AB8F5","Female":"#F9A8D4","Unknown":"#9CA3AF"})
    fig.update_layout(plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                      font_color="#e8e4dc", title_font_size=14, showlegend=False)
    return fig
