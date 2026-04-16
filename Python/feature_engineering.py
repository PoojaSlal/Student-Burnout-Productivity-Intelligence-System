import os
import pandas as pd
import numpy as np


# Ensure output folder exists
os.makedirs("data/processed", exist_ok=True)


# -----------------------------
# 1. Load cleaned dataset
# -----------------------------
df = pd.read_csv("data/cleaned/student_burnout_cleaned.csv")

print("Initial Shape:", df.shape)


# -----------------------------
# 2. Sleep Deficit
# -----------------------------
df["sleep_deficit"] = (8 - df["sleep_hours"]).clip(lower=0)


# -----------------------------
# 3. Workload Index
# -----------------------------
df["workload_index"] = (
    df["study_hours"] * 0.30
    + df["lab_hours"] * 0.15
    + df["project_work_hours"] * 0.20
    + df["assignments_due_count"] * 1.5
    + df["tests_upcoming_count"] * 2.0
)


# -----------------------------
# 4. Distraction Ratio
# -----------------------------
df["distraction_ratio"] = np.where(
    df["screen_time_hours"] > 0,
    df["social_media_hours"] / df["screen_time_hours"],
    0
)
df["distraction_ratio"] = df["distraction_ratio"].clip(0, 1)


# -----------------------------
# 5. Recovery Balance
# -----------------------------
df["recovery_balance"] = (
    df["sleep_hours"] * 0.5
    + df["break_hours"] * 0.2
    + (df["physical_activity_minutes"] / 60) * 0.3
)


# -----------------------------
# 6. Deadline Pressure Score
# -----------------------------
df["deadline_pressure_score"] = np.where(
    df["submission_deadline_proximity"] <= 2, 10,
    np.where(
        df["submission_deadline_proximity"] <= 5, 7,
        np.where(df["submission_deadline_proximity"] <= 10, 4, 2)
    )
)


# -----------------------------
# 7. Scaling function
# -----------------------------
def min_max_scale(series: pd.Series) -> pd.Series:
    min_val = series.min()
    max_val = series.max()

    if max_val == min_val:
        return pd.Series([0] * len(series), index=series.index)

    return ((series - min_val) / (max_val - min_val)) * 100


# -----------------------------
# 8. Scale features
# -----------------------------
df["sleep_deficit_scaled"] = min_max_scale(df["sleep_deficit"])
df["workload_index_scaled"] = min_max_scale(df["workload_index"])
df["distraction_ratio_scaled"] = df["distraction_ratio"] * 100
df["recovery_balance_scaled"] = min_max_scale(df["recovery_balance"])
df["deadline_pressure_scaled"] = min_max_scale(df["deadline_pressure_score"])
df["attendance_scaled"] = min_max_scale(df["class_attendance_hours"])
df["motivation_scaled"] = min_max_scale(df["motivation_score"])
df["fatigue_scaled"] = min_max_scale(df["fatigue_level"])
df["stress_scaled"] = min_max_scale(df["stress_level"])
df["mood_scaled"] = min_max_scale(df["mood_score"])


# -----------------------------
# 9. Productivity Score
# -----------------------------
df["productivity_score"] = (
    0.22 * min_max_scale(df["study_hours"])
    + 0.20 * df["attendance_scaled"]
    + 0.18 * df["motivation_scaled"]
    + 0.15 * df["recovery_balance_scaled"]
    - 0.10 * df["fatigue_scaled"]
    - 0.08 * df["distraction_ratio_scaled"]
    - 0.07 * df["workload_index_scaled"]
)
df["productivity_score"] = df["productivity_score"].clip(0, 100)


# -----------------------------
# 10. Burnout Risk Score
# -----------------------------
df["burnout_risk_score"] = (
    0.17 * df["sleep_deficit_scaled"]
    + 0.20 * df["stress_scaled"]
    + 0.16 * df["fatigue_scaled"]
    + 0.16 * df["workload_index_scaled"]
    + 0.10 * df["deadline_pressure_scaled"]
    + 0.08 * df["distraction_ratio_scaled"]
    - 0.08 * df["recovery_balance_scaled"]
    - 0.05 * df["mood_scaled"]
)
df["burnout_risk_score"] = df["burnout_risk_score"].clip(0, 100)


