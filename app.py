import streamlit as st
import requests
import pandas as pd

@st.cache_data(ttl=3600)
def get_ev_chargers():
    try:
        response = requests.get(API_URL)
        
        # Check if the request was successful (status code 200)
        response.raise_for_status() 
        
        # Try to parse the JSON
        data = response.json()
        
        # Process the data
        chargers = []
        for item in data:
            chargers.append({
                'Station': item.get('AddressInfo', {}).get('Title'),
                'lat': item.get('AddressInfo', {}).get('Latitude'),
                'lon': item.get('AddressInfo', {}).get('Longitude'),
                'Address': item.get('AddressInfo', {}).get('AddressLine1')
            })
        return pd.DataFrame(chargers)
        
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.JSONDecodeError:
        st.error("The server did not return valid JSON. Check if the URL is correct or if the API is down.")
    except Exception as err:
        st.error(f"An error occurred: {err}")
    
    return pd.DataFrame() # Return empty dataframe on error
