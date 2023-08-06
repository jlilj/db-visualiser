import os
import streamlit as st
import networkx as nx
import pandas as pd
import psycopg2

# Retrieve the database connection details from the environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

# Connect to PostgreSQL Database
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Query Tables and Columns
table_query = "SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('pg_catalog','information_schema');"
cursor.execute(table_query)
table_names = [row[0] for row in cursor.fetchall()]

columns_query = "SELECT table_name, column_name FROM information_schema.columns WHERE table_schema NOT IN ('pg_catalog','information_schema');"
cursor.execute(columns_query)
column_mappings = cursor.fetchall()

# Create Data Structure for Mapping
column_table_mapping = {}
for table_name, column_name in column_mappings:
    if column_name not in column_table_mapping:
        column_table_mapping[column_name] = [table_name]
    else:
        column_table_mapping[column_name].append(table_name)

# Create the Result Table (DataFrame)
result_table = pd.DataFrame(list(column_table_mapping.items()), columns=['Column', 'Used_By_Tables'])
result_table.sort_values(by='Column', inplace=True)
result_table.reset_index(drop=True, inplace=True)

# Create the NetworkX Graph
G = nx.Graph()

for _, row in result_table.iterrows():
    column = row['Column']
    tables = row['Used_By_Tables']
    for table in tables:
        G.add_edge(column, table)

# Streamlit Web Application
st.title("Column and Table Relationships")
st.write("The graph below shows the relationships between columns and tables in the database.")

# Visualize the NetworkX Graph using Streamlit
pos = nx.spring_layout(G, seed=42)  # You can choose different layouts based on your preference

# Set the node colors for tables and columns
node_colors = ['orange' if node in table_names else 'skyblue' for node in G.nodes()]

nx.draw(G, pos, with_labels=True, node_size=5000, node_color=node_colors, font_size=10, font_weight='bold')
st.pyplot()

# Display the Result Table
st.write("Table of columns and their corresponding tables:")
st.dataframe(result_table)