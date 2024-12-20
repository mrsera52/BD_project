import psycopg2
import psycopg2.extras
from repositories.user import get_user_id_by_name
from datetime import date
from settings import DB_CONFIG


def get_shoes() -> list[dict]:
    print("Получение пары")
    query = """
        SELECT b.shoe_id, c.firm_name, a.colour, a.size, b.price 
        FROM shoes_specifications as a 
        JOIN shoes as b USING(spec_id) 
        JOIN shoes_firms as c USING(firm_id)
        ORDER BY c.firm_name;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()


def add_buy_shoe (shoe_id: int, login: str, deliv_date: date, point_id: int):
    user_id = get_user_id_by_name(login)
    if not user_id:
        return  # Если не нашли user_id, прекращаем выполнение

    # Получаем firm_id лодки
    query_firm = """
    SELECT firm_id FROM shoes WHERE shoe_id = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query_firm, (shoe_id,))
            firm_id = cur.fetchone()[0]
    

    # Запрос для вставки записи в таблицу shoe_exploitation с датой начала и конца эксплуатации
    query = """
    INSERT INTO shoe_buy (user_id, shoe_id, point_id, deliv_date) 
    VALUES (%s, %s, %s, %s);
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (user_id, shoe_id, point_id, deliv_date))
            conn.commit()

    # Возвращаем успешный результат
    return deliv_date