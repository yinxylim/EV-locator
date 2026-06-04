import streamlit as st
import requests
import pandas as pd

# The API URL for Malaysia (Country Code 'MY')
API_URL = "https://api.openchargemap.io/v3/poi/?output=json&countrycode=MY&maxresults=500&compact=true&verbose=false"

@st.cache_data(ttl=3600) # Cache for 1 hour to stay under API limits
def get_ev_chargers():
    response = requests.get(API_URL)
    data = response.json()
    
    # Process the data into a format we can use
    chargers = []
    for item in data:
        chargers.append({
            'Station': item.get('AddressInfo', {}).get('Title'),
            'lat': item.get('AddressInfo', {}).get('Latitude'),
            'lon': item.get('AddressInfo', {}).get('Longitude'),
            'Address': item.get('AddressInfo', {}).get('AddressLine1')
        })
    return pd.DataFrame(chargers)

df = get_ev_chargers()
st.write(df) # This will display the list automatically!
