
import sqlite3
import pandas as pd
from pathlib import Path

# Connect to the project database
db_path = Path(__file__).parent / "talentscope.db"
connection = sqlite3.connect(db_path)

# 1. Company-wise job records
company_data = pd.read_sql_query("""
    SELECT company, COUNT(*) AS total_jobs
    FROM job_postings
    GROUP BY company
    ORDER BY total_jobs DESC
""", connection)

print("\n--- COMPANY-WISE RECORDS ---")
print(company_data.to_string(index=False))

# 2. Most common job roles
role_data = pd.read_sql_query("""
    SELECT job_title, COUNT(*) AS total_jobs
    FROM job_postings
    GROUP BY job_title
    ORDER BY total_jobs DESC
""", connection)

print("\n--- JOB ROLE DISTRIBUTION ---")
print(role_data.to_string(index=False))

# 3. Location-wise records
location_data = pd.read_sql_query("""
    SELECT location, COUNT(*) AS total_jobs
    FROM job_postings
    GROUP BY location
    ORDER BY total_jobs DESC
""", connection)

print("\n--- LOCATION DISTRIBUTION ---")
print(location_data.to_string(index=False))

# 4. Experience requirement
experience_data = pd.read_sql_query("""
    SELECT experience_required, COUNT(*) AS total_jobs
    FROM job_postings
    GROUP BY experience_required
    ORDER BY total_jobs DESC
""", connection)

print("\n--- EXPERIENCE REQUIREMENTS ---")
print(experience_data.to_string(index=False))


# 5. Most frequently mentioned skills
skill_data = pd.read_sql_query("""
    WITH RECURSIVE split_skills(rest, skill) AS (
        SELECT skills || ';', ''
        FROM job_postings

        UNION ALL

        SELECT
            substr(rest, instr(rest, ';') + 1),
            trim(substr(rest, 1, instr(rest, ';') - 1))
        FROM split_skills
        WHERE rest <> ''
    )
    SELECT
        skill,
        COUNT(*) AS skill_mentions
    FROM split_skills
    WHERE skill <> ''
    GROUP BY skill
    ORDER BY skill_mentions DESC
""", connection)

print("\n--- MOST FREQUENTLY MENTIONED SKILLS ---")
print(skill_data.to_string(index=False))


# 6. Company-wise skill benchmarking
company_skill_data = pd.read_sql_query("""
WITH RECURSIVE split_skills(company, rest, skill) AS (
    SELECT company, skills || ';', ''
    FROM job_postings

    UNION ALL

    SELECT
        company,
        substr(rest, instr(rest, ';') + 1),
        trim(substr(rest, 1, instr(rest, ';') - 1))
    FROM split_skills
    WHERE rest <> ''
)
SELECT
    company,
    skill,
    COUNT(*) AS mentions
FROM split_skills
WHERE skill <> ''
GROUP BY company, skill
ORDER BY company, mentions DESC
""", connection)

print("\n--- COMPANY-WISE SKILL BENCHMARKING ---")
print(company_skill_data.to_string(index=False))


# 7. Top 3 skills for each company
top_skills = company_skill_data.copy()

top_skills["skill_rank"] = (
    top_skills.groupby("company")["mentions"]
    .rank(method="first", ascending=False)
)

top_three_skills = top_skills[
    top_skills["skill_rank"] <= 3
].copy()

print("\n--- TOP 3 SKILLS BY COMPANY ---")
print(
    top_three_skills[
        ["company", "skill", "mentions"]
    ].to_string(index=False)
)


connection.close()
print("\nAnalysis completed successfully!")
