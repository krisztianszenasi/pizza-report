INSERT INTO orders (id,  date, time)
SELECT
    order_id,
    date,
    time
FROM
    orders_staging
ON CONFLICT (id) DO NOTHING;
