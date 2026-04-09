select
    department,
    job_level,
    state,
    gender,
    performance_rating,
    count(*) as total_employees,
    sum(is_active) as active_employees,
    count(*) - sum(is_active) as terminated_employees,
    round(avg(base_salary), 2) as avg_salary,
    round(avg(age), 1) as avg_age
from "hr_dwh"."public"."raw_employees"
group by department, job_level, state, gender, performance_rating