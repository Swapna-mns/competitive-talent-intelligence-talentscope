
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

CHART_COLORS = [
    "#8B5CF6",
    "#06B6D4",
    "#F97316",
    "#EC4899",
    "#10B981",
    "#F59E0B",
    "#6366F1",
    "#EF4444"
]
template="plotly_white"
hover_data=["Records"]
hover_data=["Mentions"]
hover_data=["Records"]

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = CHART_COLORS

# Modern multicolour chart theme
CHART_COLORS = [
    "#8B5CF6",  # Purple
    "#06B6D4",  # Cyan
    "#F97316",  # Orange
    "#EC4899",  # Pink
    "#10B981",  # Emerald
    "#F59E0B",  # Amber
    "#6366F1",  # Indigo
    "#EF4444"   # Coral
]

line_shape="spline",
line_dash="solid",

line=dict(color="#8B5CF6", width=3),

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = CHART_COLORS

st.set_page_config(
    page_title="TalentScope",
    page_icon="📊",
    layout="wide"
)

BASE_FOLDER = Path(__file__).parent
DB_PATH = BASE_FOLDER / "talentscope.db"
CSV_PATH = BASE_FOLDER / "data" / "job_postings_synthetic.csv"


@st.cache_data
def load_data():
    # Read from SQLite if the database exists; otherwise use the CSV.
    if DB_PATH.exists():
        connection = sqlite3.connect(DB_PATH)
        data = pd.read_sql_query(
            "SELECT * FROM job_postings",
            connection
        )
        connection.close()
    else:
        data = pd.read_csv(CSV_PATH)

    data["posted_date"] = pd.to_datetime(
        data["posted_date"], errors="coerce"
    )

    data["skills_list"] = data["skills"].fillna("").apply(
        lambda value: [
            skill.strip()
            for skill in value.split(";")
            if skill.strip()
        ]
    )

    return data


df = load_data()


st.title("TalentScope")

st.subheader(
    "Competitive Talent Market Intelligence & Skills Benchmarking Platform"
)

st.caption(
    "An interactive platform for workforce trends, skill analysis and competitive benchmarking."
)

st.info(
    "Dataset: 300 synthetic job-posting records created for analytical demonstration and benchmarking."
)


# Sidebar filters
with st.sidebar:
    st.header("Explore the dataset")

    companies = sorted(df["company"].dropna().unique())
    selected_companies = st.multiselect(
        "Companies", companies, default=companies
    )

    industries = sorted(df["industry"].dropna().unique())
    selected_industries = st.multiselect(
        "Industries", industries, default=industries
    )

    roles = sorted(df["job_title"].dropna().unique())
    selected_roles = st.multiselect(
        "Job roles", roles, default=roles
    )

    locations = sorted(df["location"].dropna().unique())
    selected_locations = st.multiselect(
        "Locations", locations, default=locations
    )

# Apply filters
filtered = df[
    df["company"].isin(selected_companies)
    & df["industry"].isin(selected_industries)
    & df["job_title"].isin(selected_roles)
    & df["location"].isin(selected_locations)
].copy()

if filtered.empty:
    st.warning(
        "No records match these filters. Select at least one option in each filter."
    )
    st.stop()

# Expand skills into individual rows
skill_rows = []

for _, row in filtered.iterrows():
    for skill in row["skills_list"]:
        skill_rows.append({
            "skill": skill,
            "company": row["company"],
            "job_title": row["job_title"]
        })

skill_df = pd.DataFrame(
    skill_rows,
    columns=["skill", "company", "job_title"]
)

# KPI cards
c1, c2, c3, c4 = st.columns(4)

c1.metric("Illustrative job records", f"{len(filtered):,}")
c2.metric("Companies represented", f"{filtered['company'].nunique():,}")
c3.metric("Job families", f"{filtered['job_title'].nunique():,}")
c4.metric(
    "Distinct skills",
    f"{skill_df['skill'].nunique():,}" if not skill_df.empty else "0"
)

st.divider()

# Job family and industry charts
left, right = st.columns(2)

