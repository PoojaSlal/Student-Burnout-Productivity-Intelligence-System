USE student_burnout_db;
--Average burnout risk by department
SELECT 
    s.department,
    ROUND(AVG(i.burnout_risk_score), 2) AS avg_burnout_risk
FROM fact_intelligence_scores i
JOIN dim_students s
    ON i.student_id = s.student_id
GROUP BY s.department
ORDER BY avg_burnout_risk DESC;

--Average productivity by year of study
SELECT 
    s.year_of_study,
    ROUND(AVG(i.productivity_score), 2) AS avg_productivity
FROM fact_intelligence_scores i
JOIN dim_students s
    ON i.student_id = s.student_id
GROUP BY s.year_of_study
ORDER BY s.year_of_study;

--Burnout distribution
SELECT 
    burnout_category,
    COUNT(*) AS record_count
FROM fact_intelligence_scores
GROUP BY burnout_category
ORDER BY record_count DESC;

--Detailed burnout distribution
SELECT 
    burnout_level_detailed,
    COUNT(*) AS record_count
FROM fact_intelligence_scores
GROUP BY burnout_level_detailed
ORDER BY record_count DESC;

--Risk detection queries
-- High and critical risk records
SELECT 
    i.student_id,
    s.department,
    s.year_of_study,
    i.record_date,
    ROUND(i.burnout_risk_score, 2) AS burnout_risk_score,
    i.burnout_category,
    i.burnout_level_detailed
FROM fact_intelligence_scores i
JOIN dim_students s
    ON i.student_id = s.student_id
WHERE i.burnout_category = 'High'
ORDER BY i.burnout_risk_score DESC, i.record_date DESC;

--Early warning students: Elevated + High + Critical
SELECT 
    i.student_id,
    s.department,
    s.year_of_study,
    i.record_date,
    ROUND(i.burnout_risk_score, 2) AS burnout_risk_score,
    i.burnout_level_detailed
FROM fact_intelligence_scores i
JOIN dim_students s
    ON i.student_id = s.student_id
WHERE i.burnout_level_detailed IN ('Elevated', 'High', 'Critical')
ORDER BY i.burnout_risk_score DESC, i.record_date DESC;

--Students with low productivity but rising concern
SELECT 
    i.student_id,
    s.department,
    i.record_date,
    ROUND(i.productivity_score, 2) AS productivity_score,
    ROUND(i.burnout_risk_score, 2) AS burnout_risk_score,
    i.burnout_level_detailed
FROM fact_intelligence_scores i
JOIN dim_students s
    ON i.student_id = s.student_id
WHERE i.productivity_score < 35
  AND i.burnout_level_detailed IN ('Elevated', 'High', 'Critical')
ORDER BY i.burnout_risk_score DESC, i.productivity_score ASC;

--3. Behavioral analysis queries
--Sleep vs burnout
SELECT 
    ROUND(m.sleep_hours, 1) AS sleep_hours,
    ROUND(AVG(i.burnout_risk_score), 2) AS avg_burnout_risk
FROM fact_daily_metrics m
JOIN fact_intelligence_scores i
    ON m.student_id = i.student_id
   AND m.record_date = i.record_date
GROUP BY ROUND(m.sleep_hours, 1)
ORDER BY sleep_hours;

--Workload vs productivity
SELECT 
    ROUND(i.workload_index, 1) AS workload_index,
    ROUND(AVG(i.productivity_score), 2) AS avg_productivity
FROM fact_intelligence_scores i
GROUP BY ROUND(i.workload_index, 1)
ORDER BY workload_index;

--Department-wise workload and burnout
SELECT 
    s.department,
    ROUND(AVG(i.workload_index), 2) AS avg_workload,
    ROUND(AVG(i.burnout_risk_score), 2) AS avg_burnout
FROM fact_intelligence_scores i
JOIN dim_students s
    ON i.student_id = s.student_id
GROUP BY s.department
ORDER BY avg_burnout DESC;

--Residence type comparison
SELECT 
    s.residence_type,
    ROUND(AVG(i.burnout_risk_score), 2) AS avg_burnout,
    ROUND(AVG(i.productivity_score), 2) AS avg_productivity
FROM fact_intelligence_scores i
JOIN dim_students s
    ON i.student_id = s.student_id
GROUP BY s.residence_type;

--Weekly trend analysis
--Weekly burnout trend
SELECT 
    YEAR(record_date) AS yr,
    WEEK(record_date) AS wk,
    ROUND(AVG(burnout_risk_score), 2) AS avg_weekly_burnout
FROM fact_intelligence_scores
GROUP BY YEAR(record_date), WEEK(record_date)
ORDER BY yr, wk;

--Weekly productivity trend
SELECT 
    YEAR(record_date) AS yr,
    WEEK(record_date) AS wk,
    ROUND(AVG(productivity_score), 2) AS avg_weekly_productivity
FROM fact_intelligence_scores
GROUP BY YEAR(record_date), WEEK(record_date)
ORDER BY yr, wk;

--Weekly early-warning count
SELECT 
    YEAR(record_date) AS yr,
    WEEK(record_date) AS wk,
    COUNT(*) AS at_risk_records
FROM fact_intelligence_scores
WHERE burnout_level_detailed IN ('Elevated', 'High', 'Critical')
GROUP BY YEAR(record_date), WEEK(record_date)
ORDER BY yr, wk;

--Students with highest average burnout over the semester
SELECT 
    i.student_id,
    s.department,
    s.year_of_study,
    ROUND(AVG(i.burnout_risk_score), 2) AS avg_burnout_risk,
    ROUND(AVG(i.productivity_score), 2) AS avg_productivity
FROM fact_intelligence_scores i
JOIN dim_students s
    ON i.student_id = s.student_id
GROUP BY i.student_id, s.department, s.year_of_study
ORDER BY avg_burnout_risk DESC
LIMIT 10;

--Addition of Primary Trigger and Suggestion
ALTER TABLE fact_intelligence_scores
ADD COLUMN primary_trigger VARCHAR(50),
ADD COLUMN suggested_action VARCHAR(255);