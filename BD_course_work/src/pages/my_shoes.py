import streamlit as st
import psycopg2
from psycopg2 import sql
from settings import DB_CONFIG


# Функция для получения информации о кроссовках всех пользовательсй (для admin)
def get_all_shoes_buy():
    query = """
    SELECT 
        shoe_buy.shoe_id,
        shoes_firms.firm_name,
        shoes_specifications.colour,
        shoes_specifications.size,
        shoe_buy.deliv_date,
        points.point_name,
        users.login
    FROM shoe_buy
    JOIN shoes ON shoe_buy.shoe_id = shoes.shoe_id
    JOIN shoes_specifications ON shoes.spec_id = shoes_specifications.spec_id
    JOIN shoes_firms ON shoes.firm_id = shoes_firms.firm_id
    JOIN points ON shoe_buy.point_id = points.point_id
    JOIN users ON shoe_buy.user_id = users.user_id
    
    ORDER BY users.login, shoe_buy.shoe_id, shoe_buy.deliv_date DESC;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
    return result


# Функция для получения информации о кроссовках
def get_shoes_buy_by_user(user_id: int):
    query = """
    SELECT 
        shoe_buy.shoe_id,
        shoes_firms.firm_name,
        shoes_specifications.colour,
        shoes_specifications.size,
        shoe_buy.deliv_date,
        points.point_name,
        points.time_work
    FROM shoe_buy
    JOIN shoes ON shoe_buy.shoe_id = shoes.shoe_id
    JOIN shoes_specifications ON shoes.spec_id = shoes_specifications.spec_id
    JOIN shoes_firms ON shoes.firm_id = shoes_firms.firm_id
    JOIN points ON shoe_buy.point_id = points.point_id
    WHERE shoe_buy.user_id = %s
    ORDER BY shoe_buy.deliv_date DESC;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (user_id,))
            result = cur.fetchall()
    return result


# Функция для отображения страницы
def show_my_shoes_page(login: str):
    st.title("Мои пары")

    # Получение данных пользователя: user_id и role
    query_login_info = """
    SELECT user_id, user_role FROM users WHERE login = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query_login_info, (login,))
            login_info = cur.fetchone()
    
    if not login_info:
        st.error("Пользователь не найден.")
        return

    user_id, user_role = login_info  # Распаковываем user_id и роль пользователя

    # Получаем данные о лодках
    if user_role == "admin":
        shoes = get_all_shoes_buy()
        if not shoes:
            st.info("В данный момент нет данных о парах.")
            return
        
        st.subheader("Список кроссовок всех польхователей")
        st.table(
            {
                "ID пары": [shoe[0] for shoe in shoes],
                "Производитель": [shoe[1] for shoe in shoes],
                "Цвет": [shoe[2] for shoe in shoes],
                "Размер": [shoe[3] for shoe in shoes],
                "Дата заказа": [shoe[4] for shoe in shoes],
                "Пункт выдачи": [shoe[5] for shoe in shoes],
                "Пользователь": [shoe[6] for shoe in shoes],
            }
        )
    else:
        shoes = get_shoes_buy_by_user(user_id)
        if not shoes:
            st.info("В данный момент нет данных о ваших кроссовках.")
            return

        st.subheader(f"Список кроссовок для пользователя '{login}'")
        st.table(
            {
                "ID пары": [shoe[0] for shoe in shoes],
                "Производитель": [shoe[1] for shoe in shoes],
                "Цвет": [shoe[2] for shoe in shoes],
                "Размер": [shoe[3] for shoe in shoes],
                "Ожидаемая дата доставки": [shoe[4] for shoe in shoes],
                "Пункт выдачи": [shoe[5] for shoe in shoes],
                "Время работы пункта выдачи": [shoe[6] for shoe in shoes],
            }
        )


# Отображаем страницу
show_my_shoes_page(st.session_state.get('login', None))