with left:
    st.markdown("### Records by job family")

    role_counts = (
        filtered["job_title"]
        .value_counts()
        .rename_axis("Job family")
        .reset_index(name="Records")
    )

    fig = px.bar(
    role_counts,
    x="Records",
    y="Job family",
    orientation="h",
    color="Job family",
    title="Synthetic records by job family"

    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("### Records by industry")

    industry_counts = (
        filtered["industry"]
        .value_counts()
        .rename_axis("Industry")
        .reset_index(name="Records")
    )

    fig = px.pie(
    industry_counts,
    names="Industry",
    values="Records",
    hole=0.45,
    color="Industry",
    title="Synthetic records by industry"
)
    st.plotly_chart(fig, use_container_width=True)

# Skills and location charts
left, right = st.columns(2)

with left:
    st.markdown("### Most frequently listed skills")

    if not skill_df.empty:
        skill_counts = (
            skill_df["skill"]
            .value_counts()
            .head(12)
            .rename_axis("Skill")
            .reset_index(name="Mentions")
        )

        fig = px.bar(
        skill_counts.sort_values("Mentions"),
        x="Mentions",
        y="Skill",
        orientation="h",
        color="Skill",
        title="Skill mentions in selected records"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No skill information available for these records.")

with right:
    st.markdown("### Location distribution")

    loc_counts = (
        filtered["location"]
        .value_counts()
        .rename_axis("Location")
        .reset_index(name="Records")
    )

    fig = px.bar(
    loc_counts,
    x="Location",
    y="Records",
    color="Location",
    title="Synthetic records by location"

    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# New feature 1: Company skill benchmarking
st.markdown("## Company skill benchmarking")

st.write(
    "Explore the most frequently listed skills for an individual "
    "company in the selected dataset."
)

if not skill_df.empty:
    available_companies = sorted(skill_df["company"].unique())

    benchmark_company = st.selectbox(
        "Select a company to benchmark",
        available_companies
    )

    company_skills = (
        skill_df[skill_df["company"] == benchmark_company]["skill"]
        .value_counts()
        .head(10)
        .rename_axis("Skill")
        .reset_index(name="Mentions")
    )

    fig = px.bar(
    company_skills.sort_values("Mentions"),
    x="Mentions",
    y="Skill",
    orientation="h",
    color="Skill",
    title=f"Top listed skills: {benchmark_company}"
)

    st.plotly_chart(fig, use_container_width=True)

else:
    st.write("No skill information available for benchmarking.")


# New feature: Cross-company skill benchmarking heatmap
st.markdown("## Cross-company skill benchmarking")

st.write(
    "Compare frequently listed skills across companies "
    "using the selected dataset."
)

if not skill_df.empty:

    top_skills = (
        skill_df["skill"]
        .value_counts()
        .head(8)
        .index
    )

    benchmark_data = skill_df[
        skill_df["skill"].isin(top_skills)
    ]

    skill_matrix = pd.crosstab(
        benchmark_data["skill"],
        benchmark_data["company"]
    )

    fig = px.imshow(
        skill_matrix,
        labels={
            "x": "Company",
            "y": "Skill",
            "color": "Skill mentions"
        },
        title="Skill frequency across companies",
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Turbo"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.write("No skill data available for comparison.")

# New feature 2: Hiring demand trend
st.markdown("## Hiring-demand trend")

st.write(
    "Monthly distribution of synthetic job-posting records. "
    "This is an illustrative trend, not a real market forecast."
)

monthly_data = filtered.dropna(subset=["posted_date"]).copy()

if not monthly_data.empty:
    monthly_data["month"] = (
        monthly_data["posted_date"].dt.to_period("M").astype(str)
    )

    monthly_counts = (
        monthly_data.groupby("month")
        .size()
        .reset_index(name="Records")
        .sort_values("month")
    )

    fig = px.line(
        monthly_counts,
        x="month",
        y="Records",
        markers=True,
        title="Monthly synthetic posting records"
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.write("No valid posting dates are available for this selection.")


# Experience-level benchmarking
st.markdown("## Experience-level benchmarking")

st.write(
    "Compare the experience requirements across the selected "
    "synthetic job-posting records."
)

if "experience_required" in filtered.columns:

    experience_counts = (
        filtered["experience_required"]
        .value_counts()
        .rename_axis("Experience level")
        .reset_index(name="Records")
    )

    fig = px.bar(
    experience_counts,
    x="Experience level",
    y="Records",
    text="Records",
    color="Experience level",
    title="Distribution of experience requirements"
)

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Experience requirement data is unavailable.")


# Executive insights
st.markdown("## Executive insights")

st.caption(
    "Automatically generated findings from the selected synthetic dataset."
)

insight_columns = st.columns(5)

# Company with the highest record count
company_counts = filtered["company"].value_counts()

# Most frequently listed skill
if not skill_df.empty:
    top_skill = skill_df["skill"].value_counts().idxmax()
else:
    top_skill = "N/A"

# Most represented job family
top_role = filtered["job_title"].value_counts().idxmax()

# Most represented location
top_location = filtered["location"].value_counts().idxmax()

# Most common experience category
top_experience = filtered["experience_required"].value_counts().idxmax()

insight_columns[0].metric(
    "Top company",
    company_counts.idxmax()
)

insight_columns[1].metric(
    "Top skill",
    top_skill
)

insight_columns[2].metric(
    "Leading job family",
    top_role
)

insight_columns[3].metric(
    "Leading location",
    top_location
)

insight_columns[4].metric(
    "Common experience",
    top_experience
)

# Company comparison
st.markdown("## Company comparison")

company_summary = (
    filtered.groupby(["company", "industry"], as_index=False)
    .agg(
        illustrative_records=("record_id", "count"),
        job_families=("job_title", "nunique"),
        locations=("location", "nunique")
    )
    .sort_values("illustrative_records", ascending=False)
)

st.dataframe(
    company_summary,
    use_container_width=True,
    hide_index=True
)

# Evidence table
st.markdown("## Evidence table")

display_cols = [
    "record_id",
    "company",
    "industry",
    "job_title",
    "location",
    "experience_required",
    "skills",
    "posted_date",
    "source_type"
]

st.dataframe(
    filtered[display_cols].sort_values(
        "posted_date", ascending=False
    ),
    use_container_width=True,
    hide_index=True
)

# Data quality checks
st.markdown("## Data quality checks")

q1, q2, q3 = st.columns(3)

q1.metric(
    "Duplicate record IDs",
    int(filtered["record_id"].duplicated().sum())
)

q2.metric(
    "Missing job titles",
    int(filtered["job_title"].isna().sum())
)

q3.metric(
    "Missing posting dates",
    int(filtered["posted_date"].isna().sum())
)

# Download filtered records
st.download_button(
    "Download filtered records as CSV",
    data=filtered[display_cols].to_csv(index=False).encode("utf-8"),
    file_name="talentscope_filtered_records.csv",
    mime="text/csv"
)

st.divider()

st.caption(
    "TalentScope AI | Portfolio prototype | Synthetic data only | "
    "Not a live job-market feed | No individual profiling"
)
