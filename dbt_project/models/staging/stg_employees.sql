select
    employee_id,
    first_name,
    last_name,
    first_name || " " || last_name as full_name,
    department,
    job_title,
    job_level,
    base_salary,
    base_salary / 12 as monthly_salary,
    state,
    hire_date,
    termination_date,
    is_active,
    performance_rating,
    gender,
    age
from {{ source("hr", "raw_employees") }}
where employee_id is not null
  and base_salary > 0
  and age between 18 and 70
