import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkintertable as ttktable
import csv
import datetime

def save_data(date, id_number, name, payment_status):
    try:
        with open('data.csv', 'a', newline='') as csvfile:
            fieldnames = ['Date', 'ID Number', 'Name', 'Payment Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Date': date, 'ID Number': id_number, 'Name': name, 'Payment Status': payment_status})
        messagebox.showinfo("Success", "Data saved successfully!")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def clear_fields():
    date_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    payment_status_var.set("Paid")

def validate_input():
    if not date_entry.get() or not id_entry.get() or not name_entry.get():
        messagebox.showerror("Error", "Please fill in all required fields.")
        return False
    try:
        datetime.datetime.strptime(date_entry.get(), "%m-%d-%Y")
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use MM-DD-YYYY.")
        return False
    return True

# Create the main window
root = tk.Tk()
root.title("Data Entry App")

# Create labels and entry fields
date_label = ttk.Label(root, text="Date (MM-DD-YYYY):")
date_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
date_var = tk.StringVar(value=datetime.datetime.now().strftime("%m-%d-%Y"))
date_entry = ttk.Entry(root, textvariable=date_var)
date_entry.grid(row=0, column=1, padx=5, pady=5)

id_label = ttk.Label(root, text="ID Number:")
id_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
id_entry = ttk.Entry(root)
id_entry.grid(row=1, column=1, padx=5, pady=5)

name_label = ttk.Label(root, text="Name:")
name_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
name_entry = ttk.Entry(root)
name_entry.grid(row=2, column=1, padx=5, pady=5)

payment_status_label = ttk.Label(root, text="Payment Status:")
payment_status_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
payment_status_var = tk.StringVar(value="Paid")
payment_status_combo = ttk.Combobox(root, textvariable=payment_status_var, values=["Paid", "Unpaid"])
payment_status_combo.grid(row=3, column=1, padx=5, pady=5)

# Create buttons
save_button = ttk.Button(root, text="Save", command=lambda: save_data(date_entry.get(), id_entry.get(), name_entry.get(), payment_status_var.get()))
save_button.grid(row=4, column=0, padx=5, pady=5)

clear_button = ttk.Button(root, text="Clear", command=clear_fields)
clear_button.grid(row=4, column=1, padx=5, pady=5)

# Create a data grid
table_frame = tk.Frame(root)
table_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
table = ttktable.Table(table_frame, height=10, width=40)
table.pack(expand=tk.YES, fill=tk.BOTH)

root.mainloop()

def populate_table():
    # Load data from CSV file
    data = []
    # ...
    table.model.data = data
    table.redraw()