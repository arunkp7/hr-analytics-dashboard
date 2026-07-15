-- ─────────────────────────────────────────
-- HR Analytics — SQL Queries
-- Database: hr_analytics_db
-- ─────────────────────────────────────────

-- Query 1: Attrition Rate by Department
SELECT 
    department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) 
          * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employees
GROUP BY department
ORDER BY attrition_rate_pct DESC;

-- Query 2: Average Salary by Job Role
SELECT 
    jobrole,
    COUNT(*) AS total_employees,
    ROUND(AVG(monthlyincome), 0) AS avg_salary,
    ROUND(AVG(CASE WHEN attrition = 'Yes' THEN monthlyincome END), 0) AS avg_salary_left,
    ROUND(AVG(CASE WHEN attrition = 'No'  THEN monthlyincome END), 0) AS avg_salary_stayed
FROM hr_employees
GROUP BY jobrole
ORDER BY avg_salary DESC;

-- Query 3: Overtime Impact on Attrition
SELECT 
    overtime,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) 
          * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employees
GROUP BY overtime
ORDER BY attrition_rate_pct DESC;

-- Query 4: Attrition by Age Group
SELECT 
    agegroup,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) 
          * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employees
GROUP BY agegroup
ORDER BY attrition_rate_pct DESC;

-- Query 5: Job Satisfaction vs Attrition
SELECT 
    jobsatisfaction,
    CASE jobsatisfaction
        WHEN 1 THEN 'Low'
        WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'High'
        WHEN 4 THEN 'Very High'
    END AS satisfaction_label,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) 
          * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employees
GROUP BY jobsatisfaction
ORDER BY jobsatisfaction;

-- Query 6: Gender Distribution (Window Function)
SELECT 
    gender,
    attrition,
    COUNT(*) AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(PARTITION BY gender), 2) AS pct_within_gender
FROM hr_employees
GROUP BY gender, attrition
ORDER BY gender, attrition;

-- Query 7: Income Comparison using CTE
WITH income_summary AS (
    SELECT 
        attrition,
        ROUND(AVG(monthlyincome), 0) AS avg_income,
        ROUND(MIN(monthlyincome), 0) AS min_income,
        ROUND(MAX(monthlyincome), 0) AS max_income,
        COUNT(*) AS employee_count
    FROM hr_employees
    GROUP BY attrition
)
SELECT 
    attrition,
    avg_income,
    min_income,
    max_income,
    employee_count,
    ROUND(avg_income - LAG(avg_income) OVER(ORDER BY attrition DESC), 0) AS income_gap
FROM income_summary;

-- Query 8: Education Level vs Attrition
SELECT 
    CASE education
        WHEN 1 THEN 'Below College'
        WHEN 2 THEN 'College'
        WHEN 3 THEN 'Bachelor'
        WHEN 4 THEN 'Master'
        WHEN 5 THEN 'Doctor'
    END AS education_level,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS attrition_count,
    ROUND(SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) 
          * 100.0 / COUNT(*), 2) AS attrition_rate_pct
FROM hr_employees
GROUP BY education
ORDER BY education;

-- Query 9: Top At-Risk Employees
WITH risk_scores AS (
    SELECT 
        employeenumber,
        age,
        department,
        jobrole,
        monthlyincome,
        overtime,
        jobsatisfaction,
        yearsatcompany,
        attrition,
        CASE WHEN overtime = 'Yes'         THEN 2 ELSE 0 END +
        CASE WHEN jobsatisfaction <= 2     THEN 2 ELSE 0 END +
        CASE WHEN monthlyincome < 3000     THEN 2 ELSE 0 END +
        CASE WHEN yearsatcompany <= 2      THEN 1 ELSE 0 END +
        CASE WHEN age < 30                 THEN 1 ELSE 0 END AS risk_score
    FROM hr_employees
)
SELECT 
    employeenumber,
    age,
    department,
    jobrole,
    monthlyincome,
    overtime,
    jobsatisfaction,
    yearsatcompany,
    risk_score,
    RANK() OVER(ORDER BY risk_score DESC) AS risk_rank
FROM risk_scores
WHERE attrition = 'No'
ORDER BY risk_score DESC
LIMIT 20;

-- Query 10: Create View for Power BI
CREATE OR REPLACE VIEW vw_attrition_summary AS
SELECT 
    department,
    jobrole,
    gender,
    educationfield,
    maritalstatus,
    overtime,
    businesstravel,
    attrition,
    age,
    monthlyincome,
    jobsatisfaction,
    worklifebalance,
    yearsatcompany,
    agegroup,
    incomeband,
    CASE education
        WHEN 1 THEN 'Below College'
        WHEN 2 THEN 'College'
        WHEN 3 THEN 'Bachelor'
        WHEN 4 THEN 'Master'
        WHEN 5 THEN 'Doctor'
    END AS education_level,
    CASE jobsatisfaction
        WHEN 1 THEN 'Low'
        WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'High'
        WHEN 4 THEN 'Very High'
    END AS satisfaction_label
FROM hr_employees;