

-- Таблица для хранения данных о пользователях
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    login VARCHAR(256),
    user_role VARCHAR(256),
    user_password VARCHAR(256)
    
);

COMMENT ON TABLE users IS 'Данные о пользователях';

COMMENT ON COLUMN users.user_id IS 'юзер айди';
COMMENT ON COLUMN users.login IS 'логин';
COMMENT ON COLUMN users.user_role IS 'роль';
COMMENT ON COLUMN users.user_password IS 'пароль';

-- Таблица для хранения информации о производителях кроссовок
CREATE TABLE shoes_firms (
    firm_id SERIAL PRIMARY KEY,
    firm_name VARCHAR(256),
    country VARCHAR(100)
);

COMMENT ON TABLE shoes_firms IS 'Информация о производителях кроссовок';

COMMENT ON COLUMN shoes_firms.firm_id IS 'Уникальный идентификатор фирмы';
COMMENT ON COLUMN shoes_firms.firm_name IS 'Название фирмы';
COMMENT ON COLUMN shoes_firms.country IS 'Страна производител';

-- Таблица для хранения состава каждой поставки
CREATE TABLE shoes_specifications (
    spec_id SERIAL PRIMARY KEY,
    colour VARCHAR(30),
    weight NUMERIC,
    size VARCHAR(10)
);

COMMENT ON TABLE shoes_specifications IS 'Состав поставки продуктов ';

COMMENT ON COLUMN shoes_specifications.spec_id IS 'Уникальный идентификатор строки поставки';
COMMENT ON COLUMN shoes_specifications.colour IS 'Модель';
COMMENT ON COLUMN shoes_specifications.weight IS 'длина стельки в см';
COMMENT ON COLUMN shoes_specifications.size IS 'Размер ';

-- Таблица для хранения информации о пунктах выдавас
CREATE TABLE points (
    point_id SERIAL PRIMARY KEY,
    
    point_name VARCHAR(100),
    time_work VARCHAR(100)
);

COMMENT ON TABLE points IS 'Информация о пунктах выдачи ';

COMMENT ON COLUMN points.point_id IS 'Уникальный идентификатор пункта';
COMMENT ON COLUMN points.point_name IS 'Название пункта';
COMMENT ON COLUMN points.time_work IS 'время работы';


-- Таблица для хранения основной информации о паре
CREATE TABLE shoes (
    shoe_id SERIAL PRIMARY KEY,
    firm_id INT,
    spec_id INT,
    price INT,
    FOREIGN KEY (firm_id) REFERENCES shoes_firms(firm_id) ON DELETE CASCADE,
    FOREIGN KEY (spec_id) REFERENCES shoes_specifications(spec_id) ON DELETE CASCADE
);

COMMENT ON TABLE shoes IS 'Основная информация о кроссовках и их стоимости';

COMMENT ON COLUMN shoes.shoe_id IS 'Уникальный идентификатор пары';
COMMENT ON COLUMN shoes.firm_id IS 'Идентификатор фирмы-производителя';
COMMENT ON COLUMN shoes.spec_id IS 'Идентификатор ';
COMMENT ON COLUMN shoes.price IS 'Цена пары';


-- Таблица для хранения информации о сделках
CREATE TABLE deals (
    deal_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    shoe_id INT REFERENCES shoes(shoe_id) ON DELETE CASCADE,
    deal_time DATE NOT NULL,
    summ INT
);




COMMENT ON COLUMN deals.deal_id IS 'Уникальный идентификатор сделки';
COMMENT ON COLUMN deals.user_id IS 'Идентификатор пользователя, совершившей покупку';
COMMENT ON COLUMN deals.shoe_id IS 'Идентификатор пары, которая была куплена';
COMMENT ON COLUMN deals.deal_time IS 'Дата, когда была совершена сделка';

COMMENT ON TABLE deals IS 'Информация об оплате';

CREATE TABLE pay (
    pay_id SERIAL PRIMARY KEY,
    
    pay_way VARCHAR(100)
);


-- Таблица для хранения информации о доставляемом заказе
CREATE TABLE shoe_buy (
    exp_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    shoe_id INT REFERENCES shoes(shoe_id) ON DELETE CASCADE,  -- Ссылка на пару из таблицы shoes
    point_id INT REFERENCES points(point_id) ON DELETE CASCADE,
    pay_id INT REFERENCES pay(pay_id) ON DELETE CASCADE,
    
    deliv_date DATE  -- Дата ожидаемой доставки
);

COMMENT ON TABLE shoe_buy IS 'Информация о купленной паре ';
COMMENT ON COLUMN shoe_buy.exp_id IS 'Уникальный идентификатор ';
COMMENT ON COLUMN shoe_buy.user_id IS 'Идентификатор пользователя';
COMMENT ON COLUMN shoe_buy.shoe_id IS 'Идентификатор пары';
COMMENT ON COLUMN shoe_buy.deliv_date IS 'Дата ожидаесой доставки';

