import streamlit as st
import psycopg2
from settings import DB_CONFIG

# Функция для получения роли пользователя
def get_user_role(login: str):
    query = """
    SELECT user_role FROM users WHERE login = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (login,))
            result = cur.fetchone()
            if result:
                return result[0]
    return None

# Функция для получения списка спецификаций лодок
def get_shoes_specifications():
    query = """
    SELECT spec_id, colour, weight, size FROM shoes_specifications;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

# Функция для получения списка производителей лодок
def get_shoes_firms():
    query = """
    SELECT firm_id, firm_name FROM shoes_firms;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

# Функция для добавления лодки в базу данных
def add_shoe(spec_id: int, firm_id: int, price: int):
    query = """
    INSERT INTO shoes (spec_id, firm_id, price)
    VALUES (%s, %s, %s);
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (spec_id, firm_id, price))
            conn.commit()

# Функция для получения информации о лодке по shoes_id
def get_shoe_info(shoe_id: int):
    query = """
    SELECT 
        shoes.shoe_id, 
        shoes_specifications.colour, 
        shoes_specifications.weight, 
        shoes_specifications.size,
        shoes_firms.firm_name
    FROM shoes
    JOIN shoes_specifications ON shoes.spec_id = shoes_specifications.spec_id
    JOIN shoes_firms ON shoes.firm_id = shoes_firms.firm_id
    WHERE shoes.shoe_id = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (shoe_id,))
            return cur.fetchone()

# Функция для удаления пары по shoe_id
def delete_shoe(shoe_id: int):
    query = "DELETE FROM shoes WHERE shoe_id = %s;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (shoe_id,))
            conn.commit()

# Основная функция отображения страницы
def show_shoes_page(login: str):
    st.title("Управление кроссовками")

    # Проверяем роль пользователя
    user_role = get_user_role(login)
    if user_role != "admin":
        st.error("У вас недостаточно прав для использования этой страницы.")
        return

    # Страница добавления лодок
    st.header("Добавить пару")
    shoe_specs = get_shoes_specifications()
    shoes_firms = get_shoes_firms()

    if not shoe_specs or not shoes_firms:
        st.error("Не удалось загрузить данные. Проверьте таблицы в базе данных.")
        return

    # Подготавливаем выборы для спецификаций и производителей
    spec_options = {
        f"colour: {spec[1]}, Size: {spec[3]}": spec[0] for spec in shoe_specs
    }
    firm_options = {firm[1]: firm[0] for firm in shoes_firms}

    # Добавление лодки
    selected_firm = st.selectbox("Выберите производителя", list(firm_options.keys()))
    selected_spec = st.selectbox("Выберите характеристики", list(spec_options.keys()))
    
    selected_price = st.text_input("Введите цену", key='price_input')
    add_shoe_btn = st.button("Добавить пару")

    if add_shoe_btn:
        spec_id = spec_options[selected_spec]
        firm_id = firm_options[selected_firm]
        try:
            price = int(selected_price)
            add_shoe(spec_id, firm_id, price)
            st.success("Пара успешно добавлена.")
        except ValueError:
            st.error("Цена должна быть числом.")

    # Страница удаления лодок
    st.header("Удалить пару")
    if "shoe_info" not in st.session_state:
        st.session_state.shoe_info = None

    shoe_id = st.text_input("Введите ID пары", key="shoe_id_input")
    fetch_shoe_btn = st.button("Найти пару", key="fetch_shoe_button")

    if fetch_shoe_btn:
        if not shoe_id.isdigit():
            st.error("ID пары должен быть числом.")
        else:
            shoe_info = get_shoe_info(int(shoe_id))
            if shoe_info:
                st.session_state.shoe_info = shoe_info
                st.success("Пара найдена.")
            else:
                st.error(f"Пара с ID {shoe_id} не найдена.")
                st.session_state.shoe_info = None

    if st.session_state.shoe_info:
        st.write("Информация о паре:")
        st.table({
            "ID пары": [st.session_state.shoe_info[0]],
            "Модель": [st.session_state.shoe_info[1]],
            "Размер в см ": [st.session_state.shoe_info[2]],
            "Размер": [st.session_state.shoe_info[3]],
            "Производитель": [st.session_state.shoe_info[4]],
        })

        if st.button("Удалить пару"):
            delete_shoe(int(st.session_state.shoe_info[0]))
            st.success(f"Пара с ID {st.session_state.shoe_info[0]} успешно удалена.")
            st.session_state.shoe_info = None

# Отображение страницы
show_shoes_page(st.session_state.get('login', None))