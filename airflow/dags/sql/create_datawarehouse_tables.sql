CREATE TABLE IF NOT EXISTS pizza_types (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    ingredients TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pizzas (
    id TEXT PRIMARY KEY,
    pizza_type_id TEXT REFERENCES pizza_types(id),
    size TEXT NOT NULL,
    price NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    time TIME NOT NULL
);

 CREATE TABLE IF NOT EXISTS order_details (
    id INTEGER PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    pizza_id TEXT REFERENCES pizzas(id),
    quantity INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS ingredients (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS pizza_ingredients (
    id SERIAL PRIMARY KEY,
    pizza_type_id TEXT REFERENCES pizza_types(id),
    ingredient_id INTEGER REFERENCES ingredients(id)
)