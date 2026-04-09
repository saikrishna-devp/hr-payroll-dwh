import os
import random
import pandas as pd
from datetime import datetime, timedelta


def generate_employees(n=10000, output_file="data/employees.csv"):
    random.seed(42)

    departments = [
        ("Engineering",     ["Software Engineer","Senior Engineer","Lead Engineer","Engineering Manager"]),
        ("Data",            ["Data Analyst","Data Engineer","Senior Data Engineer","Data Science Manager"]),
        ("Finance",         ["Financial Analyst","Senior Analyst","Finance Manager","CFO"]),
        ("HR",              ["HR Coordinator","HR Specialist","HR Manager","HR Director"]),
        ("Sales",           ["Sales Rep","Senior Sales Rep","Sales Manager","VP Sales"]),
        ("Marketing",       ["Marketing Analyst","Senior Analyst","Marketing Manager","CMO"]),
        ("Operations",      ["Operations Analyst","Senior Analyst","Ops Manager","VP Operations"]),
        ("Legal",           ["Legal Analyst","Senior Counsel","Legal Manager","General Counsel"]),
        ("Customer Support",["Support Rep","Senior Support","Support Manager","VP Support"]),
        ("Product",         ["Product Analyst","Product Manager","Senior PM","VP Product"]),
    ]

    job_levels = {
        0: ("Junior",    45000,  75000),
        1: ("Mid",       75000,  110000),
        2: ("Senior",    110000, 160000),
        3: ("Manager",   160000, 220000),
    }

    states = ["FL","TX","CA","NY","IL","PA","OH","GA","NC","MI",
              "WA","AZ","MA","TN","IN","MO","MD","WI","CO","MN"]

    performance_ratings = ["Exceeds"]*20 + ["Meets"]*60 + ["Below"]*15 + ["PIP"]*5

    rows = []
    for i in range(n):
        dept, roles = random.choice(departments)
        level_idx   = random.choices([0,1,2,3], weights=[30,40,20,10])[0]
        level_name, sal_min, sal_max = job_levels[level_idx]
        role        = roles[level_idx]
        base_salary = round(random.uniform(sal_min, sal_max), 2)
        hire_date   = datetime(2015,1,1) + timedelta(days=random.randint(0, 3650))
        is_active   = random.choices([1,0], weights=[85,15])[0]
        term_date   = None
        if not is_active:
            term_date = hire_date + timedelta(days=random.randint(180, 2000))

        rows.append({
            "employee_id":      f"EMP{i+1:06d}",
            "first_name":       random.choice(["James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda","William","Barbara","David","Susan","Richard","Jessica","Joseph","Sarah","Thomas","Karen","Charles","Lisa"]),
            "last_name":        random.choice(["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Wilson","Anderson","Taylor","Thomas","Jackson","White","Harris","Martin","Thompson","Young","Robinson","Lewis"]),
            "department":       dept,
            "job_title":        role,
            "job_level":        level_name,
            "base_salary":      base_salary,
            "state":            random.choice(states),
            "hire_date":        hire_date.strftime("%Y-%m-%d"),
            "termination_date": term_date.strftime("%Y-%m-%d") if term_date else None,
            "is_active":        is_active,
            "performance_rating": random.choice(performance_ratings),
            "gender":           random.choice(["Male","Female","Non-binary"]),
            "age":              random.randint(22, 65),
        })

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print("Generated " + str(len(df)) + " employees -> " + output_file)
    return df


if __name__ == "__main__":
    generate_employees()
