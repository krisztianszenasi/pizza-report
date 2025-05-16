DROP TABLE IF EXISTS aggregated_ingredient_per_day;


CREATE TABLE aggregated_ingredient_per_day(
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    ingredient TEXT NOT NULL
);


insert into aggregated_ingredient_per_day(date, ingredient)
select
	o.date,
	i.name 
from orders o
join
	order_details od on o.id = od.order_id
join
	pizzas p on p.id  = od.pizza_id
join
	pizza_types pt on p.pizza_type_id = pt.id
join
	pizza_ingredients pi on pt.id = pi.pizza_type_id
join
	ingredients i on i.id  = pi.ingredient_id