-- Chiffre d'affaires par jour et par pays
SELECT
    DATE(timestamp)     AS order_date,
    country,
    COUNT(*)            AS nb_orders,
    ROUND(SUM(total_price), 2) AS revenue
FROM `ecommerce-pipeline-dev.ecommerce_raw.orders`
WHERE status = 'completed'
GROUP BY order_date, country
ORDER BY order_date DESC, revenue DESC;