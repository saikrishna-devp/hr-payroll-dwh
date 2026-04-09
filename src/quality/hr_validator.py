import pandas as pd


def validate_employees(df):
    print("Running HR data quality checks...")
    checks = []

    def check(name, passed, detail=""):
        status = "PASS" if passed else "FAIL"
        print("  [" + status + "] " + name + " " + detail)
        checks.append(passed)

    check("Row count valid",
          1000 <= len(df) <= 100000,
          "(" + str(len(df)) + " rows)")

    check("No null employee IDs",
          df["employee_id"].notna().all(),
          "(" + str(df["employee_id"].isna().sum()) + " nulls)")

    check("No duplicate employee IDs",
          df["employee_id"].nunique() == len(df),
          "(" + str(df["employee_id"].nunique()) + " unique)")

    check("Salary is positive",
          (df["base_salary"] > 0).all(),
          "(min=" + str(df["base_salary"].min()) + ")")

    check("Age is valid",
          df["age"].between(18, 70).all(),
          "(min=" + str(df["age"].min()) + " max=" + str(df["age"].max()) + ")")

    valid_levels = {"Junior", "Mid", "Senior", "Manager"}
    check("Job level is valid",
          df["job_level"].isin(valid_levels).all(),
          "(found: " + str(df["job_level"].unique().tolist()) + ")")

    valid_ratings = {"Exceeds", "Meets", "Below", "PIP"}
    check("Performance rating is valid",
          df["performance_rating"].isin(valid_ratings).all(),
          "(found: " + str(df["performance_rating"].unique().tolist()) + ")")

    check("Hire date is parseable",
          pd.to_datetime(df["hire_date"], errors="coerce").notna().all(),
          "")

    passed = sum(checks)
    total  = len(checks)
    print("Result: " + str(passed) + "/" + str(total) + " checks passed")
    return passed == total


def validate_payroll(df):
    print("Running payroll quality checks...")
    checks = []

    def check(name, passed, detail=""):
        status = "PASS" if passed else "FAIL"
        print("  [" + status + "] " + name + " " + detail)
        checks.append(passed)

    check("No null payroll IDs",
          df["payroll_id"].notna().all(),
          "(" + str(df["payroll_id"].isna().sum()) + " nulls)")

    check("Gross salary positive",
          (df["gross_salary"] > 0).all(),
          "(min=" + str(df["gross_salary"].min()) + ")")

    check("Net pay positive",
          (df["net_pay"] > 0).all(),
          "(min=" + str(df["net_pay"].min()) + ")")

    check("Net pay less than gross",
          (df["net_pay"] < df["gross_salary"]).all(),
          "")

    check("Month is valid",
          df["month"].between(1, 12).all(),
          "(values: " + str(sorted(df["month"].unique().tolist())) + ")")

    check("No duplicate payroll IDs",
          df["payroll_id"].nunique() == len(df),
          "(" + str(df["payroll_id"].nunique()) + " unique)")

    passed = sum(checks)
    total  = len(checks)
    print("Result: " + str(passed) + "/" + str(total) + " checks passed")
    return passed == total
