import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 1. Setup Page
st.set_page_config(page_title="MY EV Finder", layout="wide")
st.title("⚡ Malaysia EV Charger Locator")

# 2. Load Data (Replace this with a link to your Google Sheet or CSV)
# For now, we use a small sample dataset
data = {
    'Station': ['JomCharge - Subang', 'Gentari - KLCC', 'ChargEV - Sunway'],
    'lat': [3.0738, 3.1575, 3.0673],
    'lon': [101.6064, 101.7119, 101.6030],
    'Type': ['DC', 'DC', 'AC']
}
df = pd.DataFrame(data)

# 3. Sidebar Filters
st.sidebar.header("Filter Options")
charger_type = st.sidebar.multiselect("Select Charger Type", options=df['Type'].unique(), default=df['Type'].unique())

# Filter data
filtered_df = df[df['Type'].isin(charger_type)]

# 4. Map Display
st.subheader("Chargers Near You")
m = folium.Map(location=[3.1, 101.6], zoom_start=11)

for _, row in filtered_df.iterrows():
    folium.Marker(
        [row['lat'], row['lon']], 
        popup=row['Station'],
        icon=folium.Icon(color="green" if row['Type'] == 'DC' else "blue")
    ).add_to(m)

st_folium(m, width=700, height=500)
