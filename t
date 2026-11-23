# Competitive Talent Intelligence & Workforce Benchmarking System

A data-driven talent intelligence platform designed to analyze job market trends, workforce demand, hiring patterns, industry distribution, and competitive skills across organizations.

## Project Overview

The Competitive Talent Intelligence & Workforce Benchmarking System transforms job-market data into meaningful insights through interactive analytics and structured data analysis.

The platform helps users understand:
- Job demand across companies and industries.
- Distribution of job roles and job families.
- Most frequently requested technical and professional skills.
- Hiring trends across different locations.
- Workforce and industry benchmarking patterns.
- Competitive talent demand across organizations.

## Key Features

- **Company Benchmarking:** Compare job postings across organizations.
- **Job Family Analysis:** Explore hiring demand across different job categories.
- **Industry Insights:** Analyze industry-wise job distribution.
- **Skills Intelligence:** Identify frequently requested skills.
- **Location Analysis:** Understand geographic hiring patterns.
- **Interactive Dashboard:** Explore analytical insights through visualizations.
- **SQL-Based Analysis:** Perform structured queries to extract business insights.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Database | SQLite |
| Data Analysis | Pandas, NumPy |
| Visualization | Plotly |
| Dashboard | Streamlit |
| Query Language | SQL |

## Project Structure

```text
competitive-talent-intelligence/
│
├── app.py
├── analysis.py
├── create_database.py
├── requirements.txt
├── README.md
│
├── data/
│   └── job_postings_synthetic.csv
│
└── sql/
    └── analysis_queries.sql
```

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/Swapna-mns/competitive-talent-intelligence.git
```

### 2. Navigate to the project folder

```bash
cd competitive-talent-intelligence
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows:

```bash
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Prepare the database

```bash
python create_database.py
```

### 7. Run the application

```bash
streamlit run app.py
```

## Business Value

This project demonstrates how data analytics and workforce intelligence can support:

- Competitive hiring analysis.
- Skills-demand identification.
- Industry benchmarking.
- Workforce planning.
- Data-driven talent strategy.

## Dataset

This project uses synthetic job-posting data for analytical and demonstration purposes. It does not represent live hiring information or actual company workforce records.



---

*Developed as a practical data analytics and talent intelligence project.*
