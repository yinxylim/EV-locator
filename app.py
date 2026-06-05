import streamlit as st
import math

# 1. PAGE CONFIG & DESIGN
st.set_page_config(page_title="Malaysia Master EV Navigator", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .main-title { font-size: 2.3rem !important; font-weight: 800 !important;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 0.2rem; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #38bdf8 !important; }
    .stExpander { background-color: #1e293b !important; border: 1px solid #334155 !important; border-radius: 12px !important; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 🎯 NATIONWIDE DATA GRID (ALL 13 STATES & 3 FT) ---
@st.cache_data
def get_master_database():
    return [
        {"state": "Johor", "town": "Johor Bahru", "building": "Mid Valley Southkey", "operator": "Gentari", "type": "DC", "kw": 180, "rate": 1.60, "dist": 0.5},
        {"state": "Kedah", "town": "Alor Setar", "building": "Aman Central", "operator": "JomCharge", "type": "DC", "kw": 60, "rate": 1.50, "dist": 0.2},
        {"state": "Kelantan", "town": "Kota Bharu", "building": "Perdana Hotel", "operator": "Gentari", "type": "DC", "kw": 60, "rate": 1.40, "dist": 0.5},
        {"state": "Melaka", "town": "Melaka City", "building": "Dataran Pahlawan", "operator": "ChargEV", "type": "DC", "kw": 50, "rate": 1.30, "dist": 0.3},
        {"state": "Negeri Sembilan", "town": "Seremban", "building": "Seremban Gateway", "operator": "TNB Electron", "type": "DC", "kw": 180, "rate": 1.50, "dist": 0.2},
        {"state": "Pahang", "town": "Kuantan", "building": "East Coast Mall", "operator": "ChargeSini", "type": "DC", "kw": 60, "rate": 1.20, "dist": 0.4},
        {"state": "Perak", "town": "Ipoh", "building": "Aeon Mall Kinta City", "operator": "Gentari", "type": "DC", "kw": 120, "rate": 1.60, "dist": 0.3},
        {"state": "Perlis", "town": "Kangar", "building": "Kangar Town Centre", "operator": "ChargEV", "type": "AC", "kw": 22, "rate": 0.90, "dist": 0.5},
        {"state": "Penang", "town": "George Town", "building": "Gurney Plaza", "operator": "Gentari", "type": "DC", "kw": 60, "rate": 1.60, "dist": 0.2},
        {"state": "Sabah", "town": "Kota Kinabalu", "building": "Imago Mall", "operator": "Gentari", "type": "DC", "kw": 60, "rate": 1.40, "dist": 0.3},
        {"state": "Sarawak", "town": "Kuching", "building": "The Spring Mall", "operator": "ChargEV", "type": "DC", "kw": 50, "rate": 1.30, "dist": 0.4},
        {"state": "Selangor", "town": "Subang Jaya", "building": "UOA Business Park", "operator": "DC Handal", "type": "DC", "kw": 200, "rate": 0.82, "dist": 0.8},
        {"state": "Terengganu", "town": "Kuala Terengganu", "building": "Mayang Mall", "operator": "ChargeSini", "type": "DC", "kw": 60, "rate": 1.20, "dist": 0.5},
        {"state": "FT Kuala Lumpur", "town": "KLCC", "building": "Suria KLCC", "operator": "Gentari", "type": "DC", "kw": 60, "rate": 1.60, "dist": 0.1},
        {"state": "FT Putrajaya", "town": "Putrajaya", "building": "IOI City Mall", "operator": "TNB Electron", "type": "DC", "kw": 180, "rate": 1.50, "dist": 0.2},
        {"state": "FT Labuan", "town": "Labuan", "building": "Labuan Financial Park", "operator": "ChargEV", "type": "AC", "kw": 22, "rate": 0.80, "dist": 0.2},
    ]

# --- VEHICLE MODELS ---
def get_vehicle_models():
    return {
        "Tesla": {"Model 3 RWD": 57.5, "Model 3 Long Range": 75.0, "Model Y Long Range": 75.0},
        "BYD": {"Seal Premium": 82.6, "Atto 3 Extended": 60.5},
        "BMW": {"iX xDrive40": 71.0, "iX3": 74.0},
        "Hyundai": {"Ioniq 5": 72.6, "Ioniq 6": 77.4}
    }

db = get_master_database()
car_db = get_vehicle_models()

# --- INTERFACE ---
st.markdown('<h1 class="main-title">⚡ Malaysia Master EV Navigator</h1>', unsafe_allow_html=True)
states = sorted(list(set(row["state"] for row in db)))
selected_state = st.selectbox("Select State / Federal Territory", states)
towns = sorted(list(set(row["town"] for row in db if row["state"] == selected_state)))
selected_town = st.selectbox("Select Town", towns)

# --- CONFIG ---
brand = st.selectbox("Select Brand", sorted(car_db.keys()))
model = st.selectbox("Select Model", sorted(car_db[brand].keys()))
battery = st.number_input("Usable Capacity (kWh)", value=car_db[brand][model])
start_soc = st.slider("Start SoC (%)", 0, 90, 20)
target_soc = st.slider("Goal SoC (%)", start_soc + 5, 100, 80)

# --- CALCULATION ---
st.markdown("### 🏆 Available Chargers")
filtered = [s for s in db if s["state"] == selected_state and s["town"] == selected_town]

for s in filtered:
    energy = battery * ((target_soc - start_soc) / 100)
    time = (energy / s["kw"]) * 60
    cost = energy * s["rate"]
    
    with st.expander(f"{s['building']} — {s['operator']} ({s['type']})"):
        c1, c2, c3 = st.columns(3)
        c1.metric("Time", f"{int(time)} mins")
        c2.metric("Cost", f"RM {cost:.2f}")
        c3.metric("Power", f"{s['kw']} kW")
