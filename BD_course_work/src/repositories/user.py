import psycopg2
import psycopg2.extras
import streamlit as st
from datetime import date
from settings import DB_CONFIG

def get_user_id_by_name(login: str) -> int:
    query = """
    SELECT user_id FROM users WHERE login = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (login,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                st.error(f"Пользователь '{login}'найден.")
                return None
            

def get_user_role(login: str) -> str:
    query = """
    SELECT user_role FROM users WHERE login = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (login,))
            result = cur.fetchone()
            if result:
                return result[0]  # возвращаем роль пользователя
            else:
                st.error(f"Пользователь с именем '{login}' не найде.")
                return None