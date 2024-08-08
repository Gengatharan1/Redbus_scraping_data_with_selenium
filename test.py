import pandas as pd
import mysql.connector
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='./env/secret')
load_dotenv(dotenv_path='./env/shared')

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
        st.error(f"Error connecting to the database: {e}")
        return None

# Function to execute and display the result of a SQL query
def execute_query(cursor, query, params=None):
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                                            "Price", "Seats_Available", "Ratings", "Route_name", "Origin", "Destination"])
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# App Title
st.markdown("<h1 style='font-size:36px; color:Red;text-align:center;'>Redbus Dashboard</h1>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.header("Navigation Menu")
menu_option = st.sidebar.radio("Choose a page:", ["Home", "States and Routes"])

# States and Routes page navigation
if menu_option == "States and Routes":
    st.subheader("Bus Data Filtering")

    # List of 10 states
    states = ["Andhra Pradesh", "Telangana", "Kerala", "South Bengal", "West Bengal", 
              "Rajasthan", "Bihar", "Himachal", "Chandigarh", "Assam"]

    # Select origin and destination based on states
    origin = st.selectbox("Select Origin", states)
    destination = st.selectbox("Select Destination", states)

    # Select bus type and fare range
    col1, col2 = st.columns(2)
    with col1:
        select_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-sleeper", "Others"))
    with col2:
        select_fare = st.radio("Choose Bus Fare Range", ("50-1000", "1000-2000", "2000 and above"))

    # Select bus start time
    TIME = st.selectbox("Select Start Time", ['00:00', '01:00', '02:00', '03:00', '04:00', 
                                              '05:00', '06:00', '07:00', '08:00', '09:00', 
                                              '10:00', '11:00', '12:00', '13:00', '14:00', 
                                              '15:00', '16:00', '17:00', '18:00', '19:00', 
                                              '20:00', '21:00', '22:00', '23:00'])

    # Convert selected start time to datetime format
    TIME = pd.to_datetime(TIME, format='%H:%M').time()

    # Define fare range based on selection
    if select_fare == "50-1000":
        fare_min, fare_max = 50, 1000
    elif select_fare == "1000-2000":
        fare_min, fare_max = 1000, 2000
    else:
        fare_min, fare_max = 2000, 15000

    # Define bus type condition for SQL query
    if select_type == "Sleeper":
        bus_type_condition = "Bus_type LIKE '%Sleeper%'"
    elif select_type == "Semi-sleeper":
        bus_type_condition = "Bus_type LIKE '%Semi Sleeper%'"
    else:
        bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi Sleeper%'"

    # Connect to MySQL and fetch filtered bus data
    conn = connect_mysql()
    if conn:
        cursor = conn.cursor()
        query = f'''
            SELECT * FROM bus_details 
            WHERE Price BETWEEN {fare_min} AND {fare_max}
            AND Origin = '{origin}' AND Destination = '{destination}'
            AND {bus_type_condition} AND Start_time >= '{TIME}'
            ORDER BY Price, Start_time DESC
        '''
        df_result = execute_query(cursor, query)
        cursor.close()
        conn.close()

        # Display the filtered data
        if not df_result.empty:
            st.subheader("Filtered Bus Data")
            st.dataframe(df_result)
        else:
            st.warning("No data available for the selected criteria.")
    else:
        st.error("Database connection failed.")
