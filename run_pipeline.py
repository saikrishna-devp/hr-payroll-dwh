import os
import time
import sqlite3
import pandas as pd
from datetime import datetime
import yaml


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(ts + " | " + msg)


def load_config():
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)


def show_results(db_file):
    log("=" * 60)
    log("ANALYTICS RESULTS")
    log("=" * 60)

    conn = sqlite3.connect(db_file)

    queries = {
        "Workforce summary": """
            SELECT
                COUNT(*) as total_employees,
                SUM(is_active) as active_employees,
                COUNT(*) - SUM(is_active) as terminated,
                ROUND(AVG(base_salary), 2) as avg_salary,
                ROUND(MIN(base_salary), 2) as min_salary,
                ROUND(MAX(base_salary), 2) as max_salary
            FROM raw_employees
        """,
        "Headcount by department": """
            SELECT department,
                   COUNT(*) as total,
                   SUM(is_active) as active,
                   ROUND(AVG(base_salary), 2) as avg_salary
            FROM raw_employees
            GROUP BY department
            ORDER BY active DESC
        """,
        "Salary by job level": """
            SELECT job_level,
                   COUNT(*) as employees,
                   ROUND(AVG(base_salary), 2) as avg_salary,
                   ROUND(MIN(base_salary), 2) as min_salary,
                   ROUND(MAX(base_salary), 2) as max_salary
            FROM raw_employees
            GROUP BY job_level
            ORDER BY avg_salary DESC
        """,
        "Monthly payroll summary": """
            SELECT month,
                   COUNT(DISTINCT employee_id) as employees_paid,
                   ROUND(SUM(gross_salary), 2) as total_gross,
                   ROUND(SUM(total_deductions), 2) as total_deductions,
                   ROUND(SUM(net_pay), 2) as total_net_pay
            FROM fact_payroll
            GROUP BY month
            ORDER BY month
        """,
        "Tax deductions breakdown": """
            SELECT
                ROUND(SUM(federal_tax), 2) as total_federal_tax,
                ROUND(SUM(state_tax), 2) as total_state_tax,
                ROUND(SUM(social_security), 2) as total_social_security,
                ROUND(SUM(medicare), 2) as total_medicare,
                ROUND(SUM(total_deductions), 2) as total_deductions,
                ROUND(SUM(net_pay), 2) as total_net_pay
            FROM fact_payroll
        """,
        "Attrition by department": """
            SELECT department,
                   COUNT(*) as employees_left,
                   ROUND(AVG(tenure_years), 1) as avg_tenure_years,
                   ROUND(AVG(base_salary), 2) as avg_salary
            FROM fact_attrition
            GROUP BY department
            ORDER BY employees_left DESC
        """,
        "Performance rating distribution": """
            SELECT performance_rating,
                   COUNT(*) as employees,
                   ROUND(AVG(base_salary), 2) as avg_salary
            FROM raw_employees
            GROUP BY performance_rating
            ORDER BY employees DESC
        """,
    }

    for title, sql in queries.items():
        print("\n  " + "-"*55)
        print("  " + title)
        print("  " + "-"*55)
        try:
            result = pd.read_sql_query(sql, conn)
            print(result.to_string(index=False))
        except Exception as e:
            print("  Error: " + str(e))

    conn.close()


if __name__ == "__main__":
    start = time.time()
    config = load_config()
    os.makedirs("data", exist_ok=True)

    log("=" * 60)
    log("  HR PAYROLL ANALYTICS PIPELINE")
    log("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    log("=" * 60)

    log("STEP 1 - EXTRACT: Generating HR data...")
    from src.extract.hr_extractor import generate_employees
    employees_df = generate_employees(
        n=config["pipeline"]["n_employees"],
        output_file=config["pipeline"]["raw_file"]
    )
    log("Extracted " + str(len(employees_df)) + " employees")

    log("STEP 2 - VALIDATE: Running quality checks...")
    from src.quality.hr_validator import validate_employees
    emp_valid = validate_employees(employees_df)

    log("STEP 3 - TRANSFORM: Calculating payroll...")
    from src.transform.payroll_calculator import calculate_monthly_payroll, calculate_attrition
    payroll_df   = calculate_monthly_payroll(employees_df, year=2024)
    attrition_df = calculate_attrition(employees_df, year=2024)

    log("STEP 4 - VALIDATE PAYROLL: Running payroll checks...")
    from src.quality.hr_validator import validate_payroll
    pay_valid = validate_payroll(payroll_df)

    log("STEP 5 - LOAD: Loading to PostgreSQL + SQLite...")
    from src.load.warehouse_loader import run_loader
    run_loader(employees_df, payroll_df, attrition_df, config)

    log("STEP 6 - DBT: Running transformations...")
    import subprocess
    result = subprocess.run(
        ["C:\\Users\\saira\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\dbt.exe",
         "run", "--profiles-dir", ".", "--project-dir", "."],
        cwd="dbt_project",
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print("dbt warning: " + result.stderr[:200])

    show_results(config["pipeline"]["db_file"])

    elapsed = round(time.time() - start, 1)
    log("=" * 60)
    log("  PIPELINE COMPLETE in " + str(elapsed) + " seconds!")
    log("  Employees: " + str(len(employees_df)))
    log("  Payroll records: " + str(len(payroll_df)))
    log("  Attrition records: " + str(len(attrition_df)))
    log("=" * 60)
