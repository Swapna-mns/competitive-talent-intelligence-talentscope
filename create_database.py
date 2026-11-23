
import pandas as pd
import sqlite3
from pathlib import Path

# Locate the project files
base_folder = Path(__file__).parent
csv_path = base_folder / "data" / "job_postings_synthetic.csv"
db_path = base_folder / "talentscope.db"

# Load the synthetic dataset
df = pd.read_csv(csv_path)

# Connect to SQLite and create the table
connection = sqlite3.connect(db_path)

df.to_sql(
    "job_postings",
    connection,
    if_exists="replace",
    index=False
)

# Verify the database
result = pd.read_sql_query(
    "SELECT COUNT(*) AS total_records FROM job_postings",
    connection
)

print("Database created successfully!")
print(result)

connection.close()
