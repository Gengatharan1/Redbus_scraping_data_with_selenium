import streamlit as st
import matplotlib.pyplot as plt
from sqlalchemy import text
import pandas as pd
import altair as alt


def select_multiple(items, label):
    selected_items = st.multiselect(
        label = label, 
        options = items,
    )

    # if not selected_items:
    #     st.error("Please select at least one item.")
    
    # else:
    #     selected_items = [item for item in items if items['value'] in selected_items]
    
    return selected_items


def select_one(items, label):
    selected_item = st.selectbox(
        label = label, 
        options = items
    )

    # if not selected_item:
        # st.error("Please select a value.")
    
    # else:
    #     selected_items = [item for item in items if items['value'] in selected_items]
    
    return selected_item


def bus_count_plot(col, engine, query_filter, index, title):
    col.markdown(f"### {title}")
    sql_query_type_analysis = '''
        WITH pre_table AS (
        ''' + query_filter + f''' )
        SELECT 
            {index},
            COUNT(DISTINCT bus_id) AS count,
            pre_table.operator
        FROM 
            pre_table
        GROUP BY 
            {index}, operator;
    '''
    stmt = text(sql_query_type_analysis)
    with engine.connect() as connection: res = connection.execute(stmt)
    df = pd.DataFrame(res.fetchall(), columns=res.keys())
    
    # col.bar_chart(df.set_index(index))

    chart = alt.Chart(df).mark_bar().encode(
        x=f'{index}:N',
        y='count:Q',
        color='operator:N',
        column='operator:N',
        tooltip=[f'{index}:N', 'operator:N', 'operator:N', 'count:Q']
    ).properties(
        width=450,
        height=300
    ).interactive()
    col.altair_chart(chart)


def bus_type_plot(col, engine, query_filter, title):
    col.markdown(f'### {title}')

    sql_query_type_analysis = '''
        WITH pre_table AS (
        ''' + query_filter + ''' )
        SELECT
            CASE
                WHEN LOWER(pre_table.bus_type) LIKE '%sleeper%' 
                    THEN 'Sleeper'
                ELSE 'Non Sleeper'
            END AS sleeper,
            CASE
                WHEN pre_table.bus_type LIKE '%AC%' AND pre_table.bus_type NOT LIKE '%NON AC%'
                    THEN 'AC'
                ELSE 'Non AC'
            END AS ac,
            pre_table.operator,
            COUNT(*) AS count
        FROM pre_table
        GROUP BY sleeper, ac, pre_table.operator
        ;
    '''
    stmt = text(sql_query_type_analysis)
    with engine.connect() as connection: res = connection.execute(stmt)
    df_type_analysis = pd.DataFrame(res.fetchall(), columns=res.keys()) 
    # col.write(df_type_analysis)


    # Create the chart
    chart = alt.Chart(df_type_analysis).mark_bar().encode(
        x='sleeper:N',
        y='count:Q',
        color='ac:N',
        column='operator:N',
        tooltip=['sleeper:N', 'ac:N', 'operator:N', 'count:Q']
    ).properties(
        width=500,
        # height=300
    ).interactive()
    col.altair_chart(chart)


def bus_time_plot(col, engine, query_filter, title):
    col.markdown(f'### {title}')

    sql_query_type_analysis = '''
        WITH pre_table AS (
        ''' + query_filter + ''' )
        SELECT 
            CASE 
                WHEN EXTRACT(HOUR FROM time_dep) BETWEEN 0 AND 7 THEN 'Early Morning (0 - 7)'
                WHEN EXTRACT(HOUR FROM time_dep) BETWEEN 8 AND 11 THEN 'Morning (8 - 11)'
                WHEN EXTRACT(HOUR FROM time_dep) BETWEEN 12 AND 16 THEN 'Afternoon (12 - 16)'
                WHEN EXTRACT(HOUR FROM time_dep) BETWEEN 17 AND 20 THEN 'Evening (17 - 20)'
                WHEN EXTRACT(HOUR FROM time_dep) BETWEEN 21 AND 23 THEN 'Night (21 - 23)'
            END AS time_bin,
            COUNT(bus_id) AS bus_count
        FROM 
            pre_table
        GROUP BY 
            time_bin;
    '''
    stmt = text(sql_query_type_analysis)
    with engine.connect() as connection: res = connection.execute(stmt)
    df_time_analysis = pd.DataFrame(res.fetchall(), columns=res.keys())
    df_time_analysis.set_index('time_bin', inplace=True)
    # col.write(df_time_analysis)

    col.bar_chart(df_time_analysis['bus_count'])


def avg_plot(col, engine, query_filter, level, value, title):
    col.markdown(f'### {title}')

    sql_query_type_analysis = '''
        WITH pre_table AS (
        ''' + query_filter + f''' )
        SELECT 
            {level},
            AVG({value}) AS avg_{value}
        FROM 
            pre_table
        GROUP BY 
            {level};
    '''
    stmt = text(sql_query_type_analysis)
    with engine.connect() as connection: res = connection.execute(stmt)
    df_time_analysis = pd.DataFrame(res.fetchall(), columns=res.keys())
    df_time_analysis[f'avg_{value}'] = df_time_analysis[f'avg_{value}'].astype(float).round(2)
    # df_time_analysis = df_time_analysis.sort_values(by=f'avg_{value}', ascending=False)
    df_time_analysis.set_index(f'{level}', inplace=True)
    # col.write(df_time_analysis)

    col.bar_chart(df_time_analysis[f'avg_{value}'])


def pie_plot(col, df, label, value, title):
    col.markdown(f'### {title}')
    df = df.groupby(label)[value].nunique().reset_index()
    fig, ax = plt.subplots()
    ax.pie(df[value], labels=df['label'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
    col.pyplot(fig)