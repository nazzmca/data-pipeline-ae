-- Intermediate model joining customers and orders
select
    c.customer_id,
    c.customer_name,
    c.segment,
    sum(o.order_total) as total_order_value,
    count(o.order_id) as order_count
from {{ ref('stg_customers') }} c
left join {{ source('raw', 'orders') }} o
    on c.customer_id = o.customer_id
group by 1, 2, 3
