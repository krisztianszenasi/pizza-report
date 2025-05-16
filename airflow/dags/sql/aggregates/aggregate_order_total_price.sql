DROP TABLE IF EXISTS aggregated_order_detail_total_price_name_category;


CREATE TABLE aggregated_order_detail_total_price_name_category(
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    time TIME NOT NULL,
    pizza_name TEXT NOT NULL,
    pizza_category TEXT NOT NULL,
    total_price NUMERIC NOT NULL
);


INSERT INTO aggregated_order_detail_total_price_name_category(id, date, time, pizza_name, pizza_category, total_price)
SELECT
	od.id,
    o.date,
    o.time,
    pt.name,
    pt.category,
    sum(od.quantity * p.price) as total_price
FROM orders o
JOIN
	order_details od on od.order_id = o.id
JOIN
	pizzas p on od.pizza_id = p.id
join
	pizza_types pt  on p.pizza_type_id = pt.id
GROUP BY
    od.id, o.date, o.time, pt.name, pt.category
ON CONFLICT (id) DO NOTHING;
