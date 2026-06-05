import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Malaysia EV Navigator", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 2.3rem !important; font-weight: 800 !important;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- EXPANDED DATABASE ---
@st.cache_data
def get_master_database():
    return [
        # Highway/Interstate
        {"state": "Johor", "town": "PLUS Highway (South)", "building": "Pagoh RSA Northbound", "operator": "TNB Electron", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.1},
        {"state": "Selangor", "town": "PLUS Highway (Central)", "building": "Dengkil RSA", "operator": "TNB Electron", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.2},
        # Penang
        {"state": "Penang", "town": "George Town", "building": "Gurney Plaza", "operator": "Gentari", "type": "DC", "kw": 60, "rate": 1.60, "dist": 0.3},
        {"state": "Penang", "town": "Bayan Lepas", "building": "SPICE Arena", "operator": "ChargEV", "type": "AC", "kw": 22, "rate": 0.80, "dist": 1.2},
        # Johor Bahru
        {"state": "Johor", "town": "Johor Bahru", "building": "Mid Valley Southkey", "operator": "Gentari", "type": "DC", "kw": 180, "rate": 1.60, "dist": 0.5},
        {"state": "Johor", "town": "Johor Bahru", "building": "R&F Mall", "operator": "ChargEV", "type": "DC", "kw": 60, "rate": 1.40, "dist": 0.8},
        # Pahang (Kuantan)
        {"state": "Pahang", "town": "Kuantan", "building": "East Coast Mall", "operator": "ChargeSini", "type": "DC", "kw": 60, "rate": 1.20, "dist": 0.5},
        {"state": "Pahang", "town": "Kuantan", "building": "Kuantan City Mall", "operator": "Gentari", "type": "DC", "kw": 120, "rate": 1.50, "dist": 0.6},
        # East Malaysia
        {"state": "Sarawak", "town": "Kuching", "building": "The Spring Mall", "operator": "ChargEV", "type": "DC", "kw": 50, "rate": 1.30, "dist": 0.4},
        {"state": "Sarawak", "town": "Kuching", "building": "Vivacity Megamall", "operator": "JomCharge", "type": "DC", "kw": 60, "rate": 1.40, "dist": 0.7},
        {"state": "Sabah", "town": "Kota Kinabalu", "building": "Imago Mall", "operator": "Gentari", "type": "DC", "kw": 60, "rate": 1.40, "dist": 0.3},
        {"state": "Sabah", "town": "Kota Kinabalu", "building": "Suria Sabah", "operator": "ChargeSini", "type": "DC", "kw": 50, "rate": 1.20, "dist": 0.4},
    ]

# --- VEHICLE MODELS ---
def get_vehicle_models():
    return {
        "Tesla": {"Model 3 Long Range": 75.0, "Model Y Long Range": 75.0},
        "BYD": {"Seal Premium": 82.6, "Atto 3 Extended": 60.5},
        "BMW": {"iX xDrive40": 71.0, "iX3": 74.0}
    }

# --- APP INTERFACE ---
st.markdown('<h1 class="main-title">Malaysia EV Navigator</h1>', unsafe_allow_html=True)
db = get_master_database()
cars = get_vehicle_models()

# Location Selectors
states = sorted(list(set(row["state"] for row in db)))
col1, col2 = st.columns(2)
selected_state = col1.selectbox("State", states)
towns = sorted(list(set(row["town"] for row in db if row["state"] == selected_state)))
selected_town = col2.selectbox("Town", towns)

# Car Selectors
brand = st.selectbox("Car Brand", list(cars.keys()))
model = st.selectbox("Car Model", list(cars[brand].keys()))
cap = st.number_input("Battery (kWh)", value=cars[brand][model])

s1, s2 = st.columns(2)
start_soc = s1.slider("Start SoC (%)", 0, 90, 20)
target_soc = s2.slider("Target SoC (%)", start_soc + 5, 100, 80)

# Results
filtered = [s for s in db if s["town"] == selected_town]
st.subheader("📍 Available Chargers")
for s in filtered:
    energy = cap * ((target_soc - start_soc) / 100)
    time = (energy / s["kw"]) * 60
    cost = energy * s["rate"]
    
    with st.expander(f"{s['building']} ({s['operator']})"):
        st.write(f"**Est. Time:** {int(time)} mins | **Est. Cost:** RM {cost:.2f}")
