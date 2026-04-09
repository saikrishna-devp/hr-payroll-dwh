select
    department,
    job_level,
    year,
    month,
    count(distinct employee_id) as employees_paid,
    round(sum(gross_salary), 2) as total_gross,
    round(sum(federal_tax), 2) as total_federal_tax,
    round(sum(state_tax), 2) as total_state_tax,
    round(sum(social_security), 2) as total_social_security,
    round(sum(medicare), 2) as total_medicare,
    round(sum(total_deductions), 2) as total_deductions,
    round(sum(net_pay), 2) as total_net_pay,
    round(avg(gross_salary), 2) as avg_gross_salary
from {{ source("hr", "fact_payroll") }}
group by department, job_level, year, month
