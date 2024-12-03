import streamlit as st
from pymongo import MongoClient
from urllib.parse import quote_plus

# MongoDB Atlas connection details
username = quote_plus('niteshbadgayan')
password = quote_plus('Ganapati@123')
connection_string = f"mongodb+srv://{username}:{password}@cluster0.lw4vz.mongodb.net/SCMS_Publication?retryWrites=true&w=majority"

# MongoDB connection
client = MongoClient(connection_string)
db = client['SCMS_Publication']
research_collection = db['Research']  # Tab 2: Publication Summary
publication_details_collection = db['PublicationDetails']  # Tab 3: Publication Details

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

# Streamlit App Setup
st.set_page_config(page_title="SCMS Research Publication", layout="centered")

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.logged_in_user = None
    st.session_state.publication_type = None
    st.session_state.data_saved = False
    st.session_state.submitted = False

# Login Page
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>Welcome to SCMS Research Publication Dashboard</h1>", unsafe_allow_html=True)
    st.subheader("Please Log In to Continue")

    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    login_button = st.button("Login")
    if login_button:
        if username_input in USER_CREDENTIALS and USER_CREDENTIALS[username_input] == password_input:
            st.session_state.logged_in = True
            st.session_state.logged_in_user = username_input
            st.success(f"Welcome {FACULTY_NAMES.get(username_input, 'User')}!")
            st.rerun()  # Refresh the page after login
        else:
            st.error("Invalid username or password. Please try again.")

# After successful login
if st.session_state.logged_in:
    user_name = FACULTY_NAMES.get(st.session_state.logged_in_user, "Unknown Faculty")

    # Show the main page after login
    st.markdown(f"<h2 style='text-align: center;'>Welcome, {user_name}</h2>", unsafe_allow_html=True)
    st.subheader("Enter Publication Summary")

    # Create tabs for the layout
    tab1, tab2, tab3 = st.tabs(["Select Year and Month", "Publication Summary", "Publication Details"])

    # Tab for Selecting Year and Month
    with tab1:
        selected_faculty = st.selectbox("Select Faculty Name", [user_name])
        st.write(f"You have selected: {selected_faculty}")

        selected_year = st.selectbox("Select Year", list(range(2024, 2051)))
        st.write(f"You have selected the year: {selected_year}")

        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        selected_month = st.selectbox("Select Month", months)
        st.write(f"You have selected the month: {selected_month}")

    # Tab for Publication Summary
    with tab2:  # Updated tab name
        publication_type = st.selectbox("Select Publication Type",
                                        ["Journal", "Conference", "Book/Book Chapter", "Case Study", "IP"])
        st.write(f"You have selected: {publication_type}")

        # Generate a session key based on publication type
        session_key = f"data_saved_{publication_type}"

        # Initialize session state for the session_key if not already set
        if session_key not in st.session_state:
            st.session_state[session_key] = False

        # Reset data if publication type has changed
        if publication_type != st.session_state.get("publication_type", ""):
            st.session_state[session_key] = False  # Reset save status for this type
            st.session_state["publication_type"] = publication_type  # Update the current publication type

        # Initialize a variable to store data to save
        data_to_save = {
            "year": selected_year,
            "month": selected_month,
            "faculty": selected_faculty,
            "publication_type": publication_type
        }

        # Define input fields based on publication type
        if publication_type == "Journal":
            communicated_papers = st.number_input("How many journal papers communicated?", min_value=0, step=1)
            accepted_papers = st.number_input("How many journal papers accepted?", min_value=0, step=1)
            published_papers = st.number_input("How many journal papers published?", min_value=0, step=1)

            data_to_save.update({
                "communicated_papers": communicated_papers,
                "accepted_papers": accepted_papers,
                "published_papers": published_papers
            })

        elif publication_type == "Conference":
            communicated_conferences = st.number_input("How many conference papers communicated?", min_value=0, step=1)
            accepted_conferences = st.number_input("How many conference papers accepted?", min_value=0, step=1)
            published_conferences = st.number_input("How many conference papers published?", min_value=0, step=1)

            data_to_save.update({
                "communicated_conferences": communicated_conferences,
                "accepted_conferences": accepted_conferences,
                "published_conferences": published_conferences
            })

        elif publication_type == "Book/Book Chapter":
            book_type = st.selectbox("Select Type", ["Book", "Book Chapter"])

            if book_type == "Book":
                communicated_books = st.number_input("How many books communicated?", min_value=0, step=1)
                accepted_books = st.number_input("How many books accepted?", min_value=0, step=1)
                published_books = st.number_input("How many books published?", min_value=0, step=1)

                data_to_save.update({
                    "book_type": book_type,
                    "communicated_books": communicated_books,
                    "accepted_books": accepted_books,
                    "published_books": published_books
                })
            else:
                communicated_chapters = st.number_input("How many book chapters communicated?", min_value=0, step=1)
                accepted_chapters = st.number_input("How many book chapters accepted?", min_value=0, step=1)
                published_chapters = st.number_input("How many book chapters published?", min_value=0, step=1)

                data_to_save.update({
                    "book_type": book_type,
                    "communicated_chapters": communicated_chapters,
                    "accepted_chapters": accepted_chapters,
                    "published_chapters": published_chapters
                })
        elif publication_type == "Case Study":
            communicated_studies = st.number_input("How many case studies communicated?", min_value=0, step=1)
            accepted_studies = st.number_input("How many case studies accepted?", min_value=0, step=1)
            published_studies = st.number_input("How many case studies published?", min_value=0, step=1)

            data_to_save.update({
                "communicated_studies": communicated_studies,
                "accepted_studies": accepted_studies,
                "published_studies": published_studies
            })

        elif publication_type == "IP":
            ip_type = st.selectbox("Select Type of IP",
                                   ["Design Patent/Registration", "Product Patent", "Trademark", "Copyright"])

            communicated_label = f"How many {ip_type.lower()} communicated?"
            accepted_label = f"How many {ip_type.lower()} accepted?"
            granted_label = f"How many {ip_type.lower()} granted?"

            communicated_ips = st.number_input(communicated_label, min_value=0, step=1)
            accepted_ips = st.number_input(accepted_label, min_value=0, step=1)
            granted_ips = st.number_input(granted_label, min_value=0, step=1)

            data_to_save.update({
                "ip_type": ip_type,
                "communicated_ips": communicated_ips,
                "accepted_ips": accepted_ips,
                "granted_ips": granted_ips
            })

