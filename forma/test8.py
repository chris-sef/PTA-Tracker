import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
import tkinter.messagebox as messagebox
import csv
import pandas as pd
import datetime
import os

def save_to_csv(data):
    try:
        file_path = "data.csv"  

        fieldnames = ['Date', 'ID Number', 'Name', 'Payment Status']
        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if os.stat(file_path).st_size == 0:
                writer.writeheader()
            writer.writerow(data)
        messagebox.showinfo("Success", "Data saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def export_to_excel():
    try:
        df = pd.read_csv('data.csv')
        
        # Open a file dialog for the user to specify the file path
        file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", "Data exported to Excel successfully!")
        else:
            messagebox.showwarning("Warning", "Export canceled by user.")
            
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def clear_fields():
    date_entry.set_date(datetime.date.today())
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    payment_status_var.set("Paid")

def validate_input():
    if not date_entry.get() or not id_entry.get() or not name_entry.get():
        messagebox.showerror("Error", "Please fill in all required fields.")
        return False
    return True

def submit():
    if validate_input():
        data = {
            'Date': date_entry.get(),
            'ID Number': id_entry.get(),
            'Name': name_entry.get(),
            'Payment Status': payment_status_var.get()
        }
        save_to_csv(data)
        clear_fields()

# Create the main window
root = tk.Tk()
root.title("Payment Tracker")
root.geometry('300x250')
root.minsize(300, 250)

# Define styles
style = ttk.Style(root)
style.configure('TLabel', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12))
style.configure('TCombobox', font=('Arial', 12))
style.configure('TEntry', font=('Arial', 12))

# Create frames
input_frame = ttk.Frame(root, padding="10 10 10 10")
input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
input_frame.columnconfigure(0, weight=1)
input_frame.columnconfigure(1, weight=1)

button_frame = ttk.Frame(root, padding="10 10 10 10")
button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create input fields
date_label = ttk.Label(input_frame, text="Date:")
date_entry = DateEntry(input_frame, selectmode='day', date_pattern='mm-dd-yyyy')
date_entry.set_date(datetime.date.today())

id_label = ttk.Label(input_frame, text="ID Number:")
id_entry = ttk.Entry(input_frame)

name_label = ttk.Label(input_frame, text="Name:")
name_entry = ttk.Entry(input_frame)

payment_status_label = ttk.Label(input_frame, text="Payment Status:")
payment_status_var = tk.StringVar(value="Paid")
payment_status_combobox = ttk.Combobox(input_frame, textvariable=payment_status_var, values=["Paid", "Unpaid"])

# Create buttons
submit_button = ttk.Button(button_frame, text="Submit", command=submit)
clear_button = ttk.Button(button_frame, text="Clear", command=clear_fields)
export_button = ttk.Button(button_frame, text="Export to Excel", command=export_to_excel)

# Grid layout
date_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
date_entry.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
id_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
id_entry.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
name_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
name_entry.grid(row=2, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
payment_status_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
payment_status_combobox.grid(row=3, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

submit_button.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
clear_button.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
export_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))

root.mainloop()
