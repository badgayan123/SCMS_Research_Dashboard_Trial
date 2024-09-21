import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Define the base directory for data storage
DATA_DIR = 'D:/publication'

# User credentials and faculty mapping
USER_CREDENTIALS = {
    'aarti123': 'password123',
    'chandan123': 'password456',
    'nikita123': 'password789',
    'anandita123': 'password101112',
    'sivaretinamohan123': 'password131415',
    'shanmugha123': 'password161718',
    'meenakshi123': 'password192021',
    'seeboli123': 'password222324',
    'nitesh123': 'password252627',
    'poornima123': 'password282930'
}

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

# Function to create file path for a given year and month
def get_file_path(year, month):
    month_name = month.lower().capitalize()
    return os.path.join(DATA_DIR, f'publication_data_{month_name}_{year}.csv')

# Function to ensure directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to load existing data or create a new file if it doesn't exist
def load_data(year, month):
    file_path = get_file_path(year, month)
    ensure_directory_exists(DATA_DIR)  # Create directory if it doesn't exist
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # Create a new DataFrame and save it as a CSV file if it doesn't exist
        df = pd.DataFrame(columns=['Author', 'Year', 'Month', 'Communicated', 'Accepted', 'Published'])
        df.to_csv(file_path, index=False)
        return df

# Function to save data to CSV
def save_data(df, year, month):
    file_path = get_file_path(year, month)
    ensure_directory_exists(DATA_DIR)  # Ensure directory exists before saving
    df.to_csv(file_path, index=False)

# ----------------------------
# Streamlit App Setup
# ----------------------------
st.title("SMS Publication Dashboard")

# ----------------------------
# Authentication
# ----------------------------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.faculty_name = FACULTY_NAMES.get(username)
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password.")
    st.stop()  # Stop the app until user logs in

# ----------------------------
# Layout: Two Columns for Faculty Details and Publications Overview
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Faculty Details")
    faculty_names = list(FACULTY_NAMES.values())
    selected_faculty = st.selectbox("Select Faculty Name", faculty_names)
    st.write(f"You have selected: {selected_faculty}")

with col2:
    st.subheader("Publications Overview")

    # ----------------------------
    # Tabs for Year and Month Selection and Publication Details
    # ----------------------------
    tab1, tab2 = st.tabs(["Select Year and Month", "Publication Details"])

    # ----------------------------
    # Tab for Selecting Year and Month
    # ----------------------------
    with tab1:
        selected_year = st.selectbox("Select Year", list(range(2024, 2051)))
        st.write(f"You have selected the year: {selected_year}")

        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        selected_month = st.selectbox("Select Month", months)
        st.write(f"You have selected the month: {selected_month}")

    # ----------------------------
    # Tab for Publication Details
    # ----------------------------
    with tab2:
        tab3, tab4, tab5 = st.tabs(["Communicated", "Accepted", "Published"])

        # ----------------------------
        # Tab for Communicated
        # ----------------------------
        with tab3:
            communicated = st.number_input("Enter number of papers communicated", min_value=0, step=1)
            st.write(f"Number of papers communicated: {communicated}")

        # ----------------------------
        # Tab for Accepted
        # ----------------------------
        with tab4:
            accepted = st.number_input("Enter number of papers accepted", min_value=0, step=1)
            st.write(f"Number of papers accepted: {accepted}")

        # ----------------------------
        # Tab for Published
        # ----------------------------
        with tab5:
            published = st.number_input("Enter number of papers published", min_value=0, step=1)
            st.write(f"Number of papers published: {published}")

        # Button to save the data
        if st.button("Save Data"):
            # Load data for the selected month and year
            data = load_data(selected_year, selected_month)
            # Append new entry to the existing data
            if selected_faculty == st.session_state.faculty_name:
                new_data = pd.DataFrame({
                    'Author': [selected_faculty],
                    'Year': [selected_year],
                    'Month': [selected_month],
                    'Communicated': [communicated],
                    'Accepted': [accepted],
                    'Published': [published]
                })
                data = pd.concat([data, new_data], ignore_index=True)
                save_data(data, selected_year, selected_month)
                st.success("Data saved successfully!")
            else:
                st.error("You are not authorized to enter data for this faculty member.")

# ----------------------------
# Visualization
# ----------------------------
st.header("Visualizations")

# Load data for visualization
visualization_year = st.selectbox("Select Year for Visualization", list(range(2024, 2051)))
visualization_month = st.selectbox("Select Month for Visualization", ["January", "February", "March", "April", "May", "June",
                                                                      "July", "August", "September", "October", "November", "December"])

visualization_data = load_data(visualization_year, visualization_month)

if not visualization_data.empty:
    # Bar Graph: Total Publications Communicated, Accepted, and Published
    st.subheader("Bar Graph: Total Publications Communicated, Accepted, and Published")
    bar_data = visualization_data.groupby('Author').sum().reset_index()
    bar_fig = px.bar(bar_data, x='Author', y=['Communicated', 'Accepted', 'Published'],
                     title='Total Publications Communicated, Accepted, and Published')
    st.plotly_chart(bar_fig)

    # Pie Chart: Distribution of Publication Types
    st.subheader("Pie Chart: Distribution of Publication Types")
    pie_data = visualization_data.copy()
    pie_data['Total'] = pie_data[['Communicated', 'Accepted', 'Published']].sum(axis=1)
    pie_fig = px.pie(pie_data, names='Author', values='Total',
                     title='Distribution of Publication Types')
    st.plotly_chart(pie_fig)
else:
    st.write("No data available for visualization.")
