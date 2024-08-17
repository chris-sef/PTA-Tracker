import tkinter
from tkinter import Tk, ttk, messagebox
import datetime
import csv

def clear_fields():
  """Clears all input fields"""
  for widget in window.children.values():
    if isinstance(widget, ttk.Entry):
      widget.delete(0, 'end')

def save_data():
  """Saves data to CSV file with validations"""
  try:
    query = query_entry.get().strip()
    name = name_entry.get().strip()
    payment_status = payment_var.get()
    amount_paid = amount_entry.get().strip()

    if not query or not name or not payment_status:
      raise ValueError("Please fill in all required fields.")

    if payment_status == "Partial Payment" and not amount_paid:
      raise ValueError("Amount Paid is required for Partial Payment.")

    amount_paid = float(amount_paid) if amount_paid else None

    data = {
      "Date": today.strftime("%m-%d-%Y"),
      "ID": id_entry.get().strip(),
      "Query": query,
      "Name": name,
      "Payment Status": payment_status,
      "Amount Paid": amount_paid
    }

    with open("data.csv", "a", newline='') as file:
      writer = csv.DictWriter(file, fieldnames=data.keys())
      if not file.tell():
        writer.writeheader()
      writer.writerow(data)

    messagebox.showinfo("Success", "Data saved successfully!")
    clear_fields()
  except ValueError as e:
    messagebox.showerror("Error", str(e))

def view_data():
  """Opens the CSV file"""
  try:
    import os
    os.startfile("data.csv")
  except FileNotFoundError:
    messagebox.showinfo("Info", "No data found. Please add some entries first.")

today = datetime.date.today()

window = Tk()
window.title("Transaction Tracker")

# Style configuration for theme
style = ttk.Style()
style.theme_create("custom", settings={
    ". ttk.Entry": {"foreground": "black", "background": "lightgray"},
    ". ttk.Radiobutton": {"foreground": "black"},
    ". ttk.Label": {"foreground": "black"}
})
style.theme_use("custom")

# ID Label
id_label = ttk.Label(window, text="ID:")
id_label.grid(row=0, column=0, pady=5)

# ID Entry
id_entry = ttk.Entry(window)
id_entry.grid(row=0, column=1, padx=5)

# Query Label
query_label = ttk.Label(window, text="Query:")
query_label.grid(row=1, column=0, pady=5)

# Query Entry
query_entry = ttk.Entry(window)
query_entry.grid(row=1, column=1, padx=5)

# Name Label
name_label = ttk.Label(window, text="Name:")
name_label.grid(row=2, column=0, pady=5)

# Name Entry
name_entry = ttk.Entry(window)
name_entry.grid(row=2, column=1, padx=5)

# Payment Status Label
payment_label = ttk.Label(window, text="Payment Status:")
payment_label.grid(row=3, column=0, pady=5)

# Payment Status Radio buttons with variable
payment_var = tkinter.StringVar()
payment_var.set("Paid")  # Set default

paid_radio = ttk.Radiobutton(window, text="Paid", variable=payment_var, value="Paid")
paid_radio.grid(row=3, column=1, sticky="w")

partial_radio = ttk.Radiobutton(window, text="Partial Payment", variable=payment_var, value="Partial Payment")
partial_radio.grid(row=3, column=2, sticky="w")

# Amount Paid Label (disabled initially)
amount_label = ttk.Label(window, text="Amount Paid:")
amount_label.grid(row=4, column=0, pady=5)

# Amount Paid Entry (disabled initially)
amount_entry = ttk.Entry(window, state="disabled")
amount_entry.grid(row=4, column=1, padx=5)

# Enable/Disable Amount Paid entry based on payment selection
def update_amount_state():
  payment_status = payment_var.get()
  amount_label.config(state=payment_status == "Partial Payment" and "normal" or "disabled")
  amount_entry.config(state=payment_status == "Partial Payment" and "normal" or "disabled")

payment_var.trace_add("write", update_amount_state)  # Update on selection change

# Save Button
save_button = ttk.Button(window, text="Save", command=save_data)
save_button.grid(row=5, column=0, pady=5)

# Clear Button
clear_button = ttk.Button(window, text="Clear", command=clear_fields)
clear_button.grid(row=5, column=1, pady=5)

# View Data Button
view_data_button = ttk.Button(window, text="View Data", command=view_data)
view_data_button.grid(row=5, column=2, pady=5)

# Run the main loop
window.mainloop()