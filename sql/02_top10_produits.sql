-- Top 10 produits par chiffre d'affaires
SELECT
    product_name,
    category,
    COUNT(*)                   AS nb_orders,
    ROUND(SUM(total_price), 2) AS revenue,
    ROUND(AVG(price), 2)       AS avg_price
FROM `ecommerce-pipeline-dev.ecommerce_raw.orders`
WHERE status = 'completed'
GROUP BY product_name, category
ORDER BY revenue DESC
LIMIT 10;