DROP TABLE IF EXISTS pizza_types_staging;
DROP TABLE IF EXISTS pizzas_staging;
DROP TABLE IF EXISTS orders_staging;
DROP TABLE IF EXISTS order_details_staging;


CREATE TABLE pizzas_staging (
    pizza_id TEXT PRIMARY KEY,
    pizza_type_id TEXT,
    size TEXT,
    price NUMERIC(5,2)
);


CREATE TABLE pizza_types_staging (
    pizza_type_id TEXT PRIMARY KEY,
    name TEXT,
    category TEXT,
    ingredients TEXT
);
 

CREATE TABLE orders_staging (
    order_id INTEGER PRIMARY KEY,
    date DATE,
    time TIME
);


CREATE TABLE order_details_staging (
    order_details_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    pizza_id TEXT,
    quantity INTEGER
);
