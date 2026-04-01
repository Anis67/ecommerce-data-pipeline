-- Staging : nettoyage et standardisation des données brutes
with source as (
    select * from `ecommerce-pipeline-dev.ecommerce_raw.orders`
),

cleaned as (
    select
        order_id,
        customer_id,
        product_name,
        category,
        price,
        quantity,
        total_price,
        lower(trim(status))  as status,
        trim(country)        as country,
        timestamp            as ordered_at,
        date(timestamp)      as order_date
    from source
    where order_id is not null
      and customer_id is not null
      and price > 0
      and quantity > 0
)

select * from cleaned