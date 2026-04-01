-- Dimension clients avec métriques agrégées
with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

customer_metrics as (
    select
        customer_id,
        count(*)                        as total_orders,
        round(sum(total_price), 2)      as total_spent,
        round(avg(total_price), 2)      as avg_order_value,
        countif(status = 'completed')   as completed_orders,
        countif(status = 'cancelled')   as cancelled_orders
    from orders
    group by customer_id
)

select
    c.customer_id,
    c.country,
    c.first_order_at,
    c.last_order_at,
    m.total_orders,
    m.total_spent,
    m.avg_order_value,
    m.completed_orders,
    m.cancelled_orders,
    case
        when m.total_spent > 1000 then 'VIP'
        when m.total_spent > 500  then 'Premium'
        else 'Standard'
    end as customer_segment
from customers c
left join customer_metrics m using (customer_id)