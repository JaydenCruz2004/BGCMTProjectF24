## BGCMT FALL 2024 Project
## Created: Jayden Cruz
##  

import googlemaps
import googlemaps
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime
from tkinter import ttk


class LogisticsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Logistics BGCMT System")

        # Variables
        self.df = None
        self.totalDevices = 120
        self.total_devices_needed = 0

        # Frame for buttons and file input
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        # File input label and entry
        self.path_label = tk.Label(self.frame, text="Enter CSV file path:")
        self.path_label.grid(row=0, column=0, padx=10, pady=5)

        self.path_entry = tk.Entry(self.frame, width=40)
        self.path_entry.grid(row=0, column=1, padx=10, pady=5)

        # File selection button
        self.load_button = tk.Button(self.frame, text="Load CSV File", command=self.load_file)
        self.load_button.grid(row=0, column=2, padx=10, pady=5)

        # Display logistics button
        self.display_button = tk.Button(self.frame, text="Display Logistics Plan", command=self.print_logistics_plan, state=tk.DISABLED)
        self.display_button.grid(row=1, column=0, padx=10, pady=5)

        # Check overlap button
        self.check_overlap_button = tk.Button(self.frame, text="Check Overlap", command=self.check_overlap, state=tk.DISABLED)
        self.check_overlap_button.grid(row=1, column=1, padx=10, pady=5)

        # Treeview for displaying logistics table
        self.tree = ttk.Treeview(self.root, columns=("School_Name", "Address", "Devices_Needed", "Start_Time", "End_Time"), show="headings")
        self.tree.pack(padx=20, pady=20)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Overlap selection dropdown
        self.school1_label = tk.Label(self.root, text="Select first school:")
        self.school1_label.pack(padx=20, pady=5)
        self.school1_combobox = ttk.Combobox(self.root, state="readonly")
        self.school1_combobox.pack(padx=20, pady=5)

        self.school2_label = tk.Label(self.root, text="Select second school:")
        self.school2_label.pack(padx=20, pady=5)
        self.school2_combobox = ttk.Combobox(self.root, state="readonly")
        self.school2_combobox.pack(padx=20, pady=5)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(padx=20, pady=20)

    def load_file(self):
        # Get file path from the entry widget
        file_path = self.path_entry.get()

        if file_path:
            try:
                # Load CSV data into DataFrame
                self.df = pd.read_csv(file_path)

                # Check if required columns exist
                required_columns = ["School_Name", "Address", "Devices_Needed", "Start_Time", "End_Time"]
                if not all(col in self.df.columns for col in required_columns):
                    messagebox.showerror("Column Error", "CSV is missing required columns.")
                    return

                # Convert times to datetime
                self.df['Start_Time'] = pd.to_datetime(self.df['Start_Time'], format='%H:%M')
                self.df['End_Time'] = pd.to_datetime(self.df['End_Time'], format='%H:%M')

                # Calculate total devices needed
                self.total_devices_needed = self.df["Devices_Needed"].sum()

                # Populate the treeview with data
                for row in self.df.itertuples():
                    self.tree.insert("", "end", values=(row.School_Name, row.Address, row.Devices_Needed, row.Start_Time.strftime('%H:%M'), row.End_Time.strftime('%H:%M')))

                # Populate the comboboxes with school names
                schools = self.df["School_Name"].unique()
                self.school1_combobox['values'] = schools
                self.school2_combobox['values'] = schools

                # Update buttons
                self.display_button.config(state=tk.NORMAL)
                self.check_overlap_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("File Error", f"Failed to load file: {e}")
        else:
            messagebox.showwarning("Input Error", "Please enter the file path.")

    def is_overlapping(self, schedule1, schedule2):
        # Check if times overlap
        return not (schedule1['End_Time'] <= schedule2['Start_Time'] or schedule1['Start_Time'] >= schedule2['End_Time'])

    def check_overlap(self):
        school1_name = self.school1_combobox.get()
        school2_name = self.school2_combobox.get()

        if school1_name and school2_name:
            school1 = self.df[self.df['School_Name'] == school1_name].iloc[0]
            school2 = self.df[self.df['School_Name'] == school2_name].iloc[0]

            if self.is_overlapping(school1, school2):
                self.result_label.config(text=f"{school1['School_Name']} and {school2['School_Name']} have overlapping schedules.", fg="red")
            else:
                self.result_label.config(text=f"{school1['School_Name']} and {school2['School_Name']} do not have overlapping schedules.", fg="green")
        else:
            messagebox.showwarning("Selection Error", "Please select two schools to check overlap.")

    def print_logistics_plan(self):
        plan = ""
        for _, row in self.df.iterrows():
            plan += f"{row['School_Name']} at {row['Address']} needs {row['Devices_Needed']} devices from {row['Start_Time'].strftime('%H:%M')} to {row['End_Time'].strftime('%H:%M')}\n"

        plan += f"\nTotal devices needed: {self.total_devices_needed}"

        # If total devices needed exceeds total available, allocate shared devices
        if self.total_devices_needed > self.totalDevices:
            plan += "\n\nAllocating devices between sites with proximity and schedule considerations..."

        # Show the logistics plan in a new window
        top = tk.Toplevel(self.root)
        top.title("Logistics Plan")
        text_box = tk.Text(top, width=80, height=20)
        text_box.insert(tk.END, plan)
        text_box.pack(padx=10, pady=10)


def main():
    root = tk.Tk()
    gui = LogisticsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