# -----------------------------
# 11. Basic Burnout Category
# -----------------------------
def categorize_burnout(score: float) -> str:
    if score < 40:
        return "Low"
    elif score < 70:
        return "Moderate"
    return "High"


df["burnout_category"] = df["burnout_risk_score"].apply(categorize_burnout)


# -----------------------------
# 11B. Detailed Burnout Levels
# -----------------------------
def detailed_burnout_level(score: float) -> str:
    if score < 20:
        return "Very Low"
    elif score < 40:
        return "Low"
    elif score < 55:
        return "Moderate"
    elif score < 70:
        return "Elevated"
    elif score < 85:
        return "High"
    else:
        return "Critical"


df["burnout_level_detailed"] = df["burnout_risk_score"].apply(detailed_burnout_level)


# -----------------------------
# 12. Primary Trigger Analysis
# -----------------------------
trigger_columns = [
    "sleep_deficit_scaled",
    "stress_scaled",
    "fatigue_scaled",
    "workload_index_scaled",
    "deadline_pressure_scaled",
    "distraction_ratio_scaled"
]

trigger_name_map = {
    "sleep_deficit_scaled": "Sleep Deficit",
    "stress_scaled": "Stress",
    "fatigue_scaled": "Fatigue",
    "workload_index_scaled": "Workload",
    "deadline_pressure_scaled": "Deadline Pressure",
    "distraction_ratio_scaled": "Distraction"
}

df["primary_trigger_raw"] = df[trigger_columns].idxmax(axis=1)
df["primary_trigger"] = df["primary_trigger_raw"].map(trigger_name_map)


# -----------------------------
# 13. Suggested Action
# -----------------------------
action_map = {
    "Sleep Deficit": "Recommend sleep recovery support",
    "Stress": "Recommend stress counseling",
    "Fatigue": "Recommend temporary workload reduction",
    "Workload": "Recommend workload balancing",
    "Deadline Pressure": "Recommend deadline planning support",
    "Distraction": "Recommend distraction management"
}

df["suggested_action"] = df["primary_trigger"].map(action_map)


# -----------------------------
# 14. Limit actions to at-risk students
# -----------------------------
risk_levels = ["Elevated", "High", "Critical"]

df.loc[~df["burnout_level_detailed"].isin(risk_levels), "primary_trigger"] = np.nan
df.loc[~df["burnout_level_detailed"].isin(risk_levels), "suggested_action"] = np.nan


# -----------------------------
# 15. Academic Performance Index
# -----------------------------
df["academic_performance_index"] = (
    0.35 * df["productivity_score"]
    + 0.25 * df["attendance_scaled"]
    + 0.20 * df["motivation_scaled"]
    - 0.10 * df["fatigue_scaled"]
    - 0.10 * df["burnout_risk_score"]
)
df["academic_performance_index"] = df["academic_performance_index"].clip(0, 100)


# -----------------------------
# 16. Round outputs
# -----------------------------
round_cols = [
    "sleep_deficit",
    "workload_index",
    "distraction_ratio",
    "recovery_balance",
    "productivity_score",
    "burnout_risk_score",
    "academic_performance_index",
]

df[round_cols] = df[round_cols].round(2)


# -----------------------------
# 17. Cleanup helper columns
# -----------------------------
df = df.drop(columns=["primary_trigger_raw"])


# -----------------------------
# 18. Final Check
# -----------------------------
print("Processed Shape:", df.shape)
print("\nBurnout Category:\n", df["burnout_category"].value_counts())
print("\nDetailed Levels:\n", df["burnout_level_detailed"].value_counts())
print("\nPrimary Trigger Sample:\n", df[["burnout_level_detailed", "primary_trigger", "suggested_action"]].head(10))


# -----------------------------
# 19. Save
# -----------------------------
output_path = "data/processed/student_burnout_processed.csv"
df.to_csv(output_path, index=False)

print("\nProcessed dataset saved successfully.")
print(f"Saved to: {output_path}")