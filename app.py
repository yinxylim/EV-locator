import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Malaysia Master EV Navigator", page_icon="⚡", layout="centered")

# --- EXPANDED DATABASE ---
@st.cache_data
def get_master_database():
    return [
        {"state": "Johor", "town": "Johor Bahru", "building": "Mid Valley Southkey", "operator": "Gentari", "kw": 180, "rate": 1.60},
        {"state": "Kedah", "town": "Alor Setar", "building": "Aman Central", "operator": "JomCharge", "kw": 60, "rate": 1.50},
        {"state": "Kelantan", "town": "Kota Bharu", "building": "AEON Mall", "operator": "Gentari", "kw": 60, "rate": 1.40},
        {"state": "Melaka", "town": "Melaka City", "building": "Dataran Pahlawan", "operator": "ChargEV", "kw": 50, "rate": 1.30},
        {"state": "Negeri Sembilan", "town": "Seremban", "building": "Seremban Gateway", "operator": "TNB Electron", "kw": 180, "rate": 1.50},
        {"state": "Pahang", "town": "Kuantan", "building": "East Coast Mall", "operator": "ChargeSini", "kw": 60, "rate": 1.20},
        {"state": "Perak", "town": "Ipoh", "building": "AEON Kinta City", "operator": "Gentari", "kw": 120, "rate": 1.60},
        {"state": "Perlis", "town": "Kangar", "building": "Kangar Town Centre", "operator": "ChargEV", "kw": 22, "rate": 0.90},
        {"state": "Penang", "town": "George Town", "building": "Gurney Plaza", "operator": "Gentari", "kw": 60, "rate": 1.60},
        {"state": "Sabah", "town": "Kota Kinabalu", "building": "Imago Mall", "operator": "Gentari", "kw": 60, "rate": 1.40},
        {"state": "Sarawak", "town": "Kuching", "building": "The Spring Mall", "operator": "ChargEV", "kw": 50, "rate": 1.30},
        {"state": "Selangor", "town": "Subang Jaya", "building": "UOA Business Park", "operator": "DC Handal", "kw": 200, "rate": 0.82},
        {"state": "Terengganu", "town": "Kuala Terengganu", "building": "Mayang Mall", "operator": "ChargeSini", "kw": 60, "rate": 1.20},
        {"state": "FT Kuala Lumpur", "town": "KLCC", "building": "Suria KLCC", "operator": "Gentari", "kw": 60, "rate": 1.60},
        {"state": "FT Putrajaya", "town": "Putrajaya", "building": "IOI City Mall", "operator": "TNB Electron", "kw": 180, "rate": 1.50},
        {"state": "FT Labuan", "town": "Labuan", "building": "Financial Park", "operator": "ChargEV", "kw": 22, "rate": 0.80}
    ]

# --- COMPREHENSIVE VEHICLE LIST ---
def get_vehicle_models():
    return {
        "Tesla": {"Model 3 RWD": 57.5, "Model 3 Long Range": 75.0, "Model Y RWD": 57.5, "Model Y Long Range": 75.0},
        "BYD": {"Dolphin Standard": 44.9, "Dolphin Extended": 60.5, "Atto 3 Standard": 49.9, "Atto 3 Extended": 60.5, "Seal Premium": 82.6, "Seal Performance": 82.6},
        "Proton e.MAS": {"e.MAS 5 Prime": 30.1, "e.MAS 5 Premium": 40.2, "e.MAS 7 Prime": 49.5, "e.MAS 7 Premium": 60.2},
        "BMW": {"iX xDrive40": 71.0, "iX3": 74.0, "i4 eDrive40": 80.7},
        "Hyundai": {"Ioniq 5": 72.6, "Ioniq 6": 77.4},
        "MG": {"MG4 Standard": 51.0, "MG4 Luxury": 64.0, "MG4 XPower": 64.0, "ZS EV": 51.0},
        "GWM": {"Ora Good Cat Ultra": 63.1, "Ora Good Cat GT": 63.1},
        "Neta": {"Neta V": 38.5, "Neta X": 62.0},
        "Zeekr": {"Zeekr X Premium": 66.0, "Zeekr X Flagship": 66.0},
        "Porsche": {"Taycan": 71.0, "Taycan 4S": 89.0}
    }

# --- APP INTERFACE ---
st.markdown('<h1 style="text-align: center;">⚡ Malaysia Master EV Navigator</h1>', unsafe_allow_html=True)
db = get_master_database()
cars = get_vehicle_models()

col1, col2 = st.columns(2)
selected_state = col1.selectbox("State", sorted(list(set(s["state"] for s in db))))
selected_town = col2.selectbox("Town", sorted(list(set(s["town"] for s in db if s["state"] == selected_state))))

brand = st.selectbox("Car Brand", sorted(cars.keys()))
model = st.selectbox("Car Model", sorted(cars[brand].keys()))
battery = st.number_input("Usable Capacity (kWh)", value=cars[brand][model])

start_soc = st.slider("Start SoC (%)", 0, 90, 20)
target_soc = st.slider("Goal SoC (%)", start_soc + 5, 100, 80)

# --- RESULTS ---
filtered = [s for s in db if s["state"] == selected_state and s["town"] == selected_town]
st.subheader("📍 Available Chargers")

for s in filtered:
    energy = battery * ((target_soc - start_soc) / 100)
    time = (energy / s["kw"]) * 60
    cost = energy * s["rate"]
    with st.expander(f"{s['building']} ({s['operator']})"):
        c1, c2, c3 = st.columns(3)
        c1.metric("Time", f"{int(time)} mins")
        c2.metric("Cost", f"RM {cost:.2f}")
        c3.metric("Power", f"{s['kw']} kW")
