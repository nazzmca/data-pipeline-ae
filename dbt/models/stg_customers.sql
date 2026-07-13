-- Staging model for customer data
select
    cast(customer_id as int) as customer_id,
    customer_name,
    email,
    segment,
    current_timestamp() as loaded_at
from {{ source('raw', 'customers') }}
