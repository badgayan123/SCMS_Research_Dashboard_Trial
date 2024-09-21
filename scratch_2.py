import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
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

def save_data_to_csv(author, year, month, communicated, accepted, published):
    filename = os.path.join(DATA_DIR, f"{year}_{month}.csv")
    data = {
        'Author': [author],
        'Year': [year],
        'Month': [month],
        'Communicated': [communicated],
        'Accepted': [accepted],
        'Published': [published]
    }
    df = pd.DataFrame(data)

    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

    messagebox.showinfo("Success", "Data saved locally successfully!")

def load_data_from_csv(year, month):
    filename = os.path.join(DATA_DIR, f"{year}_{month}.csv")
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        return df
    else:
        messagebox.showinfo("Info", "No data available for the selected year and month.")
        return pd.DataFrame()

def plot_visualizations():
    year = year_combobox.get()
    month = month_combobox.get()
    df = load_data_from_csv(year, month)

    if not df.empty:
        fig, ax = plt.subplots(1, 2, figsize=(14, 7))

        # Bar Graph
        bar_data = df.groupby('Author').sum().reset_index()
        bar_data.plot(kind='bar', x='Author', y=['Communicated', 'Accepted', 'Published'], ax=ax[0], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        ax[0].set_title('Total Publications by Faculty')
        ax[0].set_ylabel('Count')
        ax[0].set_xlabel('Faculty')
        ax[0].legend(title='Publication Types')
        ax[0].tick_params(axis='x', rotation=90)  # Rotate x-axis labels by 90 degrees

        # Pie Chart
        pie_data = df.groupby('Author').sum().reset_index()
        pie_data['Total'] = pie_data[['Communicated', 'Accepted', 'Published']].sum(axis=1)
        ax[1].pie(pie_data['Total'], labels=pie_data['Author'], autopct='%1.1f%%', colors=plt.cm.Paired(range(len(pie_data))))
        ax[1].set_title('Distribution of Publications by Faculty')

        plt.tight_layout()
        plt.show()
    else:
        messagebox.showinfo("Info", "No data available for visualization.")

def save_data():
    author = faculty_combobox.get()
    year = year_combobox.get()
    month = month_combobox.get()
    communicated = int(communicated_entry.get())
    accepted = int(accepted_entry.get())
    published = int(published_entry.get())
    save_data_to_csv(author, year, month, communicated, accepted, published)

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

tk.Label(root, text="Accepted", font=default_font).grid(row=5, column=0, padx=10, pady=5, sticky='e')
accepted_entry = tk.Entry(root)
accepted_entry.grid(row=5, column=1, padx=10, pady=5, sticky='w')

tk.Label(root, text="Published", font=default_font).grid(row=6, column=0, padx=10, pady=5, sticky='e')
published_entry = tk.Entry(root)
published_entry.grid(row=6, column=1, padx=10, pady=5, sticky='w')

# Buttons
tk.Button(root, text="Save Data", command=save_data, font=default_font, bg='lightblue').grid(row=7, column=0, columnspan=2, pady=10, sticky='n')
tk.Button(root, text="Plot Visualizations", command=plot_visualizations, font=default_font, bg='lightgreen').grid(row=8, column=0, columnspan=2, pady=10, sticky='n')

root.mainloop()
