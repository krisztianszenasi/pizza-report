INSERT INTO pizzas (id, pizza_type_id, size, price)
SELECT
    ps.pizza_id,
    ps.pizza_type_id,
    ps.size,
    ps.price
FROM
    pizzas_staging ps
JOIN
    pizza_types pt ON ps.pizza_type_id = pt.id
ON CONFLICT (id) DO NOTHING;
