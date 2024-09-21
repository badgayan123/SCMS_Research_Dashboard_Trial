import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter import font as tkfont

# Directory to store data
DATA_DIR = 'D:/publication'
os.makedirs(DATA_DIR, exist_ok=True)

FACULTY_NAMES = {
    'aarti123': 'Dr. Aarti Mehta Sharma',
    'chandan123': 'Dr. Chandan',
    'nikita123': 'Dr. Nikita',
    'anandita123': 'Dr. Anandita',
    'sivaretinamohan123': 'Dr. Sivaretinamohan',
    'shanmugha123': 'Dr. Shanmugha',
    'meenakshi123': 'Dr. Meenakshi',
    'seeboli123': 'Dr. Seeboli',
    'nitesh123': 'Dr. Nitesh',
    'poornima123': 'Dr. Poornima'
}

def get_paper_details(count):
    papers = []
    for i in range(count):
        title = askstring("Input", f"Enter title of paper {i + 1}:")
        if title:
            journal = askstring("Input", f"Enter journal for paper {i + 1}:")
            if journal:
                impact_factor = askstring("Input", f"Enter impact factor for paper {i + 1} (if any):")
                papers.append({
                    'Title': title,
                    'Journal': journal,
                    'Impact Factor': impact_factor if impact_factor else 'N/A'
                })
    return papers

def save_data_to_csv(author, year, month, communicated, communicated_details):
    filename = os.path.join(DATA_DIR, f"{year}_{month}.csv")
    data = {
        'Author': [author],
        'Year': [year],
        'Month': [month],
        'Communicated': [communicated]
    }
    df = pd.DataFrame(data)

    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    # Save communicated details to a separate file
    details_filename = os.path.join(DATA_DIR, f"{year}_{month}_details.csv")
    details_df = pd.DataFrame(communicated_details)
    details_df.to_csv(details_filename, index=False)

    messagebox.showinfo("Success", "Data saved locally successfully!")

def save_data():
    author = faculty_combobox.get()
    year = year_combobox.get()
    month = month_combobox.get()
    communicated = int(communicated_entry.get())

    if communicated > 0:
        communicated_details = get_paper_details(communicated)
        if communicated_details:
            save_data_to_csv(author, year, month, communicated, communicated_details)
        else:
            messagebox.showinfo("Info", "No details were provided for the communicated papers.")
    else:
        messagebox.showerror("Error", "Please enter a valid number of communicated papers.")

# Tkinter App Setup
root = tk.Tk()
root.title("SCMS Faculty Dashboard")

# Set up font and colors
default_font = tkfont.Font(family="Helvetica", size=12)
header_font = tkfont.Font(family="Helvetica", size=14, weight="bold")

# Center align widgets in the window
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(5, weight=1)
root.rowconfigure(6, weight=1)
root.rowconfigure(7, weight=1)
root.rowconfigure(8, weight=1)

# Welcome Label
tk.Label(root, text="Welcome to SCMS Faculty Dashboard", font=header_font, pady=10).grid(row=0, column=0, columnspan=2, sticky='n')

# Faculty Details
tk.Label(root, text="Select Faculty Name", font=default_font).grid(row=1, column=0, padx=10, pady=5, sticky='e')
faculty_combobox = ttk.Combobox(root, values=list(FACULTY_NAMES.values()))
faculty_combobox.grid(row=1, column=1, padx=10, pady=5, sticky='w')

# Year and Month Selection
tk.Label(root, text="Select Year", font=default_font).grid(row=2, column=0, padx=10, pady=5, sticky='e')
year_combobox = ttk.Combobox(root, values=list(range(2024, 2051)))
year_combobox.grid(row=2, column=1, padx=10, pady=5, sticky='w')

tk.Label(root, text="Select Month", font=default_font).grid(row=3, column=0, padx=10, pady=5, sticky='e')
month_combobox = ttk.Combobox(root, values=["January", "February", "March", "April", "May", "June",
                                            "July", "August", "September", "October", "November", "December"])
month_combobox.grid(row=3, column=1, padx=10, pady=5, sticky='w')

# Publication Details
tk.Label(root, text="Communicated", font=default_font).grid(row=4, column=0, padx=10, pady=5, sticky='e')
communicated_entry = tk.Entry(root)
communicated_entry.grid(row=4, column=1, padx=10, pady=5, sticky='w')

# Buttons
tk.Button(root, text="Save Data", command=save_data, font=default_font, bg='lightblue').grid(row=7, column=0, columnspan=2, pady=10, sticky='n')

root.mainloop()
