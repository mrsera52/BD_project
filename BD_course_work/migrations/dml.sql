
-- Вставка данных в таблицу points
INSERT INTO
    points (point_name, time_work)
VALUES
    (
        'Москва, ул. Пушкина д. 99',
        'C 8.00 до 18.00'
    ),
    (
        'Санкт-Петербург, ул. Пушкина д. 52',
        'C 18.00 до 20.00'
    );
    INSERT INTO
    pay (pay_way)
VALUES
    (
        'Картой'
        
    ),
    (
        'Наличные'
    );

INSERT INTO
    users (login, user_role, user_password)
VALUES
    ('admin', 'admin', '$2b$12$iD5un9xBRjxTC6Dn4DAJD.ws5Y1GbFjD9i2n35M7c1cao0HUKPWMe');

INSERT INTO
    shoes_firms (firm_name, country)
VALUES
    (
        'Adidas',
        'Germany'
    ),
    (
        ' Anta',
        'China'
    ),
    (
        'Puma',
        'Vietnam'
    ),
    (
        'Nike',
        'USA'
    ),
    (
        'Reebok',
        'UK'
    );

INSERT INTO
    shoes_specifications (colour, weight, size)
VALUES
    ('black', 24.0, '9 US'),
    ('black', 25.0, '8 US'),
    ('black', 26.0, '9 US'),
    ('black', 27.0, '10 US'),
    ('black', 28.0, '11 US'),
    ('black', 29.0, '12 US'),
    ('black', 32.0, '13 US'),
    ('white', 24.0, '9 US'),
    ('white', 25.0, '8 US'),
    ('white', 26.0, '9 US'),
    ('white', 27.0, '10 US'),
    ('white', 28.0, '11 US'),
    ('white', 29.0, '12 US'),
    ('white', 32.0, '13 US'),
    ('white', 29.0, '8 US');
    

INSERT INTO
    shoes (firm_id, spec_id, price)
VALUES
    (1, 1, 10000),
    (1, 2, 10000),
    (2, 7, 8000),
    (2, 8, 8500),
    (3, 9, 9800),
    (3, 5, 10111),
    (4, 8, 18000),
    (4, 10, 16300),
    (5, 11, 15000),
    (5, 12, 10000);