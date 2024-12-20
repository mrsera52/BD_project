import streamlit as st
import psycopg2
from repositories.user import get_user_id_by_name
#from repositories.regions import get_region_id
#from repositories.regions import get_all_regions
import bcrypt
from settings import DB_CONFIG

# Хеширование пароля
def hash_password(password):
    salt = bcrypt.gensalt()  # Генерация соли
    hashed_password = (bcrypt.hashpw(password.encode('utf-8'), salt)).decode('utf-8')
    return hashed_password

# Проверка пароля
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

# Регистрация пользователя
def register_user(login, password):
   

    hashed_password = hash_password(password)  # Хеширование пароля
    query = """
    INSERT INTO users (login, user_role, user_password)
    VALUES (%s, %s, %s);
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (login, "user", hashed_password))
            conn.commit()
    st.success("Регистрация успешна! Теперь вы можете войти.")
    return True

# Авторизация пользователя
def authenticate_user(login, password):
    query = """
    SELECT user_password FROM users WHERE login = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (login,))
            result = cur.fetchone()
            if result:
                stored_password = result[0]
                
                # Проверяем, является ли хеш пароля строкой и конвертируем в байты
                if isinstance(stored_password, str):
                    stored_password = stored_password.encode('utf-8')
                
                # Теперь можно безопасно сравнивать пароли
                if check_password(password, stored_password):
                    # Сохраняем user_id в session_state
                    user_id = get_user_id_by_name(login)
                    if user_id:
                        st.session_state.user_id = user_id
                        st.session_state.login = login
                        return True
    return False

# Главная функция для аутентификации и регистрации
def login_or_register():
    st.title("Добро пожаловать!")

    option = st.radio("Выберите действие:", ["Вход", "Регистрация"])

    if option == "Вход":
        login = st.text_input("Логин")
        password = st.text_input("Пароль", type="password")
        login_btn = st.button("Войти")

        if login_btn:
            if authenticate_user(login, password):
                st.success(f"Добро пожаловать, {login}!")
                return {"login": login}
            else:
                st.error("Неверное имя или пароль.")
        return None

    elif option == "Регистрация":
        login = st.text_input("Логин")
        #region_name = st.selectbox("Выберите регион", get_all_regions())
        password = st.text_input("Пароль", type="password")
        confirm_password = st.text_input("Подтвердите пароль", type="password")
        register_btn = st.button("Зарегистрироваться")

        if register_btn:
            if login.lower() == "admin":
                st.error("Имя 'admin' запрещено.")
            elif password != confirm_password:
                st.error("Пароли не совпадают.")
            elif register_user(login, password):
                return {"login": login}
        return None

def page_func():
    login = st.session_state.get('login', None)

    if st.session_state.get('login', None):
        st.success(f"Добро пожаловать, {login}!")
        if st.button("Выйти"):
            for key in st.session_state.keys():
                del st.session_state[key]  # Сбрасываем состояние
    elif not st.session_state.get('login', None):
        login_or_register()
        if st.button("Выйти"):
            for key in st.session_state.keys():
                del st.session_state[key]  # Сбрасываем состояние

page_func()
