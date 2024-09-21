import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
from urllib.parse import quote_plus

# MongoDB Atlas connection details
username = quote_plus('niteshbadgayan')
password = quote_plus('Ganapati@123')
connection_string = f"mongodb+srv://{username}:{password}@cluster0.lw4vz.mongodb.net/your_database_name?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(connection_string)
db = client['publication_database']  # Use your desired database name
collection = db['publications']  # Use your desired collection name

# User credentials and faculty mapping
# USER_CREDENTIALS = {
#     'aarti123': 'password123',
#     'chandan123': 'password456',
#     'nikita123': 'password789',
#     'anandita123': 'password101112',
#     'sivaretinamohan123': 'password131415',
#     'shanmugha123': 'password161718',
#     'meenakshi123': 'password192021',
#     'seeboli123': 'password222324',
#     'nitesh123': 'password252627',
#     'poornima123': 'password282930'
# }

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

# Function to save data to MongoDB
def save_data_to_mongodb(author, year, month, communicated, accepted, published):
    document = {
        'Author': author,
        'Year': year,
        'Month': month,
        'Communicated': communicated,
        'Accepted': accepted,
        'Published': published
    }
    collection.insert_one(document)
    st.success("Data saved to MongoDB successfully!")

# Load data for visualization from MongoDB
def load_data_from_mongodb(year, month):
    cursor = collection.find({"Year": year, "Month": month})
    data = pd.DataFrame(list(cursor))
    return data

# ----------------------------
# Streamlit App Setup
# ----------------------------
st.title("SCMS Research Publication Dashboard")

# ----------------------------
# Layout: Two Columns for Faculty Details and Publications Overview
# ----------------------------
col1, col2 = streamlitst.columns(2)

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
            # Save data to MongoDB for the selected month and year
            save_data_to_mongodb(selected_faculty, selected_year, selected_month, communicated, accepted, published)

# ----------------------------
# Visualization
# ----------------------------
st.header("Visualizations")

# Load data for visualization
visualization_year = st.selectbox("Select Year for Visualization", list(range(2024, 2051)))
visualization_month = st.selectbox("Select Month for Visualization", months)

visualization_data = load_data_from_mongodb(visualization_year, visualization_month)

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
