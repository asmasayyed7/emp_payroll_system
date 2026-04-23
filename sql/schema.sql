
-- ============================================================
--  PayrollOS — Employee Payroll & Department Management System
--  MySQL Schema + Sample Data (Updated Database Name)
-- ============================================================

-- Database ka naam payroll_system rakha hai jo tumhare workbench mein active hai
CREATE DATABASE IF NOT EXISTS payroll_system;
USE payroll_system;

-- ─── Table 1: DEPARTMENT ────────────────────────────────────
CREATE TABLE Department (
    DepartmentID   INT           PRIMARY KEY AUTO_INCREMENT,
    DepartmentName VARCHAR(100)  NOT NULL UNIQUE,
    Location       VARCHAR(100)  NOT NULL
);

-- ─── Table 2: EMPLOYEE ──────────────────────────────────────
CREATE TABLE Employee (
    EmployeeID   INT          PRIMARY KEY AUTO_INCREMENT,
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
);

-- ─── Table 3: SALARY ────────────────────────────────────────
CREATE TABLE Salary (
    SalaryID     INT            PRIMARY KEY AUTO_INCREMENT,
    EmployeeID   INT            NOT NULL,
    BasicSalary  DECIMAL(10,2)  NOT NULL CHECK (BasicSalary >= 0),
    Bonus        DECIMAL(10,2)  NOT NULL DEFAULT 0.00,
    Deductions   DECIMAL(10,2)  NOT NULL DEFAULT 0.00,
    TotalSalary  DECIMAL(10,2)  GENERATED ALWAYS AS
                     (BasicSalary + Bonus - Deductions) STORED,
    CONSTRAINT fk_emp
        FOREIGN KEY (EmployeeID)
        REFERENCES Employee(EmployeeID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

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
    ('Anjali Verma',  'anjali@company.com', '9900008888', '2020-09-22', 4),
    

INSERT INTO Salary (EmployeeID, BasicSalary, Bonus, Deductions) VALUES
    (1, 80000.00, 10000.00, 5000.00),
    (2, 90000.00, 12000.00, 6000.00),
    (3, 55000.00,  5000.00, 3000.00),
    (4, 60000.00,  7000.00, 4000.00),
    (5, 70000.00,  8000.00, 4500.00),
    (6, 65000.00,  6000.00, 4000.00),
    (7, 50000.00,  4000.00, 2500.00),
    (8, 55000.00,  5500.00, 3000.00);