# Save data
        save_button = st.button("Save")
        if save_button and not st.session_state[session_key]:
            try:
                research_collection.insert_one(data_to_save)
                st.session_state[session_key] = True
                st.session_state['data_saved'] = True  # Update the global data_saved variable
                st.success(f"Data for {publication_type} saved successfully!")
            except Exception as e:
                st.error(f"An error occurred while saving data: {e}")
        # Add the message below the Save button
        st.info("Once you save data, you cannot re-save for the same publication type unless you log out and log back in.")

    # Tab for Publication Details

    with tab3:
        st.subheader("Enter Publication Details")

                # Check if data is saved in Tab 2
        if not st.session_state.get('data_saved', False):
            st.warning("Please save the publication summary in Tab 2 before proceeding.")
        else:
            scopus_id = st.number_input("Scopus ID (Numeric only)", min_value=0, step=1, key="scopus_id_input")
            publication_type = st.selectbox(
                "Type of Publication",
                ["Journal", "Conference", "Book Chapter", "Case Study", "IP"],
                key="publication_type_selectbox"
            )
            publication_title = st.text_input("Title of Publication", key="publication_title_input")
            indexing = st.selectbox(
                "Indexing",
                ["Only Scopus", "Only WoS", "Both", "None"],
                key="indexing_selectbox"
            )
            ABDC = st.selectbox(
                "ABDC",
                ["A*", "A", "B", "C"],
                key="ABDC_selectbox"
            )
            journal_quartiles = st.selectbox(
                "Journal Quartiles",
                ["Q1", "Q2", "Q3", "Q4"],
                key="journal_quartiles_selectbox"
            )
            impact_factor_input = st.text_input("Impact Factor (e.g., 2.5)", key="impact_factor_input")
            doi = st.text_input("DOI (Optional)", key="doi_input")

            # Validate impact factor
            impact_factor = None
            if impact_factor_input:
                try:
                    impact_factor = float(impact_factor_input)
                    if not (0.0 <= impact_factor <= 100.0):
                        raise ValueError("Impact factor out of range.")
                except ValueError:
                    st.error("Impact factor must be a number between 0.0 and 100.0.")

            # Centered Submit Button
            # Centered Submit Button
            # Pre-Submission Message
            if not st.session_state['submitted']:
                st.info("Please note: After you submit the data, you will no longer be able to make changes.")

            # Centered Submit Button
            # Centered Submit Button
        submit_details_button = st.button("Submit Publication Details", key="submit_button")
        st.markdown(
            """
            <style>
                div.stButton > button:first-child {
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }
            </style>
            """,
            unsafe_allow_html=True
        )

        if submit_details_button and not st.session_state['submitted']:
            # Preparing the publication details dictionary
            publication_details = {
                "faculty": user_name,
                "year": selected_year,
                "month": selected_month,
                "scopus_id": scopus_id,
                "publication_type": publication_type,
                "publication_title": publication_title,
                "indexing": indexing,
                "ABDC": ABDC,
                "journal_quartiles": journal_quartiles,
                "impact_factor": impact_factor,
                "doi": doi
            }

            try:
                # Save to MongoDB
                publication_details_collection.insert_one(publication_details)
                st.session_state['submitted'] = True

                # Success Message
                st.success("Data Submitted Successfully!")

                # Balloons Animation
                st.markdown("""
                       <style>
                       .balloon {
                           position: fixed;
                           top: 100%;
                           left: calc(10% + 10vw);
                           font-size: 50px;
                           animation: fly 6s linear forwards;
                           z-index: 9999;
                       }
                       .balloon:nth-child(2) { left: calc(30% + 10vw); animation-delay: 0.2s; }
                       .balloon:nth-child(3) { left: calc(50% + 10vw); animation-delay: 0.4s; }
                       .balloon:nth-child(4) { left: calc(70% + 10vw); animation-delay: 0.6s; }
                       .balloon:nth-child(5) { left: calc(90% + 10vw); animation-delay: 0.8s; }

                       @keyframes fly {
                           0% { top: 100%; opacity: 1; }
                           100% { top: -30%; opacity: 0; }
                       }
                       </style>
                       <!-- Balloons Animation -->
                       <div class="balloon">🎈</div>
                       <div class="balloon">🎈</div>
                       <div class="balloon">🎈</div>
                       <div class="balloon">🎈</div>
                       <div class="balloon">🎈</div>
                   """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred while saving the details: {e}")

        # Disable form if already submitted
        if st.session_state['submitted']:
            st.warning("You have already submitted the data. No further changes can be made.")
            st.stop()  # Prevent further interaction with the script








