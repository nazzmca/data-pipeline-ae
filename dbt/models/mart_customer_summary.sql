-- Final output model with masked email exposure for non-sensitive reporting
select
    customer_id,
    customer_name,
    case
        when email is null then null
        else regexp_replace(email, '@.*$', '@masked.example')
    end as masked_email,
    segment,
    total_order_value,
    order_count
from {{ ref('int_customer_orders') }}
