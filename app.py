import streamlit as st

st.set_page_config(page_title="Malaysia EV Navigator", page_icon="⚡", layout="centered")

# --- COMPREHENSIVE DATABASE (ALL STATES & KEY CITIES) ---
@st.cache_data
def get_master_database():
    return [
        {"state": "Johor", "town": "Johor Bahru", "building": "Mid Valley Southkey", "operator": "Gentari", "kw": 180, "rate": 1.60},
        {"state": "Johor", "town": "Batu Pahat", "building": "BP Mall", "operator": "ChargEV", "kw": 50, "rate": 1.40},
        {"state": "Kedah", "town": "Alor Setar", "building": "Aman Central", "operator": "JomCharge", "kw": 60, "rate": 1.50},
        {"state": "Kelantan", "town": "Kota Bharu", "building": "AEON Mall", "operator": "Gentari", "kw": 60, "rate": 1.40},
        {"state": "Melaka", "town": "Melaka City", "building": "Dataran Pahlawan", "operator": "ChargEV", "kw": 50, "rate": 1.30},
        {"state": "Negeri Sembilan", "town": "Seremban", "building": "Seremban Gateway", "operator": "TNB Electron", "kw": 180, "rate": 1.50},
        {"state": "Pahang", "town": "Kuantan", "building": "East Coast Mall", "operator": "ChargeSini", "kw": 60, "rate": 1.20},
        {"state": "Penang", "town": "George Town", "building": "Gurney Plaza", "operator": "Gentari", "kw": 60, "rate": 1.60},
        {"state": "Penang", "town": "Butterworth", "building": "Sunway Carnival", "operator": "Gentari", "kw": 180, "rate": 1.60},
        {"state": "Perak", "town": "Ipoh", "building": "AEON Kinta City", "operator": "Gentari", "kw": 120, "rate": 1.60},
        {"state": "Perak", "town": "Taiping", "building": "Taiping Mall", "operator": "ChargEV", "kw": 50, "rate": 1.30},
        {"state": "Perlis", "town": "Kangar", "building": "Kangar Town Centre", "operator": "ChargEV", "kw": 22, "rate": 0.90},
        {"state": "Sabah", "town": "Kota Kinabalu", "building": "Imago Mall", "operator": "Gentari", "kw": 60, "rate": 1.40},
        {"state": "Sabah", "town": "Sandakan", "building": "Harbour Mall", "operator": "ChargeSini", "kw": 50, "rate": 1.30},
        {"state": "Sarawak", "town": "Kuching", "building": "The Spring Mall", "operator": "ChargEV", "kw": 50, "rate": 1.30},
        {"state": "Sarawak", "town": "Miri", "building": "Bintang Megamall", "operator": "JomCharge", "kw": 60, "rate": 1.40},
        {"state": "Selangor", "town": "Subang Jaya", "building": "UOA Business Park", "operator": "DC Handal", "kw": 200, "rate": 0.82},
        {"state": "Selangor", "town": "Petaling Jaya", "building": "Sunway Pyramid", "operator": "TNB Electron", "kw": 180, "rate": 1.50},
        {"state": "Terengganu", "town": "Kuala Terengganu", "building": "Mayang Mall", "operator": "ChargeSini", "kw": 60, "rate": 1.20},
        {"state": "FT Kuala Lumpur", "town": "KLCC", "building": "Suria KLCC", "operator": "Gentari", "kw": 60, "rate": 1.60},
        {"state": "FT Putrajaya", "town": "Putrajaya", "building": "IOI City Mall", "operator": "TNB Electron", "kw": 180, "rate": 1.50},
        {"state": "FT Labuan", "town": "Labuan", "building": "Financial Park", "operator": "ChargEV", "kw": 22, "rate": 0.80}
    ]

# --- APP INTERFACE ---
st.title("⚡ Malaysia Master EV Navigator")

db = get_master_database()
all_states = sorted(list(set(s["state"] for s in db)))

selected_state = st.selectbox("Select State", all_states)
# Filter towns based on the selected state
available_towns = sorted(list(set(s["town"] for s in db if s["state"] == selected_state)))
selected_town = st.selectbox("Select Town", available_towns)

# ... (Insert your vehicle and calculation logic here)
