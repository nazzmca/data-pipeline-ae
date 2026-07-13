-- Simple security-focused output check
select
    customer_id,
    customer_name,
    masked_email,
    segment
from {{ ref('mart_customer_summary') }}
where masked_email is not null
