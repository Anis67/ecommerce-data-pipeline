-- Répartition des statuts avec pourcentage (WINDOW FUNCTION)
SELECT
    status,
    COUNT(*)  AS nb_orders,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2
    ) AS pct_total
FROM `ecommerce-pipeline-dev.ecommerce_raw.orders`
GROUP BY status
ORDER BY nb_orders DESC;