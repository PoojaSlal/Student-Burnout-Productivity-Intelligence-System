# Student Burnout & Productivity Intelligence System

A data analytics project designed to analyze student behavioral and academic patterns, estimate burnout risk, measure productivity, and generate actionable intervention insights through Python, SQL, and Power BI.

---

## Overview

Student burnout is influenced by multiple factors such as sleep deficit, workload, stress, fatigue, screen distraction, and recovery balance.  
This project builds a complete analytics pipeline that simulates realistic student data, cleans and transforms it, engineers meaningful features, computes burnout and productivity scores, stores the data in a relational database, and visualizes insights using an interactive Power BI dashboard.

The system is designed not just to identify extreme burnout, but also to detect students in elevated risk states for early intervention.

---

## Problem Statement

Institutions often lack a structured system to monitor student wellbeing and productivity using behavioral and academic indicators.

This project addresses questions such as:

- Which students are at burnout risk?
- How do workload and recovery affect productivity?
- Which behavioral factors are most associated with burnout?
- How can moderate-risk students be identified before escalation?

---

## Key Features

- Simulated semester-style student behavioral dataset
- Realistic data imperfections:
  - missing values
  - inconsistent formats
  - outliers
  - duplicates
- Data cleaning and preprocessing pipeline
- Feature engineering for behavioral and workload metrics
- Explainable burnout scoring model
- Productivity scoring model
- Hierarchical burnout classification
- Normalized SQL database design
- Power BI dashboard with intervention-focused insights

---

## Tech Stack

- **Python**
- **Pandas**
- **NumPy**
- **MySQL**
- **SQLAlchemy / PyMySQL**
- **Power BI**
- **Git & GitHub**

---

## Project Pipeline

```text
Raw Data Generation
    ↓
Data Cleaning & Preprocessing
    ↓
Feature Engineering
    ↓
Burnout & Productivity Scoring
    ↓
SQL Database Loading
    ↓
Power BI Dashboarding

## Dataset Design

The dataset is built as a daily time-series structure:

- 120 students  
- 90 days  
- 10,000+ records  

Each row represents:
- one student  
- on one day  

### Core Raw Fields

#### Student attributes
- `student_id`
- `department`
- `year_of_study`
- `residence_type`

#### Daily behavior
- `sleep_hours`
- `study_hours`
- `screen_time_hours`
- `social_media_hours`
- `physical_activity_minutes`
- `class_attendance_hours`
- `break_hours`

#### Academic load
- `assignments_due_count`
- `tests_upcoming_count`
- `submission_deadline_proximity`
- `lab_hours`
- `project_work_hours`

#### Wellbeing
- `stress_level`
- `mood_score`
- `fatigue_level`
- `motivation_score`

---

## Data Cleaning

The raw dataset intentionally includes realistic imperfections to simulate real-world analytics challenges.

### Cleaning steps performed
- standardized mixed date formats  
- converted inconsistent stress values like `"7/10"` and `"High"`  
- handled missing values using mean/median imputation  
- removed duplicate student-date records  
- capped unrealistic outliers  
- converted features to consistent numeric types  

### Result
- raw rows: **11016**  
- cleaned rows: **10661**  

---

## Feature Engineering

The following derived features were created:

- `sleep_deficit`
- `workload_index`
- `distraction_ratio`
- `recovery_balance`
- `deadline_pressure_score`
- `productivity_score`
- `burnout_risk_score`
- `academic_performance_index`

---

## Burnout Scoring Logic

Burnout risk is modeled as a weighted combination of normalized stress-inducing and recovery-related factors.

### Burnout score formula

```text
burnout_risk_score =
    0.17 * sleep_deficit_scaled
  + 0.20 * stress_scaled
  + 0.16 * fatigue_scaled
  + 0.16 * workload_index_scaled
  + 0.10 * deadline_pressure_scaled
  + 0.08 * distraction_ratio_scaled
  - 0.08 * recovery_balance_scaled
  - 0.05 * mood_scaled
