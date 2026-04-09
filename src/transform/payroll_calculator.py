import pandas as pd
from datetime import datetime


FEDERAL_TAX_RATE    = 0.22
STATE_TAX_RATE      = 0.05
SOCIAL_SECURITY     = 0.062
MEDICARE            = 0.0145
TOTAL_DEDUCTION_RATE = FEDERAL_TAX_RATE + STATE_TAX_RATE + SOCIAL_SECURITY + MEDICARE


def calculate_monthly_payroll(employees_df, year=2024):
    print("Calculating monthly payroll for " + str(len(employees_df)) + " employees...")
    records = []

    for _, emp in employees_df.iterrows():
        monthly_gross = round(emp["base_salary"] / 12, 2)

        federal_tax    = round(monthly_gross * FEDERAL_TAX_RATE, 2)
        state_tax      = round(monthly_gross * STATE_TAX_RATE, 2)
        social_security = round(monthly_gross * SOCIAL_SECURITY, 2)
        medicare       = round(monthly_gross * MEDICARE, 2)
        total_deductions = round(federal_tax + state_tax + social_security + medicare, 2)
        net_pay        = round(monthly_gross - total_deductions, 2)

        hire_date = pd.to_datetime(emp["hire_date"])
        term_date = pd.to_datetime(emp["termination_date"]) if pd.notna(emp.get("termination_date")) else None

        for month in range(1, 13):
            pay_date = datetime(year, month, 28)

            if hire_date > pay_date:
                continue
            if term_date and term_date < pay_date:
                continue

            records.append({
                "payroll_id":       emp["employee_id"] + "-" + str(year) + "-" + str(month).zfill(2),
                "employee_id":      emp["employee_id"],
                "department":       emp["department"],
                "job_level":        emp["job_level"],
                "state":            emp["state"],
                "pay_period":       pay_date.strftime("%Y-%m-%d"),
                "year":             year,
                "month":            month,
                "gross_salary":     monthly_gross,
                "federal_tax":      federal_tax,
                "state_tax":        state_tax,
                "social_security":  social_security,
                "medicare":         medicare,
                "total_deductions": total_deductions,
                "net_pay":          net_pay,
                "performance_rating": emp["performance_rating"],
            })

    df = pd.DataFrame(records)
    print("Generated " + str(len(df)) + " payroll records for " + str(year))
    return df


def calculate_attrition(employees_df, year=2024):
    print("Calculating attrition metrics...")
    records = []

    terminated = employees_df[employees_df["is_active"] == 0].copy()
    terminated["termination_date"] = pd.to_datetime(terminated["termination_date"])
    terminated = terminated[terminated["termination_date"].dt.year == year]

    for _, emp in terminated.iterrows():
        term_date = emp["termination_date"]
        hire_date = pd.to_datetime(emp["hire_date"])
        tenure_days = (term_date - hire_date).days

        records.append({
            "attrition_id":     emp["employee_id"] + "-ATT",
            "employee_id":      emp["employee_id"],
            "department":       emp["department"],
            "job_level":        emp["job_level"],
            "job_title":        emp["job_title"],
            "state":            emp["state"],
            "hire_date":        emp["hire_date"],
            "termination_date": term_date.strftime("%Y-%m-%d"),
            "tenure_days":      tenure_days,
            "tenure_years":     round(tenure_days / 365, 1),
            "performance_rating": emp["performance_rating"],
            "base_salary":      emp["base_salary"],
        })

    df = pd.DataFrame(records)
    print("Found " + str(len(df)) + " attrition records for " + str(year))
    return df
