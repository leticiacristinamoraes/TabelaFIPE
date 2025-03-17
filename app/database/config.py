import psycopg
import streamlit as st
from dotenv import load_dotenv
import sys
import chardet

load_dotenv()
def get_connection():
   
    conn =psycopg.connect(
        dbname = 'postgres',
        user = 'postgres',
        password = "postgres",
        host = 'localhost',
        port = '5432'
        )  

    return conn
