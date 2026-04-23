-- ============================================================
--  PayrollOS — Employee Payroll & Department Management System
--  MySQL Schema + Sample Data
--  Run: mysql -u root -p < schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS PayrollDB;
USE PayrollDB;

-- ─── Table 1: DEPARTMENT ────────────────────────────────────
CREATE TABLE IF NOT EXISTS Department (
    DepartmentID   INT          AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(100) NOT NULL UNIQUE,
    Location       VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- ─── Table 2: EMPLOYEE ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS Employee (
    EmployeeID   INT          AUTO_INCREMENT PRIMARY KEY,
    Name         VARCHAR(100) NOT NULL,
    Email        VARCHAR(100) NOT NULL UNIQUE,
    Phone        VARCHAR(15)  NOT NULL UNIQUE,
    HireDate     DATE         NOT NULL,
    DepartmentID INT          NOT NULL,
    CONSTRAINT fk_dept
        FOREIGN KEY (DepartmentID)
        REFERENCES Department(DepartmentID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─── Table 3: SALARY ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS Salary (
    SalaryID    INT           AUTO_INCREMENT PRIMARY KEY,
    EmployeeID  INT           NOT NULL,
    BasicSalary DECIMAL(10,2) NOT NULL CHECK (BasicSalary >= 0),
    Bonus       DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    Deductions  DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    -- TotalSalary is computed as (BasicSalary + Bonus - Deductions) in queries
    CONSTRAINT fk_emp
        FOREIGN KEY (EmployeeID)
        REFERENCES Employee(EmployeeID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ─── Sample Data ─────────────────────────────────────────────
INSERT INTO Department (DepartmentName, Location) VALUES
    ('Engineering',  'Bangalore'),
    ('HR',           'Mumbai'),
    ('Finance',      'Delhi'),
    ('Marketing',    'Hyderabad');

INSERT INTO Employee (Name, Email, Phone, HireDate, DepartmentID) VALUES
    ('Arjun Sharma',  'arjun@company.com',  '9900001111', '2021-03-15', 1),
    ('Priya Nair',    'priya@company.com',  '9900002222', '2020-07-01', 1),
    ('Rahul Mehta',   'rahul@company.com',  '9900003333', '2019-11-20', 2),
    ('Sneha Patel',   'sneha@company.com',  '9900004444', '2022-01-10', 2),
    ('Karan Gupta',   'karan@company.com',  '9900005555', '2018-05-30', 3),
    ('Meena Iyer',    'meena@company.com',  '9900006666', '2023-08-05', 3),
    ('Rohan Desai',   'rohan@company.com',  '9900007777', '2021-06-14', 4),
    ('Anjali Verma',  'anjali@company.com', '9900008888', '2020-09-22', 4);

INSERT INTO Salary (EmployeeID, BasicSalary, Bonus, Deductions) VALUES
    (1, 80000.00, 10000.00, 5000.00),
    (2, 90000.00, 12000.00, 6000.00),
    (3, 55000.00,  5000.00, 3000.00),
    (4, 60000.00,  7000.00, 4000.00),
    (5, 70000.00,  8000.00, 4500.00),
    (6, 65000.00,  6000.00, 4000.00),
    (7, 50000.00,  4000.00, 2500.00),
    (8, 55000.00,  5500.00, 3000.00);

-- ─── Useful Queries ──────────────────────────────────────────

-- All employees with department
SELECT e.EmployeeID, e.Name, e.Email, e.HireDate, d.DepartmentName, d.Location
FROM Employee e
INNER JOIN Department d ON e.DepartmentID = d.DepartmentID
ORDER BY d.DepartmentName, e.Name;

-- Full payslip
SELECT e.Name, d.DepartmentName,
       s.BasicSalary, s.Bonus, s.Deductions,
       (s.BasicSalary + s.Bonus - s.Deductions) AS TotalSalary
FROM Employee e
INNER JOIN Department d ON e.DepartmentID = d.DepartmentID
INNER JOIN Salary     s ON e.EmployeeID   = s.EmployeeID
ORDER BY TotalSalary DESC;

-- Department-wise report
SELECT
    d.DepartmentName,
    COUNT(e.EmployeeID)                                    AS TotalEmployees,
    ROUND(AVG(s.BasicSalary + s.Bonus - s.Deductions), 2) AS AvgSalary,
    SUM(s.BasicSalary + s.Bonus - s.Deductions)           AS TotalSalary,
    MAX(s.BasicSalary + s.Bonus - s.Deductions)           AS HighestSalary,
    MIN(s.BasicSalary + s.Bonus - s.Deductions)           AS LowestSalary
FROM Department d
LEFT JOIN Employee e ON d.DepartmentID = e.DepartmentID
LEFT JOIN Salary   s ON e.EmployeeID   = s.EmployeeID
GROUP BY d.DepartmentName
ORDER BY TotalSalary DESC;

-- Employees above average salary
SELECT e.Name, d.DepartmentName,
       (s.BasicSalary + s.Bonus - s.Deductions) AS TotalSalary
FROM Employee e
JOIN Department d ON e.DepartmentID = d.DepartmentID
JOIN Salary     s ON e.EmployeeID   = s.EmployeeID
WHERE (s.BasicSalary + s.Bonus - s.Deductions) >
      (SELECT AVG(BasicSalary + Bonus - Deductions) FROM Salary)
ORDER BY TotalSalary DESC;
