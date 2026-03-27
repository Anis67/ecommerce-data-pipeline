-- Clients avec plus de 3 commandes (sous-requête)
SELECT
    customer_id,
    nb_orders,
    ROUND(total_spent, 2) AS total_spent
FROM (
    SELECT
        customer_id,
        COUNT(*)         AS nb_orders,
        SUM(total_price) AS total_spent
    FROM `ecommerce-pipeline-dev.ecommerce_raw.orders`
    WHERE status = 'completed'
    GROUP BY customer_id
) sub
WHERE nb_orders > 1
ORDER BY total_spent DESC
LIMIT 20;