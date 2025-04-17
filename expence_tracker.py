import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Database setup
def setup_database():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

# Function to add expense
def add_expense(amount, category, description, date):
    try:
        connection = sqlite3.connect("expenses.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                       (amount, category, description, date))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Expense added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add expense: {e}")

# Function to fetch expenses
def fetch_expenses():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    connection.close()
    return rows

# Function to plot expenses
def plot_expenses():
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    connection.close()

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    if not categories:
        messagebox.showinfo("No Data", "No expenses to display!")
        return

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
    plt.title("Expense Breakdown by Category")
    plt.show()

# GUI setup
def setup_gui():
    root = tk.Tk()
    root.title("Personal Expense Tracker")

    # Input fields
    tk.Label(root, text="Amount:").grid(row=0, column=0, padx=10, pady=5)
    amount_entry = tk.Entry(root)
    amount_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=5)
    category_entry = tk.Entry(root)
    category_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Description:").grid(row=2, column=0, padx=10, pady=5)
    description_entry = tk.Entry(root)
    description_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
    date_entry = tk.Entry(root)
    date_entry.grid(row=3, column=1, padx=10, pady=5)

    # Add expense button
    def handle_add_expense():
        amount = amount_entry.get()
        category = category_entry.get()
        description = description_entry.get()
        date = date_entry.get()

        if not amount or not category or not date:
            messagebox.showerror("Error", "Please fill out all required fields!")
            return

        try:
            amount = float(amount)
            add_expense(amount, category, description, date)
            amount_entry.delete(0, tk.END)
            category_entry.delete(0, tk.END)
            description_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")

    tk.Button(root, text="Add Expense", command=handle_add_expense).grid(row=4, column=0, columnspan=2, pady=10)

    # View expenses button
    def handle_view_expenses():
        expenses = fetch_expenses()

        view_window = tk.Toplevel(root)
        view_window.title("View Expenses")
        

        tree = ttk.Treeview(view_window, columns=("ID", "Amount", "Category", "Description", "Date"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Amount", text="Amount")
        tree.heading("Category", text="Category")
        tree.heading("Description", text="Description")
        tree.heading("Date", text="Date")

        tree.pack(fill=tk.BOTH, expand=True)

        for row in expenses:
            tree.insert("", tk.END, values=row)

    tk.Button(root, text="View Expenses", command=handle_view_expenses).grid(row=5, column=0, columnspan=2, pady=10)

    # Plot expenses button
    tk.Button(root, text="Plot Expenses", command=plot_expenses).grid(row=6, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    setup_database()
    setup_gui()
