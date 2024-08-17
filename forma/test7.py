import tkinter as tk
from tkinter import ttk
import pandas as pd
import csv
from tkcalendar import DateEntry
import tkintertable as ttk
from tkintertable import TableCanvas, TableModel

class DataEntry:
    def __init__(self, date, id_number, name, payment_status):
        self.date = date
        self.id_number = id_number
        self.name = name
        self.payment_status = payment_status

class App:
    def __init__(self, master):
        self.master = master
        master.title("Data Entry App")

        # Data
        self.data = []

        # GUI elements
        self.date_label = ttk.Label(master, text="Date:")
        self.date_entry = DateEntry(root, date_pattern='mm-dd-yyyy')
        self.id_label = ttk.Label(master, text="ID Number:")
        self.id_entry = ttk.Entry(master)
        self.name_label = ttk.Label(master, text="Name:")
        self.name_entry = ttk.Entry(master)
        self.payment_status_label = ttk.Label(master, text="Payment Status:")
        self.payment_status_var = tk.StringVar(value="Paid")
        self.payment_status_dropdown = ttk.Combobox(master, textvariable=self.payment_status_var, values=["Paid", "Unpaid"])

        self.save_button = ttk.Button(master, text="Save", command=self.save_data)
        self.clear_button = ttk.Button(master, text="Clear", command=self.clear_fields)
        self.export_button = ttk.Button(master, text="Export to Excel", command=self.export_to_excel)

        self.table_frame = ttk.Frame(master)
        self.table_model = TableModel()
        self.table_canvas = TableCanvas(self.table_frame, model=self.table_model)
        self.table_canvas.pack(fill="both", expand=True)

        # Layout
        self.date_label.grid(row=0, column=0, padx=5, pady=5)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.id_label.grid(row=1, column=0, padx=5, pady=5)
        self.id_entry.grid(row=1, column=1, padx=5, pady=5)
        self.name_label.grid(row=2, column=0, padx=5, pady=5)
        self.name_entry.grid(row=2, column=1, padx=5, pady=5)
        self.payment_status_label.grid(row=3, column=0, padx=5, pady=5)
        self.payment_status_dropdown.grid(row=3, column=1, padx=5, pady=5)
        self.save_button.grid(row=4, column=0, padx=5, pady=5)
        self.clear_button.grid(row=4, column=1, padx=5, pady=5)
        self.export_button.grid(row=4, column=2, padx=5, pady=5)
        self.table_frame.grid(row=5, column=0, columnspan=3)
        self.table_model = TableModel()
        self.table_canvas = TableCanvas(self.table_frame, model=self.table_model)
        self.table_canvas.pack(fill="both", expand=True)

        # Load data from CSV
        self.load_data()

    def save_data(self):
        try:
            date = self.date_entry.get()
            id_number = self.id_entry.get()
            name = self.name_entry.get()
            payment_status = self.payment_status_var.get()

            if not date or not id_number or not name:
                tk.messagebox.showerror("Error", "Please fill in all required fields.")
                return

            data_entry = DataEntry(date, id_number, name, payment_status)
            self.data.append(data_entry)

            # Append to CSV
            with open("data.csv", "a", newline="") as csvfile:
                fieldnames = ["date", "id_number", "name", "payment_status"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(data_entry.__dict__)

            tk.messagebox.showinfo("Success", "Data saved successfully.")
            self.clear_fields()
            self.load_data()
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_fields(self):
        self.date_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.payment_status_var.set("Paid")

    def load_data(self):
        try:
            self.data = []
            with open("data.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data_entry = DataEntry(row["date"], row["id_number"], row["name"], row["payment_status"])
                    self.data.append(data_entry)

            # Populate table
            for row in range(self.table_model.getRowCount()):
                self.table_model.delRow(0)
            for index, entry in enumerate(self.data):
                self.table_model.addRow(index)
                for column, value in entry.__dict__.items():
                    self.table_model.setValue(index, column, value)
        except FileNotFoundError:
            pass  # Handle file not found

    def export_to_excel(self):
        try:
            df = pd.DataFrame([(d.date, d.id_number, d.name, d.payment_status) for d in self.data], columns=["Date", "ID Number", "Name", "Payment Status"])
            df.to_excel("data.xlsx", index=False)
            tk.messagebox.showinfo("Success", "Data exported to Excel successfully.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")


root = tk.Tk()
app = App(root)
root.mainloop()
