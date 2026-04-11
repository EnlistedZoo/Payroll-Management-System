from tkinter import *
import sqlite3

# ---------------- DATABASE ----------------
conn = sqlite3.connect("employees.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS employee(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    hourly_wage REAL,
    hours_worked REAL,
    overtime_hours REAL
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------

def add_employee():
    name = name_text.get()
    wage = float(wage_text.get())
    hours = float(hours_text.get())
    overtime = float(overtime_text.get())

    cur.execute("INSERT INTO employee (name, hourly_wage, hours_worked, overtime_hours) VALUES (?,?,?,?)",
                (name, wage, hours, overtime))
    conn.commit()

    listbox.insert(END, f"{name} added successfully")

def view_employees():
    listbox.delete(0, END)
    cur.execute("SELECT * FROM employee")
    rows = cur.fetchall()
    for row in rows:
        listbox.insert(END, row)

def delete_employee():
    selected = listbox.get(ANCHOR)
    if selected:
        cur.execute("DELETE FROM employee WHERE id=?", (selected[0],))
        conn.commit()
        view_employees()

def calculate_salary():
    wage = float(wage_text.get())
    hours = float(hours_text.get())
    overtime = float(overtime_text.get())

    # Calculations
    basic = wage * hours
    overtime_pay = overtime * wage * 1.5
    gross = basic + overtime_pay
    tax = gross * 0.10
    net = gross - tax

    listbox.delete(0, END)
    listbox.insert(END, f"Basic Pay: {basic}")
    listbox.insert(END, f"Overtime Pay: {overtime_pay}")
    listbox.insert(END, f"Gross Salary: {gross}")
    listbox.insert(END, f"Tax (10%): {tax}")
    listbox.insert(END, f"Net Salary: {net}")

def select_item(event):
    try:
        selected = listbox.get(listbox.curselection())
        name_entry.delete(0, END)
        name_entry.insert(END, selected[1])

        wage_entry.delete(0, END)
        wage_entry.insert(END, selected[2])

        hours_entry.delete(0, END)
        hours_entry.insert(END, selected[3])

        overtime_entry.delete(0, END)
        overtime_entry.insert(END, selected[4])
    except:
        pass

# ---------------- UI ----------------

window = Tk()
window.title("Payroll Management System")

# Labels
Label(window, text="Name").grid(row=0, column=0)
Label(window, text="Hourly Wage").grid(row=1, column=0)
Label(window, text="Hours Worked").grid(row=2, column=0)
Label(window, text="Overtime Hours").grid(row=3, column=0)

# Entry fields
name_text = StringVar()
wage_text = StringVar()
hours_text = StringVar()
overtime_text = StringVar()

name_entry = Entry(window, textvariable=name_text)
name_entry.grid(row=0, column=1)

wage_entry = Entry(window, textvariable=wage_text)
wage_entry.grid(row=1, column=1)

hours_entry = Entry(window, textvariable=hours_text)
hours_entry.grid(row=2, column=1)

overtime_entry = Entry(window, textvariable=overtime_text)
overtime_entry.grid(row=3, column=1)

# Listbox
listbox = Listbox(window, height=10, width=50)
listbox.grid(row=4, column=0, columnspan=2)
listbox.bind('<<ListboxSelect>>', select_item)

# Buttons
Button(window, text="Add Employee", command=add_employee).grid(row=5, column=0)
Button(window, text="View Employees", command=view_employees).grid(row=5, column=1)
Button(window, text="Delete Employee", command=delete_employee).grid(row=6, column=0)
Button(window, text="Calculate Salary", command=calculate_salary).grid(row=6, column=1)

window.mainloop()

conn.close()#
