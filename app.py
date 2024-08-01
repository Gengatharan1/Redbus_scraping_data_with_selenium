import pandas as pd
import mysql.connector
import streamlit as st
import base64
import os
from dotenv import load_dotenv, dotenv_values

# Load environment variables
load_dotenv(dotenv_path='.env')

config={
    **dotenv_values(".env_shared"),
    **dotenv_values(".env_secret"),
    # **os.environ
}
print(config)

# Function to load data from a CSV file
def load_data(filepath):
    return pd.read_csv(filepath)

# Function to connect to MySQL database
def connect_mysql():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("host_name"),
            user=os.getenv("user_name"),
            password=os.getenv("pwd_key"),
            database=os.getenv("db_name")
        )
        return conn
    except Exception as e:
        st.error("Error connecting to the database.")
        return None

# Ensure the path is correct
current_dir = os.path.dirname(os.path.abspath(__file__))
background_image_path = os.path.join(current_dir, './image/bg_img.jpg')

base64_image = ''

# Check if the file exists
if not os.path.exists(background_image_path):
    st.error(f"File not found: {background_image_path}")
else:
    # Convert the image to base64
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    # Convert the image to base64
    base64_image = get_base64_of_bin_file(background_image_path)

# Set the background image in Streamlit
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpg;base64,{base64_image}");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# App Title
st.markdown("<h1 style='font-size:36px; color:Red;text-align:center;'>Redbus Dashboard</h1>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.header("Navigation Menu")
menu_option = st.sidebar.radio("Choose a page:", ["Home", "Project"])

# Function to display "About the Developer" section
def about_the_developer():
    st.header("About the Developer")
    st.write("Name : Gengatharan L | Role : Fresher")
    st.write("""
    I am a passionate and driven individual eager to kickstart my career in data science. 
    With a strong foundation in statistics, programming, and data analysis, I am continuously 
    honing my skills in data visualization, machine learning, deep learning, and AI. 
    My goal is to leverage data to solve real-world problems and contribute to impactful projects.
    """)
    st.subheader("Contact Details")
    st.write("[LinkedIn](https://www.linkedin.com/in/gengatharan007/) | [GitHub](https://github.com/Gengatharan1) | Email: gengatharan.ds@gmail.com")

# Function to display "Skills Take Away From This Project" section
def skills_take_away():
    st.subheader("Skills Take Away From This Project")
    skills = [
        "Selenium Webdriver",
        "Python Scripting",
        "Data Scraping",
        "Streamlit Application",
        "Pandas",
        "Data Management using MySQL"
    ]
    for skill in skills:
        st.write(f"- {skill}")

# Function to display "Objective" section
def objective():
    st.subheader("Objective")
    st.write("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")

# Function to display "Prerequisites" section
def prerequisites():
    st.subheader("Prerequisites")
    prerequisites_list = [
        "Python Environment: Install Python on your system",
        "Selenium - Chrome driver",
        "Dependencies: Install Streamlit, Pandas, Selenium, mysql_connector",
        "SQL Database: Set up MySQL database with local machine login credentials",
        "Streamlit: Install Streamlit library for running the application"
    ]
    for item in prerequisites_list:
        st.write(f"- {item}")

# Function to display "Required Python Libraries" section
def required_python_libraries():
    st.subheader("Required Python Libraries")
    libraries = ["Selenium", "pandas", "streamlit", "mysql.connector", "datetime", "re"]
    st.write(", ".join(libraries))

# Function to display "Approach" section
def approach():
    st.subheader("Approach")
    steps = [
        "Data fetching using Selenium",
        "Data cleaning or wrangling using EDA",
        "Migrate data to a SQL database using pandas",
        "Query the SQL database",
        "Display data in the Streamlit application."
    ]
    for step in steps:
        st.write(f"- {step}")

# Function to execute and display the result of a SQL query
def execute_query(cursor, query, params=None):
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                                            "Price", "Seats_Available", "Ratings", "Route_name", "Origin", "Destination"])
        st.write(df)
        st.write(f"Number of records: {len(df)}")
    except Exception as e:
        st.error("Error fetching data.")

# Home page navigation
if menu_option == "Home":
    st.sidebar.subheader("Content")
    options = ["About the Developer", "Skills Take Away From This Project", "Objective", "Prerequisites", "Required Python Libraries", "Approach"]
    choice = st.sidebar.radio("Go to", options)

    if choice == "About the Developer":
        about_the_developer()
    elif choice == "Skills Take Away From This Project":
        skills_take_away()
    elif choice == "Objective":
        objective()
    elif choice == "Prerequisites":
        prerequisites()
    elif choice == "Required Python Libraries":
        required_python_libraries()
    elif choice == "Approach":
        approach()

# Project page navigation
if menu_option == "Project":
    st.subheader("Bus Data Filtering")

    # Load data
    df = load_data("final_data.csv")
    df_origin = load_data("origin.csv")
    df_destination = load_data("destination.csv")
    print("Columns in df_destination:", df_destination.columns)
    print(df_destination.head())

    origin_set = df_origin['Origin'].unique().tolist()
    destination_set = df_destination['Destination'].unique().tolist()

    range_values = st.slider("Select a range of values:", min_value=0, max_value=15000, value=(0, 15000))
    st.write(f"You selected a range: {range_values}")

    origin = st.selectbox("Choose From", ['All'] + origin_set)
    destination = st.selectbox("Choose To", ['All'] + destination_set)

    conn = connect_mysql()
    if conn:
        my_cursor = conn.cursor()

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Apply Price Sort"):
                query = """
                SELECT * FROM bus_routes
                WHERE Price BETWEEN %s AND %s
                ORDER BY Price DESC
                """
                execute_query(my_cursor, query, (range_values[0], range_values[1]))

        with col2:
            if st.button("Apply Route Sort"):
                query = """
                SELECT * FROM bus_routes
                WHERE Origin = %s AND Destination = %s
                """
                execute_query(my_cursor, query, (origin, destination))

        with col3:
            if st.button("Apply Both Route and Price Sort"):
                query = """
                SELECT * FROM bus_routes
                WHERE Origin = %s AND Destination = %s 
                AND Price BETWEEN %s AND %s
                ORDER BY Price DESC
                """
                execute_query(my_cursor, query, (origin, destination, range_values[0], range_values[1]))
