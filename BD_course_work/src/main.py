import streamlit as st

# Главная логика приложения
def main():
    login = st.session_state.get('login', None)

    if not login:
        st.error("вы не вошли в систему")
        return
    
    if login:
        st.success(f"{login}, вы успешно вошли!")

if __name__ == "__main__":
    main()