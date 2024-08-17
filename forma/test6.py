import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import pandas as pd
import os
from tkintertable import TableCanvas, TableModel

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Transaction Manager")
        
        # Create the input fields
        tk.Label(root, text="Date of Transaction (MM-DD-YYYY):").grid(row=0, column=0)
        self.date_entry = DateEntry(root, date_pattern='mm-dd-yyyy')
        self.date_entry.grid(row=0, column=1)
        
        tk.Label(root, text="ID Number:").grid(row=1, column=0)
        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=1, column=1)
        
        tk.Label(root, text="Name:").grid(row=2, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=2, column=1)
        
        tk.Label(root, text="Payment Status:").grid(row=3, column=0)
        self.payment_status = tk.StringVar(value="Paid")
        self.payment_status_entry = tk.Entry(root, textvariable=self.payment_status)
        self.payment_status_entry.grid(row=3, column=1)
        
        # Create buttons
        self.save_button = tk.Button(root, text="Save", command=self.save_entry)
        self.save_button.grid(row=4, column=0)
        
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_entries)
        self.clear_button.grid(row=4, column=1)
        
        self.export_button = tk.Button(root, text="Export to Excel", command=self.export_to_excel)
        self.export_button.grid(row=4, column=2)
        
        # Initialize the data grid
        self.create_data_grid()
        self.load_data()
        
    def save_entry(self):
        date = self.date_entry.get()
        id_number = self.id_entry.get()
        name = self.name_entry.get()
        payment_status = self.payment_status_entry.get()
        
        if not date or not id_number or not name or not payment_status:
            messagebox.showerror("Error", "All fields must be filled.")
            return
        
        try:
            pd.to_datetime(date, format='%m-%d-%Y')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format.")
            return
        
        if not id_number.isdigit():
            messagebox.showerror("Error", "ID number must be numeric.")
            return
        
        self.append_to_csv(date, id_number, name, payment_status)
        messagebox.showinfo("Success", "Data saved successfully.")
        self.clear_entries()
        self.load_data()

    def append_to_csv(self, date, id_number, name, payment_status):
        file_exists = os.path.isfile('transactions.csv')
        data = pd.DataFrame([[date, id_number, name, payment_status]],
                            columns=['Date', 'ID', 'Name', 'Payment Status'])
        if file_exists:
            data.to_csv('transactions.csv', mode='a', header=False, index=False)
        else:
            data.to_csv('transactions.csv', mode='w', header=True, index=False)
        
    def clear_entries(self):
        self.date_entry.set_date("")
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.payment_status_entry.delete(0, tk.END)
        self.payment_status.set("Paid")
        
    def export_to_excel(self):
        if not os.path.isfile('transactions.csv'):
            messagebox.showerror("Error", "No data available to export.")
            return
        
        data = pd.read_csv('transactions.csv')
        data.to_excel('transactions.xlsx', index=False)
        messagebox.showinfo("Success", "Data exported to transactions.xlsx.")
        
    def create_data_grid(self):
        frame = tk.Frame(self.root)
        frame.grid(row=5, column=0, columnspan=3)
        self.table_model = TableModel()
        self.table = TableCanvas(frame, model=self.table_model)
        self.table.show()

    def load_data(self):
        if os.path.isfile('transactions.csv'):
            data = pd.read_csv('transactions.csv')
            # Convert the DataFrame to a dictionary with column names as keys and lists of column data as values
            data_dict = {col: list(data[col]) for col in data.columns}
            self.table_model.importDict(data_dict)
            self.table.redraw()

root = tk.Tk()
app = App(root)
root.mainloop()
