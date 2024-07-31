import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# API details
BASE_URL = "https://data.gov.sg/api/action/datastore_search"
RESOURCE_ID = "d_3f960c10fed6145404ca7b821f263b87"

def fetch_data(query=None, limit=1000):
    url = f"{BASE_URL}?resource_id={RESOURCE_ID}"
    if query:
        url += f"&q={query}"
    url += f"&limit={limit}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']['records']
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return []

# Streamlit app
st.title('ACRA Search')

# Create three columns for search inputs
col1, col2, col3 = st.columns(3)

# Search bar for general search
with col1:
    search_term = st.text_input('Enter search term')

# Year input for uen_issue_date search
with col2:
    search_year = st.number_input('Enter year to search', min_value=1800, max_value=datetime.now().year, value=None)

# Entity type filter
with col3:
    entity_types = ["All", "LL", "BN", "LC", "FC", "LP", "PF", "VC"]  # Add more types as needed
    selected_entity_type = st.selectbox('Select entity type', entity_types)

# Search functionality
if search_term or search_year or selected_entity_type != "All":
    query = []
    
    if search_term:
        query.append(search_term)
    
    if search_year:
        query.append(str(search_year))
    
    query_string = " ".join(query)
    
    results = fetch_data(query_string)
    
    if results:
        df_results = pd.DataFrame(results)
        
        # Filter for uen_status = "R"
        df_results = df_results[df_results['uen_status'].str.lower() == 'r']
        
        # Filter results by year if search_year is provided
        if search_year:
            df_results = df_results[df_results['uen_issue_date'].str[:4] == str(search_year)]
        
        # Filter by entity_type if selected
        if selected_entity_type != "All":
            df_results = df_results[df_results['entity_type'] == selected_entity_type]
        
        # Select only specific columns
        columns_to_show = ['entity_name', 'uen', 'entity_type', 'uen_issue_date', 'reg_postal_code']
        df_results = df_results[columns_to_show]
        
        # Randomly select up to 20 results
        if len(df_results) > 20:
            df_results = df_results.sample(n=20)
        
        # Reset index to start from 1
        df_results = df_results.reset_index(drop=True)
        df_results.index += 1
        
        st.write('Search Results:', df_results)
        st.write(f'Number of results: {len(df_results)}')
    else:
        st.write('No results found.')
else:
    st.write('Enter search criteria and press enter to begin a search')