import tkinter as tk
from tkinter import messagebox
import csv

# Function to validate date format
def validate_date(date):
  try:
    from datetime import datetime
    datetime.strptime(date, '%m-%d-%Y')
    return True
  except ValueError:
    return False

# Function to save data to CSV
def save_data():
  date = entry_date.get()
  name = entry_name.get()
  payment_status = var_payment.get()
  amount_paid = entry_amount.get()

  # Input validation
  if not date or not name or not payment_status:
    messagebox.showerror("Error", "Please fill all required fields!")
    return

  if not validate_date(date):
    messagebox.showerror("Error", "Invalid date format! Use MM-DD-YYYY")
    return

  if payment_status == "Partial Payment" and not amount_paid:
    messagebox.showerror("Error", "Please enter amount paid for partial payment!")
    return

  try:
    amount_paid = float(amount_paid)
  except ValueError:
    messagebox.showerror("Error", "Invalid amount! Please enter a number.")
    return

  # Open CSV file in append mode
  with open("transactions.csv", 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([date, name, payment_status, amount_paid])

  # Clear fields and show success message
  entry_date.delete(0, tk.END)
  entry_name.delete(0, tk.END)
  var_payment.set("Select Payment Status")
  entry_amount.delete(0, tk.END)
  messagebox.showinfo("Success", "Data saved successfully!")

# Function to clear input fields
def clear_data():
  entry_date.delete(0, tk.END)
  entry_name.delete(0, tk.END)
  var_payment.set("Select Payment Status")
  entry_amount.delete(0, tk.END)

# Function to open CSV file
def view_data():
  try:
    import os
    os.startfile("transactions.csv")
  except FileNotFoundError:
    messagebox.showinfo("Info", "No data found. Please add some transactions first!")

# Create main window
window = tk.Tk()
window.title("Transaction Tracker")
window.geometry("380x220")  # Set initial window size
window.configure(padx=20, pady=5)  # Add padding around elements

# Create font styles
font_label = ("Times New Roman", 12, "bold")
font_entry = ("Times New Roman", 12)
font_button = ("Times New Roman", 12, "bold")

# Create labels and entry fields with styling
label_date = tk.Label(window, text="Date (MM-DD-YYYY):", font=font_label)
label_date.grid(row=0, column=0, sticky="W")  # Align left
entry_date = tk.Entry(window, width=20, font=font_entry)
entry_date.grid(row=0, column=1, padx=5)

label_name = tk.Label(window, text="Name:", font=font_label)
label_name.grid(row=1, column=0, sticky="W")
entry_name = tk.Entry(window, width=20, font=font_entry)
entry_name.grid(row=1, column=1, padx=5)

label_payment = tk.Label(window, text="Payment Status:", font=font_label)
label_payment.grid(row=2, column=0, sticky="W")

var_payment = tk.StringVar(window)
var_payment.set("Select Payment Status")
payment_options = ["Select Payment Status", "Paid", "Partial Payment"]
payment_menu = tk.OptionMenu(window, var_payment, *payment_options)
payment_menu.grid(row=2, column=1, padx=5)

label_amount = tk.Label(window, text="Amount Paid:", font=font_label)
label_amount.grid(row=3, column=0, sticky="W")
entry_amount = tk.Entry(window, width=20, font=font_entry)
entry_amount.grid(row=3, column=1, padx=5)

# Create buttons with styling
button_save = tk.Button(window, text="Save", font=font_button, command=save_data)
button_save.grid(row=4, column=0, pady=10, sticky="E")  # Align right

button_clear = tk.Button(window, text="Clear", font=font_button, command=clear_data)
button_clear.grid(row=4, column=1, padx=5, sticky="W")  # Align left

button_view = tk.Button(window, text="View Data", font=font_button, command=view_data)
button_view.grid(row=5, columnspan=2, pady=10)  # Span across two columns

# Run the main loop
window.mainloop()