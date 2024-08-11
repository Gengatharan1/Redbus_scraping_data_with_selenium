import pandas as pd
import streamlit as st
from pathlib import Path
from utils.sql import sql, States, Routes, Buses
from utils.components import (
    bus_count_plot, pie_plot, bus_type_plot, bus_time_plot, avg_plot,
    select_multiple, select_one
)
from sqlalchemy import text
import plotly.graph_objects as go
import matplotlib.pyplot as plt


session, engine = sql()


st.set_page_config(
    page_title="Redbus Analysis",
    layout="wide"  # This sets the layout to be wide
)


st.markdown("# Bus Data Dashboard")

sql_query = f'''
    SELECT buses.*, routes.state 
    FROM buses left join routes 
    on buses.route_name = routes.route_name
    '''
stmt = text(sql_query)
with engine.connect() as connection: res = connection.execute(stmt)
df_all = pd.DataFrame(res.fetchall(), columns=res.keys()) 
# st.write(df_all)


# state
selected_states = select_multiple(df_all['state'].unique(), 'Select states')
# route
selected_routes = select_multiple(df_all['route_name'].unique(), 'Select routes')
# min seat available
selected_seats = select_one(range(df_all['seat_available'].astype(int).max() + 1), 'Select minimum seats available')
# min rating
selected_rating = select_one(range(6), 'Select minimum rating')
# max price
selected_price = st.text_input('Select maximum price', value="")
# # departure time
# selected_time = select_one(df_all['state'].unique(), 'Select departure time')

# operator

selected_sleeper = st.checkbox('Sleeper', value=True)
selected_non_sleeper = st.checkbox('Non Sleeper', value=True)
selected_ac = st.checkbox('AC', value=True)
selected_non_ac = st.checkbox('Non AC', value=True)



# filters process

# get data by filter
sql_query_all = f'''
    SELECT buses.*, routes.state 
    FROM buses left join routes 
    on buses.route_name = routes.route_name
    WHERE 1=1
    '''

normal_filters = []
if selected_states:
    normal_filters.append(f" AND routes.state IN ('{"', '".join(selected_states)}')")
if selected_routes:
    normal_filters.append(f" AND buses.route_name IN ('{"', '".join(selected_routes)}')")
if selected_seats:
    normal_filters.append(f" AND buses.seat_available >= {selected_seats}")
if selected_rating:
    normal_filters.append(f" AND buses.star_rate >= {selected_rating}")
if selected_price:
    normal_filters.append(f" AND buses.price <= {selected_price}")
if selected_sleeper and not selected_non_sleeper:
    normal_filters.append(f" AND LOWER(buses.bus_type) LIKE '%sleeper%'")
if selected_non_sleeper and not selected_sleeper:
    normal_filters.append(f" AND LOWER(buses.bus_type) NOT LIKE '%sleeper%'")
if selected_ac and not selected_non_ac:
    normal_filters.append(f" AND buses.bus_type LIKE '%AC%' AND buses.bus_type NOT LIKE '%NON AC%'")
if selected_non_ac and not selected_ac:
    normal_filters.append(f" AND buses.bus_type LIKE '%NON AC%'")

sql_query_normal = sql_query_all + ''.join(normal_filters)
sql_query_bus_type = sql_query_all + ''.join(normal_filters)
sql_query_filter = sql_query_bus_type

stmt = text(sql_query_filter)
with engine.connect() as connection: res = connection.execute(stmt)
df = pd.DataFrame(res.fetchall(), columns=res.keys()) 
# st.write(df)


# overall_title, state_title, route_title = st.columns(3)
# overall_buses, state_buses, route_buses = st.columns(3)
# overall_bus_type, state_bus_type, route_bus_type = st.columns(3)
# overall_operator, state_operator, route_operator = st.columns(3)
# overall_dep_bins, state_dep_bins, route_dep_bins = st.columns(3)
# overall_seat_avail, stat_seat_avail, rout_seat_avail = st.columns(3)



# st.markdown("## Analysis")

c11, c12 = st.columns(2)
c21, c22 = st.columns(2)
c31, c32 = st.columns(2)
c41, c42 = st.columns(2)

bus_count_plot(c11, df, 'state', 'State bus count')
bus_count_plot(c12, df, 'route_name', 'Route bus count')

avg_plot(c21, engine, sql_query_filter, 'state', 'star_rate', 'State average rating')
avg_plot(c22, engine, sql_query_filter, 'route_name', 'price', 'Route average price')

bus_count_plot(c31, df, 'loc_dep', 'Departure bus count')
bus_time_plot(c32, engine, sql_query_filter, 'Time bin bus count')

bus_type_plot(c41, engine, sql_query_filter, 'Bus type')

