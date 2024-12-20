import psycopg2
import psycopg2.extras
import streamlit as st
from repositories.shoes import get_shoes
from repositories.shoes import add_buy_shoe
from repositories.user import get_user_role
from datetime import date, timedelta
from settings import DB_CONFIG
from repositories.points import get_all_points
from repositories.points import get_point_id

# Функция отображения страницы продажи лодок
def show_selling_shoes_page(login: str):
    st.title("Покупка кроссовок")

    if  login is None:
        st.error("Вы не авторизовались.")
        return
    
    # Получаем роль пользователя
    user_role = get_user_role(login)
    if not user_role:
        return  # Если роль не найдена, прекращаем выполнение
    
    # Получаем список пар из базы данных
    shoes = get_shoes()
    shoe_options = {f"{shoe['firm_name']} {shoe['colour']}  {shoe['size']}: {shoe['price']} р.  ": shoe['shoe_id'] for shoe in shoes}

    # Логика выборав зависимости от роли пользователя
    if user_role == "admin":
        # Если роль admin, показываем все 
        query_users = "SELECT login FROM users;"
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(query_users)
                users = cur.fetchall()

        hool_names = [user[0] for user in users]
    else:
        # Если роль не admin, показываем только школу пользователя
        hool_names = [login]
    
    # Поля для ввода данных
    selected_shoe_name = st.selectbox("Выберите пару", list(shoe_options.keys()))
    login = st.selectbox("Выберите пользователя", hool_names)
    deliv_date = st.date_input("Выберите дату доставки", min_value=(date.today() + timedelta(days=5)))
    point_name = st.selectbox("Выберите пункт выдачи ", get_all_points())
    point_id = get_point_id(point_name)
    #cart =  st.text_input("Номер карты")

    # Кнопки
    add_deal_btn = st.button("Приобрести товар")

    # Обработчик события
    if add_deal_btn:
        shoe_id = shoe_options[selected_shoe_name]
            
        # Добавляем запись о сделке и ждем доставку
        end_date = add_buy_shoe (shoe_id, login, deliv_date, point_id)
       
        st.success(f"Вы приобрели товар. Ожидаемая дата доставки: {deliv_date} ")

show_selling_shoes_page(st.session_state.get('login', None))
