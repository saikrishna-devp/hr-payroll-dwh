select * from {{ source("hr", "raw_employees") }}
