import os
import pandas as pd
import numpy as np


# Ensure output folder exists
os.makedirs("data/cleaned", exist_ok=True)


# -----------------------------
# 1. Load raw dataset
# -----------------------------
df = pd.read_csv("data/raw/student_burnout_raw.csv")

print("Initial Shape:", df.shape)


# -----------------------------
# 2. Handle Date Formats
# -----------------------------
def parse_dates_flexibly(date_val):
    if pd.isna(date_val):
        return pd.NaT

    date_val = str(date_val).strip()

    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%d/%m/%Y",
    ]

    for fmt in formats:
        try:
            return pd.to_datetime(date_val, format=fmt)
        except ValueError:
            continue

    try:
        return pd.to_datetime(date_val, dayfirst=True)
    except Exception:
        try:
            return pd.to_datetime(date_val)
        except Exception:
            return pd.NaT


df["record_date"] = df["record_date"].apply(parse_dates_flexibly)

print("Unparsed dates before drop:", df["record_date"].isna().sum())

# Drop only truly invalid dates
df = df.dropna(subset=["record_date"])


# -----------------------------
# 3. Clean stress_level column
# -----------------------------
def clean_stress(val):
    if pd.isna(val):
        return np.nan

    val = str(val).strip()

    if "/10" in val:
        try:
            return float(val.split("/")[0])
        except ValueError:
            return np.nan

    if val.lower() == "high":
        return 9.0
    if val.lower() == "low":
        return 3.0

    try:
        return float(val)
    except ValueError:
        return np.nan


df["stress_level"] = df["stress_level"].apply(clean_stress)


# -----------------------------
# 4. Ensure numeric columns are clean
# -----------------------------
numeric_cols = [
    "sleep_hours",
    "study_hours",
    "screen_time_hours",
    "social_media_hours",
    "physical_activity_minutes",
    "class_attendance_hours",
    "break_hours",
    "assignments_due_count",
    "tests_upcoming_count",
    "submission_deadline_proximity",
    "lab_hours",
    "project_work_hours",
    "stress_level",
    "mood_score",
    "fatigue_level",
    "motivation_score",
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# -----------------------------
# 5. Handle Missing Values
# -----------------------------
df["sleep_hours"] = df["sleep_hours"].fillna(df["sleep_hours"].median())
df["study_hours"] = df["study_hours"].fillna(df["study_hours"].median())
df["mood_score"] = df["mood_score"].fillna(df["mood_score"].median())
df["class_attendance_hours"] = df["class_attendance_hours"].fillna(
    df["class_attendance_hours"].mean()
)
df["stress_level"] = df["stress_level"].fillna(df["stress_level"].median())


# -----------------------------
# 6. Remove Duplicates
# -----------------------------
df = df.drop_duplicates(subset=["student_id", "record_date"])


# -----------------------------
# 7. Fix Outliers (Capping)
# -----------------------------
df["sleep_hours"] = df["sleep_hours"].clip(3, 9)
df["study_hours"] = df["study_hours"].clip(0, 12)
df["screen_time_hours"] = df["screen_time_hours"].clip(1, 14)
df["fatigue_level"] = df["fatigue_level"].clip(1, 10)
df["stress_level"] = df["stress_level"].clip(1, 10)
df["mood_score"] = df["mood_score"].clip(1, 10)
df["motivation_score"] = df["motivation_score"].clip(1, 10)
df["class_attendance_hours"] = df["class_attendance_hours"].clip(0, 6)
df["social_media_hours"] = df["social_media_hours"].clip(0, 8)
df["physical_activity_minutes"] = df["physical_activity_minutes"].clip(0, 120)


# -----------------------------
# 8. Final Check
# -----------------------------
print("After Cleaning Shape:", df.shape)
print("\nMissing Values:\n", df.isnull().sum())


# -----------------------------
# 9. Save Cleaned Data
# -----------------------------
output_path = "data/cleaned/student_burnout_cleaned.csv"
df.to_csv(output_path, index=False)

print("\nCleaned dataset saved successfully.")
print(f"Saved to: {output_path}")