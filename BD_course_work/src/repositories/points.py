import psycopg2
import psycopg2.extras
from settings import DB_CONFIG

# Получение ID региона по имени
def get_point_id(point_name):
    query = "SELECT point_id FROM points WHERE point_name = %s;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (point_name,))
            result = cur.fetchone()
            return result[0] if result else None

# Получение всех регионов из базы
def get_all_points():
    query = "SELECT point_name FROM points;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            points = [row[0] for row in cur.fetchall()]
    return points
    