import psycopg2
import pandas as pd
from app.database.config import get_connection
from calendar import monthrange

def create_research_stats_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS research_stats (
            id SERIAL PRIMARY KEY,
            researcher_id INTEGER NOT NULL,
            search_date DATE NOT NULL,
            search_count INTEGER NOT NULL,
            FOREIGN KEY (researcher_id) REFERENCES users(id) ON DELETE SET NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def get_research_data(pesquisador_id, ano_inicio, mes_inicio, ano_fim, mes_fim):

    create_research_stats_table()

    conn = get_connection()
    cur = conn.cursor()

    _, last_day = monthrange(ano_fim, mes_fim)

    cur.execute("""
        SELECT search_date, search_count
        FROM research_stats
        WHERE researcher_id = %s
        AND search_date BETWEEN %s AND %s
        ORDER BY search_date ASC
    """, (pesquisador_id, f"{ano_inicio}-{mes_inicio:02d}-01", f"{ano_fim}-{mes_fim:02d}-{last_day}"))

    data = cur.fetchall()
    conn.close()

    return pd.DataFrame(data, columns=["search_date", "search_count"])
