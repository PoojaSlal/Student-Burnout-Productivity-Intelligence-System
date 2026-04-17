from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

print("Script started")

load_dotenv()

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

print("Loading environment variables...")
print("HOST:", db_host)
print("USER:", db_user)
print("DB:", db_name)

print("Building SQLAlchemy engine...")

encoded_password = quote_plus(db_password)

engine = create_engine(
    f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}/{db_name}",
    pool_pre_ping=True
)

print("Engine created")

# Load CSV
df = pd.read_csv("data/processed/student_burnout_processed.csv")
print("CSV loaded:", df.shape)

# Make sure record_date is proper date
df["record_date"] = pd.to_datetime(df["record_date"]).dt.date

# -----------------------------
# 1. dim_students
# -----------------------------
students_df = df[
    ["student_id", "department", "year_of_study", "residence_type"]
].drop_duplicates()

# Clear and reload
with engine.begin() as conn:
    conn.execute(text("DELETE FROM fact_intelligence_scores"))
    conn.execute(text("DELETE FROM fact_academic_load"))
    conn.execute(text("DELETE FROM fact_daily_metrics"))
    conn.execute(text("DELETE FROM dim_students"))

students_df.to_sql(
    "dim_students",
    con=engine,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=1000
)
print("Inserted dim_students")

# -----------------------------
# 2. fact_daily_metrics
# -----------------------------
daily_df = df[
    [
        "student_id",
        "record_date",
        "sleep_hours",
        "study_hours",
        "screen_time_hours",
        "social_media_hours",
        "physical_activity_minutes",
        "class_attendance_hours",
        "break_hours",
    ]
]

daily_df.to_sql(
    "fact_daily_metrics",
    con=engine,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=1000
)
print("Inserted fact_daily_metrics")

# -----------------------------
# 3. fact_academic_load
# -----------------------------
academic_df = df[
    [
        "student_id",
        "record_date",
        "assignments_due_count",
        "tests_upcoming_count",
        "submission_deadline_proximity",
        "lab_hours",
        "project_work_hours",
    ]
]

academic_df.to_sql(
    "fact_academic_load",
    con=engine,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=1000
)
print("Inserted fact_academic_load")

# -----------------------------
# 4. fact_intelligence_scores
# -----------------------------
intelligence_df = df[
    [
        "student_id",
        "record_date",
        "sleep_deficit",
        "workload_index",
        "distraction_ratio",
        "recovery_balance",
        "productivity_score",
        "burnout_risk_score",
        "burnout_category",
        "burnout_level_detailed",
        "primary_trigger",
        "suggested_action",
        "academic_performance_index",
    ]
]

intelligence_df.to_sql(
    "fact_intelligence_scores",
    con=engine,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=1000
)
print("Inserted fact_intelligence_scores")

print("All data inserted successfully!")