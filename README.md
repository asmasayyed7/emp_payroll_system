# PayrollOS — Employee Payroll & Department Management System

A complete frontend interface for the MySQL-based Employee Payroll System.

## Project Structure

```
PayrollOS/
├── index.html        ← Main application (open this in your browser)
├── README.md         ← You are here
├── sql/
│   └── schema.sql    ← Full MySQL database schema + sample data
└── screenshots
https://github.com/asmasayyed7/emp_payroll_system/blob/507eac5f0d4105c440da5919c5038de9c6399a1a/Screenshot%202026-04-23%20224809.png


```

## How to Run

1. Open `index.html` in any modern browser (Chrome, Firefox, Edge)
2. No server needed — runs entirely in the browser!

## Features

- Dashboard with live stats and department breakdown
- Employee Management (Add / Edit / Delete)
- Department Management (Add / Delete)
- Salary Records with live net-pay calculator
- Reports: Department-wise SUM, AVG, COUNT, MAX, MIN

## MySQL Database

Import `sql/schema.sql` into MySQL Workbench or run:

```bash
mysql -u root -p < sql/schema.sql
```

## Tech Stack

- Pure HTML5 + CSS3 + Vanilla JavaScript
- No frameworks or dependencies required
- Google Fonts: IBM Plex Mono + DM Sans
