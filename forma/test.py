import csv
from tkinter import *

# Function to get user info
def get_user_info():
  name = name_entry.get()
  payment_status = payment_var.get().upper()
  return name, payment_status

# Function to save data
def save_data():
  name, payment_status = get_user_info()
  # Check for empty fields
  if not name or not payment_status:
    message_label.config(text="Please fill all fields!", fg="red")
    return
  
  # Open CSV file in append mode
  with open("user_data.csv", "a", newline="") as csvfile:
    writer = csv.writer(csvfile)
    # Check if file is empty, write headers if needed
    if csvfile.tell() == 0:
      writer.writerow(["Name", "Payment Status"])
    # Write user data to CSV
    writer.writerow([name, payment_status])
  message_label.config(text="Data saved successfully!", fg="green")
  # Clear entry fields
  name_entry.delete(0, END)
  payment_var.set("")

# Main GUI
root = Tk()
root.title("User Data Input")
root.geometry("300x150")

# Name label and entry
name_label = Label(root, text="Name:")
name_label.pack(pady=10)
name_entry = Entry(root)
name_entry.pack(pady=5)

# Payment status options
payment_var = StringVar()
payment_var.set("Select Status")
payment_options = OptionMenu(root, payment_var, "Paid", "Not Paid")
payment_options.pack(pady=5)

# Save button
save_button = Button(root, text="Save", command=save_data)
save_button.pack(pady=10)

# Message label
message_label = Label(root, text="")
message_label.pack()

root.mainloop()