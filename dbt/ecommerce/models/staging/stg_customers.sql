-- Staging : extraction des clients uniques
with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select distinct
        customer_id,
        country,
        min(ordered_at) over (partition by customer_id) as first_order_at,
        max(ordered_at) over (partition by customer_id) as last_order_at
    from orders
)

select * from customers