-- Dimension produits avec métriques
with orders as (
    select * from {{ ref('stg_orders') }}
),

product_metrics as (
    select
        product_name,
        category,
        count(*)                        as total_orders,
        round(sum(total_price), 2)      as total_revenue,
        round(avg(price), 2)            as avg_price,
        sum(quantity)                   as total_quantity_sold,
        countif(status = 'completed')   as completed_orders
    from orders
    group by product_name, category
)

select
    {{ dbt_utils.generate_surrogate_key(['product_name']) }} as product_id,
    product_name,
    category,
    total_orders,
    total_revenue,
    avg_price,
    total_quantity_sold,
    completed_orders
from product_metrics