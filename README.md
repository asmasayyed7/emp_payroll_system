# PayrollOS — Employee Payroll & Department Management System

A complete frontend interface for the MySQL-based Employee Payroll System.

## Project Structure

```
PayrollOS/
├── index.html        ← Main application (open this in your browser)
├── README.md         ← You are here
├── sql/
│   └── schema.sql    ← Full MySQL database schema + sample data
```
## Preview
<img width="1912" height="758" alt="Screenshot 2026-04-23 224809" src="https://github.com/user-attachments/assets/4b654022-6587-4a1c-88f2-a8b9d3f813c8" />
<img width="1911" height="824" alt="Screenshot 2026-04-23 224753" src="https://github.com/user-attachments/assets/8e31e17a-5bf5-476b-8393-55b6830d397d" />


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
