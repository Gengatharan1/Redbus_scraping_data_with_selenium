import pandas as pd
import mysql.connector
import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
from utils import sql

# Function to load data from a CSV file
def load_data(filepath):
    return pd.read_csv(filepath)


st.subheader("Bus Data Filtering")

# Load data
df = load_data("data/final_bus_data.csv")

# Create select boxes for origin and destination
origin_set = df['Origin'].unique().tolist()
destination_set = df['Destination'].unique().tolist()
destination_set = df['Destination'].unique().tolist()

origin = st.selectbox("Select Origin", origin_set)
destination = st.selectbox("Select Destination", destination_set)

# # Sort columns for bus type, fare range, and time input
# col1, col2 = st.columns(2)
# with col1:
#     select_type = st.radio("Choose Bus Type", ("Sleeper", "Semi-sleeper", "Others"))
# with col2:
#     select_fare = st.radio("Choose Bus Fare Range", ("50-1000", "1000-2000", "2000 and above"))

# TIME = st.time_input("Select the Time")

# # sort based on bus type
# if select_type == "Sleeper":
#     bus_type_condition = "Bus_type LIKE '%Sleeper%'"
# elif select_type == "semi-sleeper":
#     bus_type_condition = "Bus_type LIKE '%A/c Semi Sleeper %'"
# else:
#     bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%'"

# sort based on bus fare
if select_fare == "50-1000":
    fare_min, fare_max = 50, 1000
elif select_fare == "1000-2000":
    fare_min, fare_max = 1000, 2000
else:
    fare_min, fare_max = 2000, 15000

# Convert Start_time to time format
df['Start_time'] = pd.to_datetime(df['Start_time'], format='%H:%M').dt.time

filtered_df = df[(df['Origin'] == origin) &
                    (df['Destination'] == destination) &
                    (df['Bus_type'] == select_type) &
                    (df['Price'].between(fare_min, fare_max)) &
                    (df['Start_time'] == TIME)]

# Sort the results by price and bus type
filtered_df = filtered_df.sort_values(by=['Bus_type', 'Price'])

# Display filtered bus data
st.subheader("Filtered Bus Data")
st.write(df)
# st.write(filtered_df)

# Connect to MySQL and fetch data
conn = sql.connect_mysql()
if conn:
    cursor = conn.cursor()
    sql_query = "SELECT * FROM bus_routes"
    df = sql.execute_query(cursor, sql_query)
    cursor.close()
    conn.close()
    
    # Display the SQL data
    if not df.empty:
        st.write(df)
        st.write(f"Number of records: {len(df)}")
    else:
        st.warning("No data available from the SQL database.")