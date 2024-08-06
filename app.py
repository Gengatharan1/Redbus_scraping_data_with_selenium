import pandas as pd
import mysql.connector
import streamlit as st
import os
from dotenv import load_dotenv, dotenv_values


# Load environment variables
load_dotenv(dotenv_path='.env')

config={
    **dotenv_values(".env_shared"),
    **dotenv_values(".env_secret")
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


# App Title
st.markdown("<h1 style='font-size:36px; color:Red;text-align:center;'>Redbus Dashboard</h1>", unsafe_allow_html=True)


# Sidebar Navigation
st.sidebar.header("Navigation Menu")
menu_option = st.sidebar.radio("Choose a page:", ["Home", "Project"])


# Function to display "About the Developer" section
def about_the_developer():
    st.header("About Myself")
    st.write("Name : Gengatharan L | Role : Fresher")
    st.write("""
    I am a passionate and driven individual eager to kickstart my career in data science. 
    With a strong foundation in statistics, programming, and data analysis, I am continuously 
    honing my skills in data visualization, machine learning, deep learning, and AI. 
    My goal is to leverage data to solve real-world problems and contribute to impactful projects.
    """)
    st.subheader("Contact Details")
    st.write("[LinkedIn](https://www.linkedin.com/in/gengatharan007/) | [GitHub](https://github.com/Gengatharan1) | Email: gengatharan.ds@gmail.com")


# Function to display "Skills Take Away From This Project"
def skills_takeaway():
    st.subheader("Skills Takeaway")
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


# Function to display "Objective" of the project
def objective():
    st.subheader("Main Objective")
    st.write("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")


# Function to display "Prerequisites" to follow-up while creating a web application
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


# Function to display "Required Python Libraries" for this project
def required_python_libraries():
    st.subheader("Required Python Libraries")
    libraries = ["Selenium", "pandas", "numpy", "mysql.connector", "streamlit", "datetime"]
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
        skills_takeaway()
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

    # Create select boxes for origin and destination
    origin_set = df['Origin'].unique().tolist()
    destination_set = df['Destination'].unique().tolist()
    
    origin = st.selectbox("Select Origin", origin_set)
    destination = st.selectbox("Select Destination", destination_set)

    # Sort columns for bus type, fare range, and time input
    col1, col2 = st.columns(2)
    with col1:
        select_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-sleeper", "Others"))
    with col2:
        select_fare = st.radio("Choose Bus Fare Range", ("50-1000", "1000-2000", "2000 and above"))

    TIME = st.time_input("Select the Time")

    # Convert fare range selection to numerical bounds
    if select_fare == "50-1000":
        fare_min, fare_max = 50, 1000
    elif select_fare == "1000-2000":
        fare_min, fare_max = 1000, 2000
    else:
        fare_min, fare_max = 2000, 15000

    # Filter the DataFrame based on user selection
    filtered_df = df[(df['Origin'] == origin) &
                     (df['Destination'] == destination) &
                     (df['Bus_type'].str.lower() == select_type.lower()) &
                     (df['Price'].between(fare_min, fare_max))]

    # Convert Start_time column to datetime to match the selected time
    try:
        df['Start_time'] = pd.to_datetime(df['Start_time'], format='%H:%M').dt.time
    except ValueError:
        st.error("Time format in the data does not match expected format '%H:%M'. Please check the data format.")

    filtered_df = filtered_df[filtered_df['Start_time'] == TIME]

    # Sort the results by price
    filtered_df = filtered_df.sort_values(by='Price')

    # Display the filtered and sorted data
    if not filtered_df.empty:
        st.write(filtered_df)
        st.write(f"Number of records: {len(filtered_df)}")
    else:
        st.warning("No results found for the selected criteria.")