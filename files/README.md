# PayrollOS — Employee Payroll & Department Management System
Built with Python + Tkinter + MySQL

## Requirements

- Python 3.8 or higher
- MySQL Server (local or remote)
- One extra package:

```bash
pip install mysql-connector-python
```

## Setup

### 1. Configure your MySQL credentials
Open `main.py` and edit the `DB_CONFIG` at the top:

```python
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "your_password_here",   # ← change this
    "database": "PayrollDB",
}
```

### 2. Run the app
```bash
python main.py
```

The app will automatically:
- Create the `PayrollDB` database if it doesn't exist
- Create all tables (Department, Employee, Salary)
- Insert sample data on first run

### Optional: Import schema manually
If you prefer to set up the database yourself first:
```bash
mysql -u root -p < schema.sql
```

## Features

| Page         | What you can do                                       |
|--------------|-------------------------------------------------------|
| Dashboard    | Live stats, recent employees, department overview     |
| Employees    | Add / Edit / Delete + Search                          |
| Departments  | Add / Edit / Delete (blocked if employees exist)      |
| Salary       | Add / Edit / Delete records + live net pay preview    |
| Reports      | Dept-wise SUM, AVG, COUNT, MAX, MIN + full payslip    |

## Project Structure

```
PayrollOS/
├── main.py       ← Run this (entire app: frontend + backend)
├── schema.sql    ← Optional manual DB setup / reference
└── README.md     ← This file
```

## Database (MySQL)

Three tables connected by foreign keys:

```
Department ──< Employee ──< Salary
```

- `Department`: DepartmentID, DepartmentName, Location
- `Employee`: EmployeeID, Name, Email, Phone, HireDate, DepartmentID (FK)
- `Salary`: SalaryID, EmployeeID (FK), BasicSalary, Bonus, Deductions

TotalSalary = BasicSalary + Bonus - Deductions (computed in queries)

## Keyboard / UI Tips

- Click a row to select it, then use Edit or Delete buttons
- Search box filters live as you type (Employees & Salary pages)
- Toast notifications confirm every action (bottom-right corner)
