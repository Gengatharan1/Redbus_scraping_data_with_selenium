import streamlit as st


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


def objective():
    st.subheader("Main Objective")
    st.write("Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit")


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


def required_python_libraries():
    st.subheader("Required Python Libraries")
    libraries = ["Selenium", "pandas", "numpy", "mysql.connector", "streamlit", "datetime"]
    st.write(", ".join(libraries))


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
