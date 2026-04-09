import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text


def get_engine(config):
    db = config["database"]
    return create_engine(
        "postgresql+psycopg2://" + db["user"] + ":" + db["password"] +
        "@" + db["host"] + ":" + str(db["port"]) + "/" + db["name"]
    )


def create_tables(engine):
    sql = """
    CREATE TABLE IF NOT EXISTS raw_employees (
        employee_id         VARCHAR(10) PRIMARY KEY,
        first_name          VARCHAR(50),
        last_name           VARCHAR(50),
        department          VARCHAR(50),
        job_title           VARCHAR(50),
        job_level           VARCHAR(20),
        base_salary         DECIMAL(12,2),
        state               VARCHAR(5),
        hire_date           DATE,
        termination_date    DATE,
        is_active           INTEGER,
        performance_rating  VARCHAR(20),
        gender              VARCHAR(20),
        age                 INTEGER
    );

    CREATE TABLE IF NOT EXISTS fact_payroll (
        payroll_id          VARCHAR(20) PRIMARY KEY,
        employee_id         VARCHAR(10),
        department          VARCHAR(50),
        job_level           VARCHAR(20),
        state               VARCHAR(5),
        pay_period          DATE,
        year                INTEGER,
        month               INTEGER,
        gross_salary        DECIMAL(12,2),
        federal_tax         DECIMAL(12,2),
        state_tax           DECIMAL(12,2),
        social_security     DECIMAL(12,2),
        medicare            DECIMAL(12,2),
        total_deductions    DECIMAL(12,2),
        net_pay             DECIMAL(12,2),
        performance_rating  VARCHAR(20)
    );

    CREATE TABLE IF NOT EXISTS fact_attrition (
        attrition_id        VARCHAR(15) PRIMARY KEY,
        employee_id         VARCHAR(10),
        department          VARCHAR(50),
        job_level           VARCHAR(20),
        job_title           VARCHAR(50),
        state               VARCHAR(5),
        hire_date           DATE,
        termination_date    DATE,
        tenure_days         INTEGER,
        tenure_years        DECIMAL(5,1),
        performance_rating  VARCHAR(20),
        base_salary         DECIMAL(12,2)
    );
    """
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    print("Tables created successfully")


def load_to_postgres(df, table_name, engine):
    try:
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print("  [PostgreSQL] " + str(len(df)) + " rows -> " + table_name)
    except Exception as e:
        print("  PostgreSQL error: " + str(e))


def load_to_sqlite(df, table_name, db_file):
    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print("  [SQLite] " + str(len(df)) + " rows -> " + table_name)


def run_loader(employees_df, payroll_df, attrition_df, config):
    engine  = get_engine(config)
    db_file = config["pipeline"]["db_file"]

    print("Creating tables...")
    create_tables(engine)

    print("Loading employees...")
    load_to_postgres(employees_df, "raw_employees", engine)
    load_to_sqlite(employees_df, "raw_employees", db_file)

    print("Loading payroll...")
    load_to_postgres(payroll_df, "fact_payroll", engine)
    load_to_sqlite(payroll_df, "fact_payroll", db_file)

    print("Loading attrition...")
    load_to_postgres(attrition_df, "fact_attrition", engine)
    load_to_sqlite(attrition_df, "fact_attrition", db_file)

    print("All data loaded successfully!")
