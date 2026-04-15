from dotenv import load_dotenv
import os
import pandas as pd
import mysql.connector

print("Before DB connection")

load_dotenv()

print("HOST:", os.getenv("DB_HOST"))
print("USER:", os.getenv("DB_USER"))
print("PASSWORD:", os.getenv("DB_PASSWORD"))
print("DB:", os.getenv("DB_NAME"))
# Connect to MySQL
try:
    print("Attempting DB connection...")

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    print("Connected to DB")

except Exception as e:
    print("ERROR OCCURRED:")
    print(e)
# Load CSV
df = pd.read_csv("data/processed/student_burnout_processed.csv")

print("CSV loaded:", df.shape)


# -----------------------------
# 1. Insert into dim_students
# -----------------------------
students_df = df[[
    "student_id", "department", "year_of_study", "residence_type"
]].drop_duplicates()

for _, row in students_df.iterrows():
    cursor.execute("""
        INSERT IGNORE INTO dim_students 
        (student_id, department, year_of_study, residence_type)
        VALUES (%s, %s, %s, %s)
    """, tuple(row))

conn.commit()
print("Inserted dim_students")


# -----------------------------
# 2. Insert into fact_daily_metrics
# -----------------------------
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO fact_daily_metrics (
            student_id, record_date,
            sleep_hours, study_hours, screen_time_hours,
            social_media_hours, physical_activity_minutes,
            class_attendance_hours, break_hours
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row["student_id"], row["record_date"],
        row["sleep_hours"], row["study_hours"], row["screen_time_hours"],
        row["social_media_hours"], row["physical_activity_minutes"],
        row["class_attendance_hours"], row["break_hours"]
    ))

conn.commit()
print("Inserted fact_daily_metrics")


# -----------------------------
# 3. Insert into fact_academic_load
# -----------------------------
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO fact_academic_load (
            student_id, record_date,
            assignments_due_count, tests_upcoming_count,
            submission_deadline_proximity,
            lab_hours, project_work_hours
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row["student_id"], row["record_date"],
        row["assignments_due_count"], row["tests_upcoming_count"],
        row["submission_deadline_proximity"],
        row["lab_hours"], row["project_work_hours"]
    ))

conn.commit()
print("Inserted fact_academic_load")


# -----------------------------
# 4. Insert into intelligence table
# -----------------------------
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO fact_intelligence_scores (
            student_id, record_date,
            sleep_deficit, workload_index, distraction_ratio, recovery_balance,
            productivity_score, burnout_risk_score,
            burnout_category, burnout_level_detailed,
            academic_performance_index
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row["student_id"], row["record_date"],
        row["sleep_deficit"], row["workload_index"],
        row["distraction_ratio"], row["recovery_balance"],
        row["productivity_score"], row["burnout_risk_score"],
        row["burnout_category"], row["burnout_level_detailed"],
        row["academic_performance_index"]
    ))

conn.commit()
print("Inserted fact_intelligence_scores")


cursor.close()
conn.close()

print("All data inserted successfully 🚀")