import psycopg2
import streamlit as st
DB_CONFIG = {
    "dbname": ,
    "user": ,
    "password": ,
    "host": "t",
    "port": "5432"
}
def init_connection():
    return psycopg2.connect(**DB_CONFIG)

def table_exists(table_name):
    conn = init_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = %s
        );
    """, (table_name,))
    
    exists = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    return exists
