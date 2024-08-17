from tkinter import *
from tkinter import messagebox
import datetime
from csv import writer

# Function to validate date format
def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m-%d-%Y')
        return True
    except ValueError:
        return False

# Function to validate payment and amount paid
def validate_payment(payment_status, amount_paid):
    if payment_status == "Paid" and amount_paid != "":
        return False
    elif payment_status == "Partial Payment" and amount_paid == "":
        return False
    else:
        return True

# Function to clear input fields
def clear_fields():
    name_entry.delete(0, END)
    id_entry.delete(0, END)
    amount_entry.delete(0, END)
    payment_var.set("Paid")
    amount_entry.config(state=DISABLED)

# Function to save data to CSV
def save_data():
    name = name_entry.get()
    id_number = id_entry.get()
    payment_status = payment_var.get()
    amount_paid = amount_entry.get()
    date_today = datetime.date.today().strftime('%m-%d-%Y')

    # Validate user input
    if not all([name, id_number, payment_status]):
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    if not validate_date(date_today):
        messagebox.showerror("Error", "Invalid date format. Please use MM-DD-YYYY.")
        return

    if not validate_payment(payment_status, amount_paid):
        messagebox.showerror("Error", "Payment validation failed. Check payment status and amount.")
        return

    # Write data to CSV
    with open("transaction_data.csv", "a", newline="") as csvfile:
        writer(csvfile).writerow([date_today, name, id_number, payment_status, amount_paid])

    # Clear fields and show success message
    clear_fields()
    messagebox.showinfo("Success", "Data saved successfully!")

# Function to open the CSV file
def view_data():
    try:
        os.startfile("transaction_data.csv")
    except FileNotFoundError:
        messagebox.showinfo("Information", "No data found. Please save some data first.")
    except:
        messagebox.showerror("Error", "Failed to open file. Please check file permissions.")

# Initialize main window
window = Tk()
window.title("Transaction Tracker")
window.geometry("300x220")

# Create labels and input fields

name_label = Label(window, text="Name:")
name_label.grid(row=0, column=0, pady=5)  
name_entry = Entry(window)
name_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

id_label = Label(window, text="ID Number:")
id_label.grid(row=1, column=0, pady=5) 
id_entry = Entry(window)
id_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

payment_label = Label(window, text="Payment Status:")
payment_label.grid(row=2, column=0, pady=5) 

payment_var = StringVar(window)
payment_var.set("Paid")  # Default selection

payment_menu = OptionMenu(window, payment_var, "Paid", "Partial Payment")
payment_menu.grid(row=2, column=1, pady=5) 

amount_label = Label(window, text="Amount Paid:")
amount_label.grid(row=3, column=0, pady=5)  
amount_entry = Entry(window, state=DISABLED)  # Initially disabled
amount_entry.grid(row=3, column=1, pady=5)


# Function to enable amount entry when partial payment is selected
def enable_amount_entry(payment_status):
    if payment_status == "Partial Payment":
        amount_entry.config(state=NORMAL)
    else:
        amount_entry.config(state=DISABLED)

payment_var.trace_add("write", lambda *args: enable_amount_entry(payment_var.get()))  # Update on selection change

# Create buttons
clear_button = Button(window, text="Clear", command=clear_fields)
clear_button.grid(row=5, column=0, pady=10)

save_button = Button(window, text="Save", command=save_data)
save_button.grid(row=5, column=1, pady=10)

view_button = Button(window, text="View Data", command=view_data)
view_button.grid(row=5, column=2, pady=10)

# Run main loop
window.mainloop()