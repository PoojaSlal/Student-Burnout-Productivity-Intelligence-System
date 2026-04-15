import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


random.seed(42)
np.random.seed(42)


def ensure_directories() -> None:
    """Create required project directories if they do not exist."""
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("python", exist_ok=True)


def random_department() -> str:
    return random.choice(["CSE", "ECE", "EEE", "MECH", "CIVIL", "IT", "AIML", "DS"])


def random_residence() -> str:
    return random.choice(["Hosteller", "Day Scholar"])


def generate_students(num_students: int = 120) -> pd.DataFrame:
    """Generate student master data."""
    students = []

    for i in range(1, num_students + 1):
        students.append(
            {
                "student_id": 1000 + i,
                "department": random_department(),
                "year_of_study": random.randint(1, 4),
                "residence_type": random_residence(),
            }
        )

    return pd.DataFrame(students)


def format_date_messily(date_obj: datetime) -> str:
    """Return dates in mixed formats intentionally."""
    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%d/%m/%Y",
    ]
    return date_obj.strftime(random.choice(formats))


def capped_normal(mean: float, std: float, low: float, high: float, decimals: int = 1) -> float:
    """Generate a clipped normal-distribution value."""
    value = np.random.normal(mean, std)
    value = np.clip(value, low, high)
    return round(float(value), decimals)


def generate_daily_logs(
    students_df: pd.DataFrame,
    start_date: str = "2025-01-01",
    num_days: int = 90,
) -> pd.DataFrame:
    """Generate daily student activity and wellbeing logs."""
    rows = []
    start = datetime.strptime(start_date, "%Y-%m-%d")

    for _, student in students_df.iterrows():
        student_id = student["student_id"]
        year = student["year_of_study"]

        for day_offset in range(num_days):
            current_date = start + timedelta(days=day_offset)

            # Simulate slightly higher pressure during later semester days
            exam_pressure_factor = 1.0
            if day_offset >= 60:
                exam_pressure_factor = 1.25
            if day_offset >= 75:
                exam_pressure_factor = 1.45

            sleep_hours = capped_normal(6.5, 1.3, 3.0, 9.0)
            study_hours = capped_normal(4.5 * exam_pressure_factor, 1.8, 0.0, 12.0)
            screen_time_hours = capped_normal(6.0, 2.0, 1.0, 14.0)
            social_media_hours = round(min(screen_time_hours, max(0.0, np.random.normal(2.8, 1.2))), 1)
            physical_activity_minutes = int(np.clip(np.random.normal(30, 20), 0, 120))
            class_attendance_hours = capped_normal(3.5, 1.5, 0.0, 6.0)
            break_hours = capped_normal(1.8, 0.8, 0.0, 5.0)

            assignments_due_count = int(np.clip(np.random.poisson(1.3 * exam_pressure_factor), 0, 6))
            tests_upcoming_count = int(np.clip(np.random.poisson(0.8 * exam_pressure_factor), 0, 4))
            submission_deadline_proximity = random.randint(0, 14)
            lab_hours = capped_normal(1.5, 1.0, 0.0, 4.0)
            project_work_hours = capped_normal(1.7 + (0.2 * year), 1.1, 0.0, 6.0)

            # Wellbeing linked loosely to behavior
            stress_base = 4.5 + (study_hours / 3) + (assignments_due_count * 0.5) + (tests_upcoming_count * 0.8)
            stress_level = int(np.clip(round(np.random.normal(stress_base, 1.5)), 1, 10))

            fatigue_base = 4.0 + ((8 - sleep_hours) * 0.9) + (study_hours * 0.25)
            fatigue_level = int(np.clip(round(np.random.normal(fatigue_base, 1.4)), 1, 10))

            motivation_base = 6.5 - ((stress_level - 5) * 0.25) + (class_attendance_hours * 0.2)
            motivation_score = int(np.clip(round(np.random.normal(motivation_base, 1.5)), 1, 10))

            mood_base = 6.5 - ((stress_level - 5) * 0.4) - ((fatigue_level - 5) * 0.2) + (physical_activity_minutes / 60)
            mood_score = int(np.clip(round(np.random.normal(mood_base, 1.5)), 1, 10))

            rows.append(
                {
                    "student_id": student_id,
                    "department": student["department"],
                    "year_of_study": year,
                    "residence_type": student["residence_type"],
                    "record_date": format_date_messily(current_date),  # intentionally messy
                    "sleep_hours": sleep_hours,
                    "study_hours": study_hours,
                    "screen_time_hours": screen_time_hours,
                    "social_media_hours": social_media_hours,
                    "physical_activity_minutes": physical_activity_minutes,
                    "class_attendance_hours": class_attendance_hours,
                    "break_hours": break_hours,
                    "assignments_due_count": assignments_due_count,
                    "tests_upcoming_count": tests_upcoming_count,
                    "submission_deadline_proximity": submission_deadline_proximity,
                    "lab_hours": lab_hours,
                    "project_work_hours": project_work_hours,
                    "stress_level": stress_level,
                    "mood_score": mood_score,
                    "fatigue_level": fatigue_level,
                    "motivation_score": motivation_score,
                }
            )

    return pd.DataFrame(rows)


