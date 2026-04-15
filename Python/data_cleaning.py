import pandas as pd
import numpy as np
import os


# Ensure output folder exists
os.makedirs("data/cleaned", exist_ok=True)


# Load raw dataset
df = pd.read_csv("data/raw/student_burnout_raw.csv")


print("Initial Shape:", df.shape)


# -----------------------------
# 1. Handle Date Formats
# -----------------------------
df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")


# -----------------------------
# 2. Clean stress_level column
# -----------------------------
def clean_stress(val):
    if pd.isna(val):
        return np.nan

    val = str(val).strip()

    if "/10" in val:
        return float(val.split("/")[0])

    if val.lower() == "high":
        return 9
    if val.lower() == "low":
        return 3

    try:
        return float(val)
    except:
        return np.nan


df["stress_level"] = df["stress_level"].apply(clean_stress)


# -----------------------------
# 3. Handle Missing Values
# -----------------------------
df["sleep_hours"].fillna(df["sleep_hours"].median(), inplace=True)
df["mood_score"].fillna(df["mood_score"].median(), inplace=True)
df["class_attendance_hours"] = df["class_attendance_hours"].fillna(
    df["class_attendance_hours"].mean()
)


# -----------------------------
# 4. Remove Duplicates
# -----------------------------
df.drop_duplicates(subset=["student_id", "record_date"], inplace=True)


# -----------------------------
# 5. Fix Outliers (Capping)
# -----------------------------
df["sleep_hours"] = df["sleep_hours"].clip(3, 9)
df["study_hours"] = df["study_hours"].clip(0, 12)
df["screen_time_hours"] = df["screen_time_hours"].clip(1, 14)
df["fatigue_level"] = df["fatigue_level"].clip(1, 10)


# -----------------------------
# 6. Ensure numeric columns are clean
# -----------------------------
numeric_cols = [
    "sleep_hours", "study_hours", "screen_time_hours",
    "social_media_hours", "physical_activity_minutes",
    "class_attendance_hours", "break_hours",
    "assignments_due_count", "tests_upcoming_count",
    "submission_deadline_proximity", "lab_hours",
    "project_work_hours", "stress_level", "mood_score",
    "fatigue_level", "motivation_score"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# -----------------------------
# 7. Final Check
# -----------------------------
print("After Cleaning Shape:", df.shape)
print("\nMissing Values:\n", df.isnull().sum())


# -----------------------------
# 8. Save Cleaned Data
# -----------------------------
df.to_csv("data/cleaned/student_burnout_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully.")