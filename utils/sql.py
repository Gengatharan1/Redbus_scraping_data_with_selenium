import pandas as pd
import mysql.connector
import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path


# Load environment variables from .env and .env_shared/.env_secret
load_dotenv(dotenv_path='./env/secret')
load_dotenv(dotenv_path='./env/shared')
print(os.getenv("MY_SECRET_KEY"))

# config = {
#     **dotenv_values(".env_shared"),
#     **dotenv_values(".env_secret")
# }
# print(config)


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
