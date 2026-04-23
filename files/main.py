"""
PayrollOS — Employee Payroll & Department Management System
Built with Python Tkinter + MySQL
Run: python main.py

Requirements:
    pip install mysql-connector-python

Edit the DB_CONFIG dict below to match your MySQL credentials.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error as MySQLError
import os
from datetime import date

# ─── MySQL Connection Config ─────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "@Sayyedasma07",
    "database": "payroll_system",  # Isse update kar diya
}

# ─── Colour palette ──────────────────────────────────────────
C = {
    "bg":       "#0a0c0f",
    "bg2":      "#111418",
    "bg3":      "#181c22",
    "bg4":      "#1f242c",
    "border":   "#1e2329",
    "accent":   "#00e5a0",
    "accent2":  "#00b87a",
    "text":     "#e8eaed",
    "text2":    "#8b9099",
    "text3":    "#545a63",
    "danger":   "#ff5c5c",
    "warning":  "#f5a623",
    "blue":     "#5b9cf6",
    "white":    "#ffffff",
}


# ═══════════════════════════════════════════════════════════════
#  DATABASE LAYER  (MySQL)
# ═══════════════════════════════════════════════════════════════
class Database:
    def __init__(self):
        # First connect without specifying a database so we can CREATE it
        init_cfg = {k: v for k, v in DB_CONFIG.items() if k != "database"}
        self.conn = mysql.connector.connect(**init_cfg)
        self.conn.autocommit = False
        self._bootstrap_db()
        # Reconnect with the target database selected
        self.conn.close()
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.conn.autocommit = False
        self._create_tables()
        self._seed_data()

    # ── Internal helpers ────────────────────────────────────
    def _bootstrap_db(self):
        cur = self.conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}`")
        self.conn.commit()
        cur.close()

    def _exec(self, sql, params=None, *, many=False, fetchall=False, fetchone=False, lastrowid=False):
        cur = self.conn.cursor(dictionary=True)
        if many:
            cur.executemany(sql, params or [])
        else:
            cur.execute(sql, params or ())
        if fetchall:
            result = cur.fetchall()
            cur.close()
            return result
        if fetchone:
            result = cur.fetchone()
            cur.close()
            return result
        if lastrowid:
            rid = cur.lastrowid
            cur.close()
            return rid
        cur.close()

    def _commit(self):
        self.conn.commit()

    # ── Schema ──────────────────────────────────────────────
    def _create_tables(self):
        statements = [
            """
            CREATE TABLE IF NOT EXISTS Department (
                DepartmentID   INT          AUTO_INCREMENT PRIMARY KEY,
                DepartmentName VARCHAR(100) NOT NULL UNIQUE,
                Location       VARCHAR(100) NOT NULL
            ) ENGINE=InnoDB;
            """,
            """
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
                    ON DELETE RESTRICT ON UPDATE CASCADE
            ) ENGINE=InnoDB;
            """,
            """
            CREATE TABLE IF NOT EXISTS Salary (
                SalaryID    INT            AUTO_INCREMENT PRIMARY KEY,
                EmployeeID  INT            NOT NULL,
                BasicSalary DECIMAL(10,2)  NOT NULL CHECK (BasicSalary >= 0),
                Bonus       DECIMAL(10,2)  NOT NULL DEFAULT 0.00,
                Deductions  DECIMAL(10,2)  NOT NULL DEFAULT 0.00,
                CONSTRAINT fk_emp
                    FOREIGN KEY (EmployeeID)
                    REFERENCES Employee(EmployeeID)
                    ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB;
            """,
        ]
        for sql in statements:
            self._exec(sql)
        self._commit()

    # ── Seed data ────────────────────────────────────────────
    def _seed_data(self):
        count = self._exec(
            "SELECT COUNT(*) AS c FROM Department", fetchone=True)["c"]
        if count > 0:
            return
        self._exec(
            "INSERT INTO Department (DepartmentName, Location) VALUES (%s, %s)",
            [("Engineering","Bangalore"),("HR","Mumbai"),
             ("Finance","Delhi"),("Marketing","Hyderabad")],
            many=True,
        )
        self._exec(
            "INSERT INTO Employee (Name,Email,Phone,HireDate,DepartmentID) VALUES (%s,%s,%s,%s,%s)",
            [
                ("Arjun Sharma","arjun@company.com","9900001111","2021-03-15",1),
                ("Priya Nair",  "priya@company.com","9900002222","2020-07-01",1),
                ("Rahul Mehta", "rahul@company.com","9900003333","2019-11-20",2),
                ("Sneha Patel", "sneha@company.com","9900004444","2022-01-10",2),
                ("Karan Gupta", "karan@company.com","9900005555","2018-05-30",3),
                ("Meena Iyer",  "meena@company.com","9900006666","2023-08-05",3),
                ("Rohan Desai", "rohan@company.com","9900007777","2021-06-14",4),
                ("Anjali Verma","anjali@company.com","9900008888","2020-09-22",4),
            ],
            many=True,
        )
        self._exec(
            "INSERT INTO Salary (EmployeeID,BasicSalary,Bonus,Deductions) VALUES (%s,%s,%s,%s)",
            [(1,80000,10000,5000),(2,90000,12000,6000),(3,55000,5000,3000),
             (4,60000,7000,4000),(5,70000,8000,4500),(6,65000,6000,4000),
             (7,50000,4000,2500),(8,55000,5500,3000)],
            many=True,
        )
        self._commit()

    # ── Department queries ───────────────────────────────────
    def get_departments(self):
        return self._exec(
            "SELECT * FROM Department ORDER BY DepartmentName",
            fetchall=True)

    def add_department(self, name, loc):
        self._exec(
            "INSERT INTO Department (DepartmentName, Location) VALUES (%s, %s)",
            (name, loc))
        self._commit()

    def update_department(self, did, name, loc):
        self._exec(
            "UPDATE Department SET DepartmentName=%s, Location=%s WHERE DepartmentID=%s",
            (name, loc, did))
        self._commit()

    def delete_department(self, did):
        row = self._exec(
            "SELECT COUNT(*) AS c FROM Employee WHERE DepartmentID=%s",
            (did,), fetchone=True)
        count = row["c"]
        if count:
            raise ValueError(f"Cannot delete — {count} employee(s) still assigned.")
        self._exec("DELETE FROM Department WHERE DepartmentID=%s", (did,))
        self._commit()

    # ── Employee queries ─────────────────────────────────────
    def get_employees(self, search=""):
        q = f"%{search}%"
        return self._exec("""
            SELECT e.*, d.DepartmentName FROM Employee e
            JOIN Department d ON e.DepartmentID = d.DepartmentID
            WHERE e.Name LIKE %s OR e.Email LIKE %s OR d.DepartmentName LIKE %s
            ORDER BY e.Name
        """, (q, q, q), fetchall=True)

    def add_employee(self, name, email, phone, hire, dept_id):
        self._exec(
            "INSERT INTO Employee (Name,Email,Phone,HireDate,DepartmentID) VALUES (%s,%s,%s,%s,%s)",
            (name, email, phone, hire, dept_id))
        self._commit()

    def update_employee(self, eid, name, email, phone, hire, dept_id):
        self._exec(
            "UPDATE Employee SET Name=%s,Email=%s,Phone=%s,HireDate=%s,DepartmentID=%s WHERE EmployeeID=%s",
            (name, email, phone, hire, dept_id, eid))
        self._commit()

    def delete_employee(self, eid):
        self._exec("DELETE FROM Employee WHERE EmployeeID=%s", (eid,))
        self._commit()

    # ── Salary queries ───────────────────────────────────────
    def get_salaries(self, search=""):
        q = f"%{search}%"
        return self._exec("""
            SELECT s.*,
                   e.Name,
                   d.DepartmentName,
                   (s.BasicSalary + s.Bonus - s.Deductions) AS TotalSalary
            FROM Salary s
            JOIN Employee e   ON s.EmployeeID   = e.EmployeeID
            JOIN Department d ON e.DepartmentID = d.DepartmentID
            WHERE e.Name LIKE %s
            ORDER BY TotalSalary DESC
        """, (q,), fetchall=True)

    def add_salary(self, emp_id, basic, bonus, ded):
        self._exec(
            "INSERT INTO Salary (EmployeeID,BasicSalary,Bonus,Deductions) VALUES (%s,%s,%s,%s)",
            (emp_id, basic, bonus, ded))
        self._commit()

    def update_salary(self, sid, basic, bonus, ded):
        self._exec(
            "UPDATE Salary SET BasicSalary=%s, Bonus=%s, Deductions=%s WHERE SalaryID=%s",
            (basic, bonus, ded, sid))
        self._commit()

    def delete_salary(self, sid):
        self._exec("DELETE FROM Salary WHERE SalaryID=%s", (sid,))
        self._commit()

    # ── Report queries ───────────────────────────────────────
    def get_dept_report(self):
        return self._exec("""
            SELECT d.DepartmentID,
                   d.DepartmentName,
                   d.Location,
                   COUNT(e.EmployeeID) AS EmpCount,
                   ROUND(AVG(s.BasicSalary + s.Bonus - s.Deductions), 2) AS AvgSalary,
                   ROUND(SUM(s.BasicSalary + s.Bonus - s.Deductions), 2) AS TotalSalary,
                   ROUND(MAX(s.BasicSalary + s.Bonus - s.Deductions), 2) AS MaxSalary,
                   ROUND(MIN(s.BasicSalary + s.Bonus - s.Deductions), 2) AS MinSalary
            FROM Department d
            LEFT JOIN Employee e ON d.DepartmentID = e.DepartmentID
            LEFT JOIN Salary   s ON e.EmployeeID   = s.EmployeeID
            GROUP BY d.DepartmentID, d.DepartmentName, d.Location
            ORDER BY TotalSalary DESC
        """, fetchall=True)

    def get_stats(self):
        row = self._exec("""
            SELECT
                (SELECT COUNT(*) FROM Employee)   AS emps,
                (SELECT COUNT(*) FROM Department) AS depts,
                COALESCE((SELECT SUM(BasicSalary+Bonus-Deductions) FROM Salary),0) AS tot,
                COALESCE((SELECT AVG(BasicSalary+Bonus-Deductions) FROM Salary),0) AS avg_sal
        """, fetchone=True)
        return row["emps"], row["depts"], float(row["tot"]), float(row["avg_sal"])

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════
#  REUSABLE UI HELPERS
# ═══════════════════════════════════════════════════════════════
def styled_btn(parent, text, cmd, color=None, fg="#000", **kw):
    bg = color or C["accent"]
    b = tk.Button(parent, text=text, command=cmd,
                  bg=bg, fg=fg, activebackground=bg, activeforeground=fg,
                  relief="flat", cursor="hand2",
                  font=("Consolas", 10, "bold"),
                  padx=12, pady=5, **kw)
    b.bind("<Enter>", lambda e: b.config(bg=_lighten(bg)))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


def _lighten(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = min(255, r + 20); g = min(255, g + 20); b = min(255, b + 20)
    return f"#{r:02x}{g:02x}{b:02x}"


def make_tree(parent, columns, col_widths, height=14):
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Dark.Treeview",
        background=C["bg2"], foreground=C["text2"],
        fieldbackground=C["bg2"], rowheight=28,
        borderwidth=0, font=("Consolas", 10))
    style.configure("Dark.Treeview.Heading",
        background=C["bg3"], foreground=C["text3"],
        borderwidth=0, font=("Consolas", 9, "bold"), relief="flat")
    style.map("Dark.Treeview",
        background=[("selected", C["bg4"])],
        foreground=[("selected", C["accent"])])

    frame = tk.Frame(parent, bg=C["bg2"])
    tree  = ttk.Treeview(frame, columns=columns, show="headings",
                         height=height, style="Dark.Treeview")
    vsb   = tk.Scrollbar(frame, orient="vertical", command=tree.yview,
                         bg=C["bg3"], troughcolor=C["bg2"], width=10)
    tree.configure(yscrollcommand=vsb.set)
    for col, width in zip(columns, col_widths):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor="w", minwidth=40)
    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")
    return frame, tree


def entry_field(parent, label_text, row, default="", width=28):
    tk.Label(parent, text=label_text, bg=C["bg3"], fg=C["text3"],
             font=("Consolas", 9)).grid(row=row, column=0, sticky="w",
                                        padx=(0, 10), pady=4)
    var = tk.StringVar(value=default)
    e = tk.Entry(parent, textvariable=var, bg=C["bg4"], fg=C["text"],
                 insertbackground=C["accent"], relief="flat",
                 font=("Consolas", 10), width=width,
                 highlightthickness=1, highlightbackground=C["border"],
                 highlightcolor=C["accent"])
    e.grid(row=row, column=1, sticky="ew", pady=4, ipady=5)
    return var


def fmt_inr(val):
    try:
        return "₹{:,.0f}".format(float(val))
    except Exception:
        return "₹0"


# ═══════════════════════════════════════════════════════════════
#  DIALOGS
# ═══════════════════════════════════════════════════════════════
class BaseDialog(tk.Toplevel):
    def __init__(self, parent, title, width=420, height=380):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=C["bg3"])
        self.resizable(False, False)
        self.geometry(f"{width}x{height}")
        self._center(parent)
        self.grab_set()
        self.result = None
        self._build()

    def _center(self, parent):
        self.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width() // 2
        py = parent.winfo_rooty() + parent.winfo_height() // 2
        x  = px - int(self.geometry().split("x")[0]) // 2
        y  = py - int(self.geometry().split("x")[1].split("+")[0]) // 2
        self.geometry(f"+{x}+{y}")

    def _build(self): pass

    def _footer(self, parent, save_cmd):
        f = tk.Frame(parent, bg=C["bg3"])
        f.pack(fill="x", padx=20, pady=(10, 16))
        styled_btn(f, "Cancel", self.destroy,
                   color=C["bg4"], fg=C["text2"]).pack(side="right", padx=(6, 0))
        styled_btn(f, "  Save  ", save_cmd).pack(side="right")


class DeptDialog(BaseDialog):
    def __init__(self, parent, name="", loc=""):
        self._def_name = name
        self._def_loc  = loc
        super().__init__(parent, "Department", 400, 240)

    def _build(self):
        tk.Label(self, text="Department Details", bg=C["bg3"],
                 fg=C["accent"], font=("Consolas", 12, "bold")).pack(pady=(18, 12))
        form = tk.Frame(self, bg=C["bg3"])
        form.pack(padx=24, fill="x")
        form.columnconfigure(1, weight=1)
        self.v_name = entry_field(form, "Name",     0, self._def_name)
        self.v_loc  = entry_field(form, "Location", 1, self._def_loc)
        self._footer(self, self._save)

    def _save(self):
        n = self.v_name.get().strip()
        l = self.v_loc.get().strip()
        if not n or not l:
            messagebox.showwarning("Missing", "Fill all fields.", parent=self)
            return
        self.result = (n, l)
        self.destroy()


class EmpDialog(BaseDialog):
    def __init__(self, parent, db, emp=None):
        self._db  = db
        self._emp = emp
        super().__init__(parent, "Employee", 440, 400)

    def _build(self):
        tk.Label(self, text="Employee Details", bg=C["bg3"],
                 fg=C["accent"], font=("Consolas", 12, "bold")).pack(pady=(18, 12))
        form = tk.Frame(self, bg=C["bg3"])
        form.pack(padx=24, fill="x")
        form.columnconfigure(1, weight=1)

        e = self._emp
        self.v_name  = entry_field(form, "Full Name", 0, e["Name"]    if e else "")
        self.v_email = entry_field(form, "Email",     1, e["Email"]   if e else "")
        self.v_phone = entry_field(form, "Phone",     2, e["Phone"]   if e else "")
        hire_default = str(e["HireDate"]) if e else str(date.today())
        self.v_hire  = entry_field(form, "Hire Date\n(YYYY-MM-DD)", 3, hire_default)

        tk.Label(form, text="Department", bg=C["bg3"], fg=C["text3"],
                 font=("Consolas", 9)).grid(row=4, column=0, sticky="w", pady=4)
        depts = self._db.get_departments()
        self._dept_ids   = [d["DepartmentID"]   for d in depts]
        self._dept_names = [d["DepartmentName"] for d in depts]
        self.v_dept = tk.StringVar()
        combo = ttk.Combobox(form, textvariable=self.v_dept,
                             values=self._dept_names, state="readonly", width=26)
        combo.grid(row=4, column=1, sticky="ew", pady=4, ipady=4)
        if e:
            try:   combo.current(self._dept_ids.index(e["DepartmentID"]))
            except: combo.current(0)
        elif depts:
            combo.current(0)

        self._footer(self, self._save)

    def _save(self):
        n  = self.v_name.get().strip()
        em = self.v_email.get().strip()
        ph = self.v_phone.get().strip()
        hi = self.v_hire.get().strip()
        dn = self.v_dept.get()
        if not all([n, em, ph, hi, dn]):
            messagebox.showwarning("Missing", "Fill all fields.", parent=self)
            return
        try:
            idx = self._dept_names.index(dn)
        except ValueError:
            messagebox.showwarning("Error", "Select a valid department.", parent=self)
            return
        self.result = (n, em, ph, hi, self._dept_ids[idx])
        self.destroy()


class SalaryDialog(BaseDialog):
    def __init__(self, parent, db, sal=None):
        self._db  = db
        self._sal = sal
        super().__init__(parent, "Salary Record", 440, 380)

    def _build(self):
        tk.Label(self, text="Salary Record", bg=C["bg3"],
                 fg=C["accent"], font=("Consolas", 12, "bold")).pack(pady=(18, 12))
        form = tk.Frame(self, bg=C["bg3"])
        form.pack(padx=24, fill="x")
        form.columnconfigure(1, weight=1)

        s = self._sal
        if not s:
            tk.Label(form, text="Employee", bg=C["bg3"], fg=C["text3"],
                     font=("Consolas", 9)).grid(row=0, column=0, sticky="w", pady=4)
            emps = self._db.get_employees()
            self._emp_ids   = [e["EmployeeID"] for e in emps]
            self._emp_names = [e["Name"]        for e in emps]
            self.v_emp = tk.StringVar()
            combo = ttk.Combobox(form, textvariable=self.v_emp,
                                 values=self._emp_names, state="readonly", width=26)
            combo.grid(row=0, column=1, sticky="ew", pady=4, ipady=4)
            if emps: combo.current(0)
            row_off = 1
        else:
            row_off = 0

        self.v_basic = entry_field(form, "Basic Salary", row_off,
                                   str(s["BasicSalary"]) if s else "")
        self.v_bonus = entry_field(form, "Bonus",        row_off + 1,
                                   str(s["Bonus"])       if s else "0")
        self.v_ded   = entry_field(form, "Deductions",   row_off + 2,
                                   str(s["Deductions"])  if s else "0")

        # Live net-pay preview
        self._net_var = tk.StringVar(value="Net: ₹0")
        tk.Label(form, textvariable=self._net_var,
                 bg=C["bg3"], fg=C["accent"],
                 font=("Consolas", 11, "bold")).grid(
                     row=row_off + 3, column=0, columnspan=2,
                     sticky="e", pady=(8, 0))

        for v in (self.v_basic, self.v_bonus, self.v_ded):
            v.trace_add("write", self._update_net)
        self._update_net()
        self._footer(self, self._save)

    def _update_net(self, *_):
        try:
            net = (float(self.v_basic.get() or 0)
                   + float(self.v_bonus.get() or 0)
                   - float(self.v_ded.get()   or 0))
            self._net_var.set(f"Net: {fmt_inr(net)}")
        except ValueError:
            self._net_var.set("Net: —")

    def _save(self):
        try:
            basic = float(self.v_basic.get())
            bonus = float(self.v_bonus.get())
            ded   = float(self.v_ded.get())
        except ValueError:
            messagebox.showwarning("Invalid", "Salary fields must be numbers.", parent=self)
            return
        if self._sal:
            self.result = (basic, bonus, ded)
        else:
            dn = self.v_emp.get()
            try:   idx = self._emp_names.index(dn)
            except ValueError:
                messagebox.showwarning("Error", "Select an employee.", parent=self)
                return
            self.result = (self._emp_ids[idx], basic, bonus, ded)
        self.destroy()


# ═══════════════════════════════════════════════════════════════
#  PAGES
# ═══════════════════════════════════════════════════════════════
class Page(tk.Frame):
    def __init__(self, parent, db, app):
        super().__init__(parent, bg=C["bg"])
        self.db  = db
        self.app = app
        self.build()

    def build(self): pass
    def refresh(self): pass

    def _section_header(self, parent, title, subtitle=""):
        top = tk.Frame(parent, bg=C["bg"])
        top.pack(fill="x", padx=24, pady=(20, 10))
        tk.Label(top, text=title, bg=C["bg"], fg=C["text"],
                 font=("Consolas", 15, "bold")).pack(side="left")
        if subtitle:
            tk.Label(top, text=subtitle, bg=C["bg"], fg=C["text3"],
                     font=("Consolas", 9)).pack(side="right", padx=4)


# ── Dashboard ────────────────────────────────────────────────
class DashboardPage(Page):
    def build(self):
        self._section_header(self, "◈  Dashboard", "PAYROLLOS v2.0 · MySQL")

        stats_frame = tk.Frame(self, bg=C["bg"])
        stats_frame.pack(fill="x", padx=24, pady=(0, 20))

        self._stat_vars = {}
        for i, (key, label, icon) in enumerate([
            ("emps",  "Total Employees",  "◉"),
            ("depts", "Departments",      "⬡"),
            ("tot",   "Total Payroll",    "₹"),
            ("avg",   "Avg. Net Salary",  "~"),
        ]):
            card = tk.Frame(stats_frame, bg=C["bg2"],
                            highlightthickness=1,
                            highlightbackground=C["border"])
            card.grid(row=0, column=i, padx=(0, 12), ipadx=16, ipady=12, sticky="nsew")
            stats_frame.columnconfigure(i, weight=1)
            tk.Label(card, text=icon, bg=C["bg2"], fg=C["accent"],
                     font=("Consolas", 18)).pack(pady=(10, 2))
            var = tk.StringVar(value="—")
            self._stat_vars[key] = var
            tk.Label(card, textvariable=var, bg=C["bg2"], fg=C["text"],
                     font=("Consolas", 14, "bold")).pack()
            tk.Label(card, text=label, bg=C["bg2"], fg=C["text3"],
                     font=("Consolas", 9)).pack(pady=(2, 10))

        tk.Label(self, text="Recent Employees", bg=C["bg"], fg=C["text2"],
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=24, pady=(0, 6))
        tf, self._recent_tree = make_tree(self,
            ["#", "Name", "Email", "Department", "Hired"],
            [40, 160, 200, 130, 110], height=6)
        tf.pack(fill="x", padx=24, pady=(0, 20))

        tk.Label(self, text="Salary Overview by Department",
                 bg=C["bg"], fg=C["text2"],
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=24, pady=(0, 6))
        tf2, self._dept_tree = make_tree(self,
            ["Department", "Employees", "Total Salary", "Avg Salary"],
            [160, 90, 160, 150], height=5)
        tf2.pack(fill="both", expand=True, padx=24, pady=(0, 20))

    def refresh(self):
        try:
            emps, depts, tot, avg = self.db.get_stats()
        except Exception:
            return
        self._stat_vars["emps"].set(str(emps))
        self._stat_vars["depts"].set(str(depts))
        self._stat_vars["tot"].set(fmt_inr(tot))
        self._stat_vars["avg"].set(fmt_inr(avg))

        for r in self._recent_tree.get_children():
            self._recent_tree.delete(r)
        for i, e in enumerate(self.db.get_employees()[:8]):
            self._recent_tree.insert("", "end", values=(
                f"#{e['EmployeeID']:03d}", e["Name"], e["Email"],
                e["DepartmentName"], str(e["HireDate"])))

        for r in self._dept_tree.get_children():
            self._dept_tree.delete(r)
        for row in self.db.get_dept_report():
            self._dept_tree.insert("", "end", values=(
                row["DepartmentName"], row["EmpCount"],
                fmt_inr(row["TotalSalary"] or 0),
                fmt_inr(row["AvgSalary"]   or 0)))


# ── Employees ────────────────────────────────────────────────
class EmployeesPage(Page):
    def build(self):
        top = tk.Frame(self, bg=C["bg"])
        top.pack(fill="x", padx=24, pady=(20, 10))
        tk.Label(top, text="◉  Employees", bg=C["bg"], fg=C["text"],
                 font=("Consolas", 15, "bold")).pack(side="left")

        btn_f = tk.Frame(top, bg=C["bg"])
        btn_f.pack(side="right")
        styled_btn(btn_f, "✎ Edit",   self._edit,   color=C["blue"],   fg=C["white"]).pack(side="right", padx=(6, 0))
        styled_btn(btn_f, "✕ Delete", self._delete, color=C["danger"], fg=C["white"]).pack(side="right", padx=(6, 0))
        styled_btn(btn_f, "+ Add",    self._add).pack(side="right")

        sf = tk.Frame(self, bg=C["bg"])
        sf.pack(fill="x", padx=24, pady=(0, 10))
        tk.Label(sf, text="Search:", bg=C["bg"], fg=C["text3"],
                 font=("Consolas", 9)).pack(side="left")
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self.refresh())
        tk.Entry(sf, textvariable=self._search_var,
                 bg=C["bg3"], fg=C["text"], insertbackground=C["accent"],
                 relief="flat", font=("Consolas", 10), width=30,
                 highlightthickness=1, highlightbackground=C["border"],
                 highlightcolor=C["accent"]).pack(side="left", padx=8, ipady=5)

        tf, self._tree = make_tree(self,
            ["#", "Name", "Email", "Phone", "Hired", "Department"],
            [45, 150, 190, 110, 100, 130])
        tf.pack(fill="both", expand=True, padx=24, pady=(0, 20))

    def refresh(self):
        q = self._search_var.get() if hasattr(self, "_search_var") else ""
        for r in self._tree.get_children(): self._tree.delete(r)
        for e in self.db.get_employees(q):
            self._tree.insert("", "end", values=(
                f"#{e['EmployeeID']:03d}", e["Name"], e["Email"],
                e["Phone"], str(e["HireDate"]), e["DepartmentName"]))

    def _selected_id(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Please select a row first.")
            return None
        return int(str(self._tree.item(sel[0])["values"][0]).lstrip("#"))

    def _add(self):
        dlg = EmpDialog(self, self.db)
        self.wait_window(dlg)
        if dlg.result:
            try:
                self.db.add_employee(*dlg.result)
                self.refresh(); self.app.refresh_stats()
                self.app.toast("Employee added!")
            except MySQLError as e:
                messagebox.showerror("DB Error", str(e))

    def _edit(self):
        eid = self._selected_id()
        if not eid: return
        emp = next((r for r in self.db.get_employees() if r["EmployeeID"] == eid), None)
        if not emp: return
        dlg = EmpDialog(self, self.db, emp)
        self.wait_window(dlg)
        if dlg.result:
            try:
                self.db.update_employee(eid, *dlg.result)
                self.refresh(); self.app.refresh_stats()
                self.app.toast("Employee updated!")
            except MySQLError as e:
                messagebox.showerror("DB Error", str(e))

    def _delete(self):
        eid = self._selected_id()
        if not eid: return
        if messagebox.askyesno("Confirm", f"Delete Employee #{eid}?"):
            self.db.delete_employee(eid)
            self.refresh(); self.app.refresh_stats()
            self.app.toast("Employee deleted.", kind="warn")


# ── Departments ──────────────────────────────────────────────
class DepartmentsPage(Page):
    def build(self):
        top = tk.Frame(self, bg=C["bg"])
        top.pack(fill="x", padx=24, pady=(20, 10))
        tk.Label(top, text="⬡  Departments", bg=C["bg"], fg=C["text"],
                 font=("Consolas", 15, "bold")).pack(side="left")

        btn_f = tk.Frame(top, bg=C["bg"])
        btn_f.pack(side="right")
        styled_btn(btn_f, "✎ Edit",   self._edit,   color=C["blue"],   fg=C["white"]).pack(side="right", padx=(6, 0))
        styled_btn(btn_f, "✕ Delete", self._delete, color=C["danger"], fg=C["white"]).pack(side="right", padx=(6, 0))
        styled_btn(btn_f, "+ Add",    self._add).pack(side="right")

        tf, self._tree = make_tree(self,
            ["ID", "Department", "Location", "Employees", "Total Salary", "Avg Salary"],
            [45, 160, 130, 90, 130, 130])
        tf.pack(fill="both", expand=True, padx=24, pady=(0, 20))

    def refresh(self):
        for r in self._tree.get_children(): self._tree.delete(r)
        for row in self.db.get_dept_report():
            self._tree.insert("", "end", iid=str(row["DepartmentID"]),
                values=(f"#{row['DepartmentID']:03d}",
                        row["DepartmentName"], row["Location"],
                        row["EmpCount"],
                        fmt_inr(row["TotalSalary"] or 0),
                        fmt_inr(row["AvgSalary"]   or 0)))

    def _selected_id(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Please select a department.")
            return None
        return int(sel[0])

    def _add(self):
        dlg = DeptDialog(self)
        self.wait_window(dlg)
        if dlg.result:
            try:
                self.db.add_department(*dlg.result)
                self.refresh(); self.app.refresh_stats()
                self.app.toast("Department added!")
            except MySQLError:
                messagebox.showerror("Error", "Department name already exists.")

    def _edit(self):
        did = self._selected_id()
        if not did: return
        dept = next((d for d in self.db.get_departments()
                     if d["DepartmentID"] == did), None)
        if not dept: return
        dlg = DeptDialog(self, dept["DepartmentName"], dept["Location"])
        self.wait_window(dlg)
        if dlg.result:
            try:
                self.db.update_department(did, *dlg.result)
                self.refresh(); self.app.refresh_stats()
                self.app.toast("Department updated!")
            except MySQLError:
                messagebox.showerror("Error", "Name already exists.")

    def _delete(self):
        did = self._selected_id()
        if not did: return
        if messagebox.askyesno("Confirm", "Delete this department?"):
            try:
                self.db.delete_department(did)
                self.refresh(); self.app.refresh_stats()
                self.app.toast("Department deleted.", kind="warn")
            except ValueError as e:
                messagebox.showerror("Cannot Delete", str(e))


# ── Salary ───────────────────────────────────────────────────
class SalaryPage(Page):
    def build(self):
        top = tk.Frame(self, bg=C["bg"])
        top.pack(fill="x", padx=24, pady=(20, 10))
        tk.Label(top, text="◈  Salary Records", bg=C["bg"], fg=C["text"],
                 font=("Consolas", 15, "bold")).pack(side="left")

        btn_f = tk.Frame(top, bg=C["bg"])
        btn_f.pack(side="right")
        styled_btn(btn_f, "✎ Edit",   self._edit,   color=C["blue"],   fg=C["white"]).pack(side="right", padx=(6, 0))
        styled_btn(btn_f, "✕ Delete", self._delete, color=C["danger"], fg=C["white"]).pack(side="right", padx=(6, 0))
        styled_btn(btn_f, "+ Add",    self._add).pack(side="right")

        sf = tk.Frame(self, bg=C["bg"])
        sf.pack(fill="x", padx=24, pady=(0, 10))
        tk.Label(sf, text="Search:", bg=C["bg"], fg=C["text3"],
                 font=("Consolas", 9)).pack(side="left")
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self.refresh())
        tk.Entry(sf, textvariable=self._search_var,
                 bg=C["bg3"], fg=C["text"], insertbackground=C["accent"],
                 relief="flat", font=("Consolas", 10), width=30,
                 highlightthickness=1, highlightbackground=C["border"],
                 highlightcolor=C["accent"]).pack(side="left", padx=8, ipady=5)

        tf, self._tree = make_tree(self,
            ["Sal ID", "Employee", "Department", "Basic", "Bonus", "Deductions", "Net Pay"],
            [60, 160, 120, 110, 100, 110, 120])
        tf.pack(fill="both", expand=True, padx=24, pady=(0, 20))

    def refresh(self):
        q = self._search_var.get() if hasattr(self, "_search_var") else ""
        for r in self._tree.get_children(): self._tree.delete(r)
        for s in self.db.get_salaries(q):
            self._tree.insert("", "end", iid=str(s["SalaryID"]),
                values=(f"#{s['SalaryID']:03d}", s["Name"],
                        s["DepartmentName"],
                        fmt_inr(s["BasicSalary"]),
                        fmt_inr(s["Bonus"]),
                        fmt_inr(s["Deductions"]),
                        fmt_inr(s["TotalSalary"])))

    def _selected_id(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Please select a salary record.")
            return None
        return int(sel[0])

    def _add(self):
        dlg = SalaryDialog(self, self.db)
        self.wait_window(dlg)
        if dlg.result:
            try:
                self.db.add_salary(*dlg.result)
                self.refresh(); self.app.refresh_stats()
                self.app.toast("Salary record added!")
            except MySQLError as e:
                messagebox.showerror("DB Error", str(e))

    def _edit(self):
        sid = self._selected_id()
        if not sid: return
        sal = next((s for s in self.db.get_salaries() if s["SalaryID"] == sid), None)
        if not sal: return
        dlg = SalaryDialog(self, self.db, sal)
        self.wait_window(dlg)
        if dlg.result:
            self.db.update_salary(sid, *dlg.result)
            self.refresh(); self.app.refresh_stats()
            self.app.toast("Salary updated!")

    def _delete(self):
        sid = self._selected_id()
        if not sid: return
        if messagebox.askyesno("Confirm", "Delete this salary record?"):
            self.db.delete_salary(sid)
            self.refresh(); self.app.refresh_stats()
            self.app.toast("Record deleted.", kind="warn")


# ── Reports ──────────────────────────────────────────────────
class ReportsPage(Page):
    def build(self):
        self._section_header(self, "▦  Reports", "ANALYTICS")

        tk.Label(self, text="Department-wise Salary Report",
                 bg=C["bg"], fg=C["text2"],
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=24, pady=(0, 6))
        tf, self._tree1 = make_tree(self,
            ["Department", "Location", "Employees", "Avg Salary",
             "Total Salary", "Highest", "Lowest"],
            [140, 110, 90, 120, 130, 110, 110], height=7)
        tf.pack(fill="x", padx=24, pady=(0, 20))

        tk.Label(self, text="Full Payslip View (JOIN Query)",
                 bg=C["bg"], fg=C["text2"],
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=24, pady=(0, 6))
        tf2, self._tree2 = make_tree(self,
            ["Employee", "Department", "Basic", "Bonus", "Deductions", "Net Pay"],
            [160, 130, 110, 100, 110, 120], height=7)
        tf2.pack(fill="both", expand=True, padx=24, pady=(0, 20))

    def refresh(self):
        for r in self._tree1.get_children(): self._tree1.delete(r)
        for row in self.db.get_dept_report():
            self._tree1.insert("", "end", values=(
                row["DepartmentName"], row["Location"],
                row["EmpCount"],
                fmt_inr(row["AvgSalary"]   or 0),
                fmt_inr(row["TotalSalary"] or 0),
                fmt_inr(row["MaxSalary"]   or 0),
                fmt_inr(row["MinSalary"]   or 0)))

        for r in self._tree2.get_children(): self._tree2.delete(r)
        for s in self.db.get_salaries():
            self._tree2.insert("", "end", values=(
                s["Name"], s["DepartmentName"],
                fmt_inr(s["BasicSalary"]),
                fmt_inr(s["Bonus"]),
                fmt_inr(s["Deductions"]),
                fmt_inr(s["TotalSalary"])))


# ═══════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PayrollOS — Employee Payroll & Department Management · MySQL")
        self.geometry("1100x680")
        self.minsize(900, 580)
        self.configure(bg=C["bg"])

        try:
            self.db = Database()
        except MySQLError as e:
            messagebox.showerror(
                "MySQL Connection Failed",
                f"Could not connect to MySQL.\n\n{e}\n\n"
                "Edit the DB_CONFIG dict at the top of main.py and try again."
            )
            self.destroy()
            return

        self._pages = {}
        self._active = None
        self._build_ui()
        self._nav_to("dashboard")
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # ── Sidebar ─────────────────────────────────────────
        sidebar = tk.Frame(self, bg=C["bg2"], width=200)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        logo = tk.Frame(sidebar, bg=C["bg2"])
        logo.pack(fill="x", padx=18, pady=(22, 18))
        tk.Label(logo, text="// PayrollOS", bg=C["bg2"], fg=C["accent"],
                 font=("Consolas", 10, "bold")).pack(anchor="w")
        tk.Label(logo, text="Management System", bg=C["bg2"],
                 fg=C["text2"], font=("DM Sans", 11, "bold")).pack(anchor="w", pady=(2, 0))

        tk.Frame(sidebar, bg=C["border"], height=1).pack(fill="x")

        nav = tk.Frame(sidebar, bg=C["bg2"])
        nav.pack(fill="x", padx=8, pady=12)

        self._nav_btns = {}
        items = [
            ("dashboard",   "◈  Dashboard"),
            ("employees",   "◉  Employees"),
            ("departments", "⬡  Departments"),
            ("salary",      "◈  Salary Records"),
            ("reports",     "▦  Reports"),
        ]
        for key, text in items:
            btn = tk.Label(nav, text=text, bg=C["bg2"], fg=C["text2"],
                           font=("Consolas", 10), padx=14, pady=9,
                           cursor="hand2", anchor="w")
            btn.pack(fill="x", pady=1)
            btn.bind("<Button-1>", lambda e, k=key: self._nav_to(k))
            btn.bind("<Enter>",    lambda e, b=btn, k=key:
                     b.config(bg=C["bg3"], fg=C["text"])
                     if k != self._active else None)
            btn.bind("<Leave>",    lambda e, b=btn, k=key:
                     b.config(bg=C["bg2"] if k != self._active else C["bg3"],
                              fg=C["text2"] if k != self._active else C["accent"]))
            self._nav_btns[key] = btn

        # DB status indicator
        status = tk.Frame(sidebar, bg=C["bg2"])
        status.pack(side="bottom", fill="x", padx=16, pady=14)
        tk.Frame(sidebar, bg=C["border"], height=1).pack(side="bottom", fill="x")
        dot = tk.Canvas(status, width=8, height=8, bg=C["bg2"], highlightthickness=0)
        dot.create_oval(0, 0, 7, 7, fill=C["accent"], outline="")
        dot.pack(side="left", pady=2)
        tk.Label(status,
                 text=f"MySQL · {DB_CONFIG['host']}:{DB_CONFIG['port']}",
                 bg=C["bg2"], fg=C["text3"],
                 font=("Consolas", 8)).pack(side="left", padx=6)

        # ── Content area ─────────────────────────────────────
        content = tk.Frame(self, bg=C["bg"])
        content.grid(row=0, column=1, sticky="nsew")

        page_classes = {
            "dashboard":   DashboardPage,
            "employees":   EmployeesPage,
            "departments": DepartmentsPage,
            "salary":      SalaryPage,
            "reports":     ReportsPage,
        }
        for key, cls in page_classes.items():
            p = cls(content, self.db, self)
            p.place(relwidth=1, relheight=1)
            self._pages[key] = p

        # Toast notification
        self._toast_lbl = tk.Label(
            self, text="", bg=C["bg3"], fg=C["accent"],
            font=("Consolas", 10), padx=16, pady=8, relief="flat",
            highlightthickness=1, highlightbackground=C["border"])
        self._toast_job = None

    def _nav_to(self, key):
        if self._active:
            self._nav_btns[self._active].config(bg=C["bg2"], fg=C["text2"])
        self._active = key
        self._nav_btns[key].config(bg=C["bg3"], fg=C["accent"])
        self._pages[key].lift()
        self._pages[key].refresh()

    def refresh_stats(self):
        if self._active == "dashboard":
            self._pages["dashboard"].refresh()

    def toast(self, msg, kind="ok"):
        colors = {"ok": C["accent"], "warn": C["warning"], "danger": C["danger"]}
        self._toast_lbl.config(text=f"  ✓  {msg}", fg=colors.get(kind, C["accent"]))
        self._toast_lbl.place(relx=1.0, rely=1.0, anchor="se", x=-24, y=-24)
        if self._toast_job:
            self.after_cancel(self._toast_job)
        self._toast_job = self.after(2500, self._toast_lbl.place_forget)

    def _on_close(self):
        self.db.close()
        self.destroy()


# ─── Entry point ─────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
