import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from fpdf import FPDF

def load_excel(file_path):
    try:
        data = pd.read_excel(file_path)
        if 'Date' not in data.columns:
            raise ValueError("Excel file must contain a 'Date' column.")
        return data
    except Exception as e:
        raise ValueError(f"Error loading Excel file: {e}")

def filter_transactions(data, start_date, end_date):
    data['Date'] = pd.to_datetime(data.iloc[:, 0])
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.min.time())
    filtered_data = data[(data['Date'] >= start_datetime) & (data['Date'] <= end_datetime)]
    return filtered_data

def generate_report(filtered_data):
    report = filtered_data.groupby(filtered_data['Date'].dt.date).size()
    return report

class TransactionReportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Report Generator")
        self.root.geometry("700x560")
        self.create_widgets()
    
    def create_widgets(self):
        # Styling
        style = ttk.Style(self.root)
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 10))
        style.configure('TDateEntry', font=('Arial', 10))
        
        # File selection
        self.file_label = ttk.Label(self.root, text="Select Excel File:")
        self.file_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.file_entry = ttk.Entry(self.root, width=50)
        self.file_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.browse_button = ttk.Button(self.root, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        
        # Date range selection
        self.start_date_label = ttk.Label(self.root, text="Start Date:")
        self.start_date_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.start_date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.start_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        self.end_date_label = ttk.Label(self.root, text="End Date:")
        self.end_date_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.end_date_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.end_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        # Buttons
        self.generate_button = ttk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.generate_button.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        
        self.clear_button = ttk.Button(self.root, text="Clear", command=self.clear_fields)
        self.clear_button.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        self.save_button = ttk.Button(self.root, text="Save Report", command=self.save_report)
        self.save_button.grid(row=3, column=2, padx=10, pady=10, sticky='w')
        
        self.chart_button = ttk.Button(self.root, text="Show Chart", command=self.show_chart)
        self.chart_button.grid(row=3, column=3, padx=10, pady=10, sticky='w')
        
        # Report display
        self.report_text = tk.Text(self.root, width=80, height=20)
        self.report_text.grid(row=4, column=0, columnspan=4, padx=10, pady=10)
        
        # Tooltips
        self.create_tooltips()
    
    def create_tooltips(self):
        tooltips = {
            self.browse_button: "Click to select an Excel file",
            self.start_date_entry: "Select the start date for filtering transactions",
            self.end_date_entry: "Select the end date for filtering transactions",
            self.generate_button: "Generate the transaction report based on selected dates",
            self.clear_button: "Clear all inputs and the report",
            self.save_button: "Save the generated report as a PDF file",
            self.chart_button: "Show a bar chart of the transactions"
        }
        for widget, text in tooltips.items():
            ToolTip(widget, text)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)
    
    def generate_report(self):
        file_path = self.file_entry.get()
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        
        if not file_path:
            messagebox.showwarning("Input Error", "Please select an Excel file.")
            return
        
        if start_date > end_date:
            messagebox.showwarning("Date Error", "Start date cannot be after end date.")
            return
        
        try:
            data = load_excel(file_path)
            filtered_data = filter_transactions(data, start_date, end_date)
            report = generate_report(filtered_data)
            
            self.report_text.delete(1.0, tk.END)
            if report.empty:
                self.report_text.insert(tk.END, "No transactions found for the selected date range.")
            else:
                total_transactions = report.sum()
                report_str = f"Transaction Report\n\n"
                report_str += f"Date Range: {start_date} to {end_date}\n"
                report_str += "Date        | Number of Transactions\n"
                report_str += "-"*35 + "\n"
                report_str += report.to_string(header=False)
                report_str += f"\n\nTotal Transactions: {total_transactions}"
                self.report_text.insert(tk.END, report_str)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def clear_fields(self):
        self.file_entry.delete(0, tk.END)
        self.start_date_entry.set_date(datetime.now())
        self.end_date_entry.set_date(datetime.now())
        self.report_text.delete(1.0, tk.END)
    
    def save_report(self):
        report_text = self.report_text.get(1.0, tk.END)
        if report_text.strip():
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
            if file_path:
                self.create_pdf_report(file_path, report_text)
                messagebox.showinfo("Success", "Report saved successfully.")
        else:
            messagebox.showwarning("Save Error", "No report to save.")
    
    def create_pdf_report(self, file_path, report_text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        lines = report_text.split('\n')
        for line in lines:
            pdf.cell(200, 10, txt=line, ln=True)
        
        pdf.output(file_path)
    
    def show_chart(self):
        file_path = self.file_entry.get()
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        
        if not file_path:
            messagebox.showwarning("Input Error", "Please select an Excel file.")
            return
        
        try:
            data = load_excel(file_path)
            filtered_data = filter_transactions(data, start_date, end_date)
            report = generate_report(filtered_data)
            
            if report.empty:
                messagebox.showinfo("No Data", "No transactions found for the selected date range.")
            else:
                report.plot(kind='bar')
                plt.xlabel('Date')
                plt.ylabel('Number of Transactions')
                plt.title('Transactions Over Time')
                plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.tooltip = None
    
    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(self.tooltip, text=self.text, relief='solid', borderwidth=1, wraplength=200)
        label.pack(ipadx=1)
    
    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
        self.tooltip = None

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TransactionReportApp(root)
    root.mainloop()
