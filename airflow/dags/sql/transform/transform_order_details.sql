INSERT INTO order_details (id, order_id, pizza_id, quantity)
SELECT
    ods.order_details_id,
    ods.order_id,
    ods.pizza_id,
    ods.quantity
FROM
    order_details_staging ods
JOIN
    orders o ON o.id = ods.order_id
JOIN
    pizzas p ON p.id = ods.pizza_id
ON CONFLICT (id) DO NOTHING;