def introduce_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Introduce realistic missing values in selected columns."""
    df = df.copy()

    missing_config = {
        "sleep_hours": 0.06,
        "mood_score": 0.08,
        "class_attendance_hours": 0.05,
    }

    for column, frac in missing_config.items():
        idx = df.sample(frac=frac, random_state=42).index
        df.loc[idx, column] = np.nan

    return df


def introduce_inconsistent_stress_formats(df: pd.DataFrame) -> pd.DataFrame:
    """Convert some numeric stress values into messy strings."""
    df = df.copy()

    idx_1 = df.sample(frac=0.03, random_state=11).index
    idx_2 = df.sample(frac=0.02, random_state=22).index
    idx_3 = df.sample(frac=0.01, random_state=33).index

    df.loc[idx_1, "stress_level"] = df.loc[idx_1, "stress_level"].astype(str) + "/10"

    high_map = {8: "High", 9: "High", 10: "High"}
    df.loc[idx_2, "stress_level"] = df.loc[idx_2, "stress_level"].replace(high_map).astype(str)

    low_map = {1: "Low", 2: "Low", 3: "Low"}
    df.loc[idx_3, "stress_level"] = df.loc[idx_3, "stress_level"].replace(low_map).astype(str)

    return df


def introduce_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Introduce a few intentional outliers."""
    df = df.copy()

    outlier_indices = df.sample(frac=0.01, random_state=101).index.tolist()

    if len(outlier_indices) >= 5:
        df.loc[outlier_indices[:2], "sleep_hours"] = [1.5, 2.0]
        df.loc[outlier_indices[2:4], "study_hours"] = [14.0, 15.0]
        df.loc[outlier_indices[4:], "fatigue_level"] = 15

    return df


def introduce_contradictions(df: pd.DataFrame) -> pd.DataFrame:
    """Introduce a few contradictory records."""
    df = df.copy()

    idx = df.sample(frac=0.015, random_state=202).index

    df.loc[idx, "study_hours"] = 9.5
    df.loc[idx, "class_attendance_hours"] = 0.5
    df.loc[idx, "stress_level"] = random.choice([2, 3, "Low"])

    return df


def introduce_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Duplicate a small percentage of rows intentionally."""
    duplicate_rows = df.sample(frac=0.02, random_state=303)
    df_with_duplicates = pd.concat([df, duplicate_rows], ignore_index=True)
    return df_with_duplicates


def main() -> None:
    ensure_directories()

    students_df = generate_students(num_students=120)
    raw_df = generate_daily_logs(students_df=students_df, start_date="2025-01-01", num_days=90)

    raw_df = introduce_missing_values(raw_df)
    raw_df = introduce_inconsistent_stress_formats(raw_df)
    raw_df = introduce_outliers(raw_df)
    raw_df = introduce_contradictions(raw_df)
    raw_df = introduce_duplicates(raw_df)

    students_output_path = "data/raw/students.csv"
    logs_output_path = "data/raw/student_burnout_raw.csv"

    students_df.to_csv(students_output_path, index=False)
    raw_df.to_csv(logs_output_path, index=False)

    print("Dataset generation complete.")
    print(f"Students file saved to: {students_output_path}")
    print(f"Raw logs file saved to: {logs_output_path}")
    print(f"Students rows: {len(students_df)}")
    print(f"Raw dataset rows: {len(raw_df)}")
    print("\nSample:")
    print(raw_df.head())


if __name__ == "__main__":
    main()