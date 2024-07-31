import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import datetime

# Create an SQLite database
engine = create_engine('sqlite:///local_database.db')

# Load CSV data into a DataFrame
df = pd.read_csv('data/EntitiesRegisteredwithACRA.csv')

# Filter the DataFrame to only include rows where uen_status is 'R'
df_filtered = df[df['uen_status'] == 'R']

# Write filtered DataFrame to SQLite database
df_filtered.to_sql('data_table', engine, if_exists='replace', index=False)

# Streamlit app
st.title('ACRA Search')

# Create two columns for search inputs
col1, col2 = st.columns(2)

# Search bar for general search
with col1:
    search_term = st.text_input('Enter search term')

# Year input for uen_issue_date search
with col2:
    search_year = st.number_input('Enter year to search', min_value=1800, max_value=datetime.datetime.now().year, value=None)

# Search functionality
if search_term or search_year:
    query = "SELECT * FROM data_table WHERE 1=1"
    
    if search_term:
        query += f""" 
        AND (
            uen LIKE '%{search_term}%' 
            OR issuance_agency_id LIKE '%{search_term}%'
            OR entity_name LIKE '%{search_term}%'
            OR entity_type LIKE '%{search_term}%'
            OR reg_street_name LIKE '%{search_term}%'
            OR reg_postal_code LIKE '%{search_term}%'
        )
        """
    
    if search_year:
        query += f" AND strftime('%Y', uen_issue_date) = '{search_year}'"
    
    # Add ORDER BY RANDOM() and LIMIT 20 to get 20 random results
    query += " ORDER BY RANDOM() LIMIT 20"
    
    results = pd.read_sql_query(query, engine)
    st.write('Search Results:', results)
else:
    st.write('Enter name or year and press enter to begin a search')