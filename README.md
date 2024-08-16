# Redbus Scraping and Filtering

## Description
This project is designed to scrape bus transportation data from various government state transport and private buses in redbus website using Selenium. The scraped data is then stored in a SQL database and processed using Python. A Streamlit application is built on top of this data, allowing users to filter and analyze bus routes, fares, and other relevant details.

## Table of Contents
- [Redbus Scraping and Filtering](#redbus-scraping-and-filtering)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [Softwares needed](#softwares-needed)
    - [Code](#code)
    - [Python packages](#python-packages)
    - [Environment\_variables](#environment_variables)
    - [Database Setup](#database-setup)
    - [Run App](#run-app)
  - [Workflow](#workflow)
  - [Contact](#contact)

## Setup
### Softwares needed
1. IDE (VS Code)
2. Python
3. Git (with git bash)
4. Selenium (Chrome Driver)
5. PostgreSQL (psycopg2)
6. Pandas
7. Sql Alchemy
8. Streamlit

### Code

Clone this repository and ```cd``` into that directory
``` 
git clone https://github.com/Gengatharan1/redbus_scraping_filtering.git
cd redbus_scraping_filtering
```

### Python packages

Install all necessary packages
``` 
pip install -r requirements.txt
```
To Avoiding the ModuleNotFoundError, If utils is missing an __init__.py file, create one:
``` 
touch utils/__init__.py
```

### Environment_variables
Creating ```.env``` file using template
``` 
cp env_template.txt .env
```

### Database Setup

Create an app and stored in Postgresql db and add its credentials in ```.env``` file.

Create a local sql database and add its credentials in ```.env``` file

### Run App
``` 
streamlit run Intro.py
```


## Workflow
[Slides](https://docs.google.com/presentation/d/16UceFjcFdSviX3FvEB9mInjUgLwBWEhL1dvOh8HB2zA)


## Contact
[LinkedIn](https://www.linkedin.com/in/gengatharan007/)

---
^ [Back to table of contents](#table-of-contents)
