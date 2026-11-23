
# TalentScope AI
### Competitive Talent Intelligence & Workforce Benchmarking System

## Project Overview

TalentScope AI is a data analytics application designed to explore
job-posting patterns and compare skill requirements across fictional
organisations.

The system uses Python, SQL, SQLite and Streamlit to analyse job
families, skill frequency, experience requirements, locations and
company-level workforce demand indicators.

It provides interactive dashboards and comparative visualisations
to demonstrate how talent intelligence can support analytical
decision-making.

## Key Features

- Interactive company, industry, role and location filters
- Job-family and industry distribution analysis
- Skill frequency analysis
- Company-level skill benchmarking
- Cross-company skill comparison heatmap
- Monthly job-posting trend analysis
- SQLite-based data storage and SQL analysis
- Data quality checks
- Filtered CSV export

## Technology Stack

- Python
- Pandas
- SQLite
- SQL
- Streamlit
- Plotly
- VS Code
- Git and GitHub

## Dataset

The project currently uses a synthetic dataset containing
300 fictional job-posting records across 10 fictional companies.

The dataset includes:
- Company and industry
- Job title
- Location
- Experience requirements
- Required skills
- Posting date
- Source type

**Data disclaimer:** All current records and company names are
fictional. The project does not represent real hiring activity,
actual competitor intelligence or verified labour-market trends.

## Project Structure

```text
TalentScope_AI/
│
├── app.py
├── analysis.py
├── create_database.py
├── talentscope.db
├── requirements.txt
├── README.md
│
├── data/
│   └── job_postings_synthetic.csv
│
└── sql/
    └── analysis_queries.sql
```

## How to Run

1. Install Python 3.12 or a compatible version.
2. Open the project folder in VS Code.
3. Create and activate a virtual environment.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Launch the dashboard:

```bash
streamlit run app.py
```

## Analytical Capabilities

The project demonstrates:
- SQL-based data aggregation
- Skill-frequency analysis
- Company-level benchmarking
- Job-family distribution
- Location and experience analysis
- Data validation and quality checks
- Interactive data visualisation

## Future Enhancements

- Add permitted, documented public job-posting observations.
- Separate real observations from synthetic demonstration data.
- Add source tracking and observation dates.
- Develop additional analytical comparisons.
- Improve reporting and export capabilities.

## Project Status

Working portfolio prototype.

