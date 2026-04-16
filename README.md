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
