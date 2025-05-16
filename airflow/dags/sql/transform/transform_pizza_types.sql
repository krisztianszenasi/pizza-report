INSERT INTO pizza_types (id, name, category, ingredients)
SELECT
    pizza_type_id,
    name,
    category,
    ingredients
FROM
    pizza_types_staging
ON CONFLICT (id) DO NOTHING;