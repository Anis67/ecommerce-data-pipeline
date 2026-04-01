-- Table de faits : une ligne par commande
with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select customer_id, customer_segment
    from {{ ref('dim_customers') }}
)

select
    o.order_id,
    o.customer_id,
    o.product_name,
    o.category,
    o.price,
    o.quantity,
    o.total_price,
    o.status,
    o.country,
    o.ordered_at,
    o.order_date,
    round(o.price * o.quantity, 2)  as total_price_calculated,
    o.total_price > 200             as is_high_value,
    extract(hour from o.ordered_at) as order_hour,
    c.customer_segment,
    current_timestamp()             as loaded_at
from orders o
left join customers c using (customer_id)