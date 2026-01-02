import streamlit as st
import time

# -- Imports from our new structure --
from modules.simulation import SafetySimulator
from modules.risk_engine import RiskEngine
from modules.prevention import GuardianAI
from modules.sentinel import Sentinel

from components.sidebar import render_sidebar
from components.dashboard import render_metrics, render_alert
from components.map_view import render_map
from components.chat import render_chat

from utils import set_page_config, load_css

# --- Initialization ---
# Simple caching to avoid reloading heavy models if we had them
if 'sim' not in st.session_state:
    st.session_state.sim = SafetySimulator()
    st.session_state.risk_engine = RiskEngine()
    st.session_state.guardian = GuardianAI()
    st.session_state.sentinel = Sentinel()

sim = st.session_state.sim
risk_engine = st.session_state.risk_engine
guardian = st.session_state.guardian
sentinel = st.session_state.sentinel

set_page_config()
load_css()

# --- Application Logic ---

# 1. Sidebar & Control
params = render_sidebar() 

# 2. Logic Pipeline
# Check for GPS Params
query_params = st.query_params
gps_lat = float(query_params.get("lat", 12.9716))
gps_lon = float(query_params.get("lon", 77.5946))

# Determine Start Position
# Determine Start Position
if "GPS" in params['location']:
    current_pos = [gps_lon, gps_lat]
else:
    # Use deterministic visual simulation for manual inputs
    current_pos = sim._get_simulated_coordinates(params['location'])

# Prepare Simulation Params
sim_params = {
    "location": params['location'], 
    "lighting": params['lighting'], 
    "crowd": params['crowd'], 
    "time_hour": params['time_hour'], 
    "escape_routes": 1
}

# Apply Crisis
if params['crisis_action'] != "None":
    sim_params = sim.run_simulation_step(sim_params, params['crisis_action'])

# Calculate Risk
score, esi, factors = risk_engine.calculate_risk_score(sim_params, params['mode'])

# Sentinel (Live Data)
sentinel_data = None
path_tracking = [current_pos] # Path history

if params['is_live']:
    # Initialize path tracking
    if 'path_progress' not in st.session_state:
        st.session_state.path_progress = 0
    
    # Generate Route (Source -> Dest)
    # We pass the CURRENT GPS position as the start
    risky, safer = sim.generate_route(current_pos, params['destination'])
    
    # Update Position (Simulation of movement along path)
    current_pos, next_idx = sentinel.update_user_position(safer, st.session_state.path_progress)
    st.session_state.path_progress = next_idx
    
    # In live mode, we auto-refresh
    sentinel_data = sentinel.get_live_metrics(score)
    time.sleep(1.5)
    st.rerun()
else:
    risky, safer = sim.generate_route(current_pos, params['destination'])

# --- Main Dashboard ---
st.title("🛡️ Silent Guardian AI")

# KPIs
render_metrics(score, esi, sim_params['crowd'], params['mode'], sentinel_data)
render_alert(score)

st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🗺️ Live Map", "🤖 Guardian", "📊 Sentinel Analytics"])

with tab1:
    # We pass the dynamic routes
    heatmap = sim.generate_heatmap_data()
    render_map(sim, safer, risky, heatmap, current_pos)
    
    st.markdown("---")
    # Embed Google Maps
    # Use the raw location/destination strings from params
    # Note: params['location'] might be "GPS Location (Detected)" or a real address
    src_val = "My Location" if "GPS" in params['location'] else params['location']
    from components.map_view import render_google_maps_embed
    render_google_maps_embed(src_val, params['destination'])

with tab2:
    render_chat(guardian, score)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Risk Factors")
        if factors:
            for f in factors:
                st.warning(f"• {f}")
        else:
            st.success("No critical risk factors.")
            
        st.markdown("### Suggested Actions")
        actions = guardian.suggest_actions(score, factors, params['mode'])
        for a in actions:
            st.info(a)
    with c2:
        st.subheader("Community Statistics")
        pulse = sim.get_community_pulse()
        st.line_chart(pulse.set_index("Day"))
        
        if sentinel_data:
            st.markdown("### Biometric Logs")
            st.json(sentinel_data)

# Footer
st.markdown("---")
st.caption("Silent Guardian AI | Real-Time Protection System")
