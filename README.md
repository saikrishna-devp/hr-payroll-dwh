# HR Payroll Analytics Data Warehouse

An end-to-end HR payroll analytics platform processing 10,000 employees
with real US payroll tax calculations, dbt transformations, PostgreSQL
data warehouse and a live Tableau Public dashboard.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![dbt](https://img.shields.io/badge/dbt-1.11-FF694B?style=flat-square&logo=dbt&logoColor=white)](https://getdbt.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Tableau](https://img.shields.io/badge/Tableau-Public-E97627?style=flat-square&logo=tableau&logoColor=white)](https://public.tableau.com)

## Live Dashboard

View the interactive Tableau dashboard:
https://public.tableau.com/views/HR_Dashboard_Analytics_17757057726400/Dashboard1

## Project Structure
## Pipeline Results

- Employees: 10,000
- Payroll records: 102,592 (12 months)
- Attrition records: 163
- Pipeline runtime: 15.6 seconds

## Payroll Tax Calculations

Real US payroll formulas applied to every employee every month:

- Federal Tax: 22 percent
- State Tax: 5 percent
- Social Security: 6.2 percent
- Medicare: 1.45 percent

Annual totals:
- Total Federal Tax: 188,921,518 USD
- Total State Tax: 42,936,724 USD
- Total Net Pay: 561,182,779 USD

## Data Quality Checks

8 employee checks and 6 payroll checks run before every load.

Employee checks: row count, null IDs, duplicate IDs,
positive salary, valid age, valid job level,
valid performance rating, parseable hire date.

Payroll checks: null IDs, positive gross, positive net,
net less than gross, valid month, no duplicates.

## dbt Architecture

Three layer architecture:
- Raw: exact copy of source data as views
- Staging: cleaned and standardized as views
- Marts: business aggregations as tables

## Setup

1. Install dependencies: pip install -r requirements.txt
2. Start PostgreSQL: docker start claims-db
3. Run pipeline: python run_pipeline.py
4. Open Tableau Public and connect to CSV files in data/ folder

## Connect

Saikrishna Suryavamsham - Senior Data Engineer - Tampa FL
LinkedIn: linkedin.com/in/sai207
Email: krishnasv207@gmail.com
