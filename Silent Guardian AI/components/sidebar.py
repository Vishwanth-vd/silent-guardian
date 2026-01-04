import streamlit as st
from utils import LOCATIONS, LIGHTING, CROWD, MODES, reverse_geocode

def render_sidebar():
    with st.sidebar:
        # --- Identity Header ---
        st.markdown("""
        <div style="text-align: center; margin-bottom: 20px; padding: 20px; background: linear-gradient(135deg, rgba(0,201,255,0.1), rgba(0,0,0,0)); border-radius: 20px; border: 1px solid rgba(0,201,255,0.2);">
            <div style="font-size: 80px; filter: drop-shadow(0 0 15px rgba(0,201,255,0.6));">🛡️</div>
            <h2 style="margin: 10px 0 0 0; font-size: 1.5rem; background: linear-gradient(to right, #00C9FF, #92FE9D); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">SILENT GUARDIAN</h2>
            <p style="font-size: 0.8rem; letter-spacing: 2px; opacity: 0.7; margin: 0;">AI SAFETY SYSTEM v2.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- Mode Selection (Prominent) ---
        st.markdown("##### 🛡️ Select Active Mode")
        mode = st.radio("Guardian Mode", MODES, label_visibility="collapsed")
        
        st.markdown("---")
        
        # --- Navigation Section ---
        with st.expander("📍 NAVIGATION CONTROLS", expanded=True):
            # GPS Button with JS
            gps_js = """
            <button onclick="getLocation()" class="gps-btn">⌖ DETECT MY LOCATION</button>
            <script>
            function getLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(showPosition);
                } else { 
                    alert("Geolocation is not supported by this browser.");
                }
            }
            function showPosition(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const url = new URL(window.location.href);
                url.searchParams.set('lat', lat);
                url.searchParams.set('lon', lon);
                window.location.href = url.toString();
            }
            </script>
            <style>
            .gps-btn {
                background: linear-gradient(45deg, #00C9FF, #92FE9D);
                border: none;
                padding: 12px;
                color: #050510;
                border-radius: 8px;
                font-weight: 800;
                letter-spacing: 1px;
                cursor: pointer;
                width: 100%;
                margin-bottom: 10px;
                transition: 0.3s;
                text-transform: uppercase;
                font-family: 'Orbitron', sans-serif;
            }
            .gps-btn:hover {
                box-shadow: 0 0 20px rgba(0, 201, 255, 0.6);
                transform: translateY(-2px);
            }
            </style>
            """
            
            use_gps = st.checkbox("Use GPS Coordinates", value=True)
            
            if use_gps:
                qp = st.query_params
                lat = float(qp.get("lat", 0))
                lon = float(qp.get("lon", 0))
                
                if lat != 0 and lon != 0:
                    address = reverse_geocode(lat, lon)
                    st.success(f"**{address}**")
                    location = address 
                else:
                    location = "GPS Location (Detecting...)"
                    st.caption("Waiting for signal...")
                
                st.components.v1.html(gps_js, height=60)
            else:
                location = st.text_input("Start Point", "Central Bus Stand")
                
            destination = st.text_input("Destination", "City University")
            
            # Google Maps Link
            if use_gps:
                gmaps_url = f"https://www.google.com/maps/dir/?api=1&destination={destination.replace(' ', '+')}&travelmode=walking"
            else:
                gmaps_url = f"https://www.google.com/maps/dir/?api=1&origin={location.replace(' ', '+')}&destination={destination.replace(' ', '+')}&travelmode=walking"
            
            st.link_button("🗺️ Open Google Maps", gmaps_url, use_container_width=True)

        # --- Settings Section ---
        with st.expander("⚙️ SIMULATION SETTINGS", expanded=False):
            # Live Simulation Toggle
            is_live = st.toggle("🔴 CONNECT LIVE SENSORS", value=False)
            
            if not is_live:
                st.caption("Manual Override Active")
                time_hour = st.slider("Time (24h)", 0, 23, 22)
                
                # Dynamic Defaults based on Location
                # Logic: If location changed, update session state defaults
                if "last_location" not in st.session_state or st.session_state.last_location != location:
                    # Fetch profile
                    # We need access to sim instance, but sidebar is decoupled. 
                    # Ideally passed in, but we can do a quick lookup relative to our known lists or import sim class.
                    # Better: logic in app.py or quick lookup here.
                    from modules.simulation import SafetySimulator
                    temp_sim = SafetySimulator()
                    profile = temp_sim.get_location_profile(location)
                    
                    st.session_state.default_lighting = profile['lighting']
                    st.session_state.default_crowd = profile['crowd']
                    st.session_state.last_location = location
                
                # Use session state for values so they can be overridden by user too
                def_light = st.session_state.get("default_lighting", "Dim Light")
                def_crowd = st.session_state.get("default_crowd", "Sparse")

                try:
                    light_idx = LIGHTING.index(def_light)
                    crowd_idx = CROWD.index(def_crowd)
                except:
                    light_idx, crowd_idx = 3, 1

                lighting = st.select_slider("Lighting", options=LIGHTING, value=LIGHTING[light_idx])
                crowd = st.select_slider("Crowd Density", options=CROWD, value=CROWD[crowd_idx])
            else:
                st.caption("Streaming Data from Nodes...")
                time_hour = 23 # Late night live
                lighting = "Dim Light"
                crowd = "Empty"
            
            st.markdown("#### Crisis Injection")
            crisis_action = st.selectbox("Trigger Event", ["None", "Power Failure", "Crowd Surge", "Road Block"], label_visibility="collapsed")

        # --- Emergency Section ---
        st.markdown("---")
        st.markdown("### 🚨 EMERGENCY OVERRIDE")
        with st.expander("🆘 SOS Configuration", expanded=True):
            sos_name = st.text_input("Emergency Contact Name", value="Mom")
            sos_phone = st.text_input("Emergency Phone", value="+91 99999 99999")
            
        if st.button("🆘 TRIGGER SOS BEACON", type="primary"):
            # 1. Log to file to prove transmission
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] SOS SENT TO {sos_name} ({sos_phone}) | Location: {location}\n"
            
            with open("sos_logs.txt", "a") as f:
                f.write(log_entry)

            st.toast(f"SOS SENT TO {sos_name.upper()} ({sos_phone})!", icon="🚨")
            st.error(f"EMERGENCY SIGNAL BROADCASTED: Alerting {sos_name}...")
            st.info(f"Log recorded in: sos_logs.txt")
            
    return {
        "mode": mode,
        "location": location,
        "destination": destination,
        "time_hour": time_hour,
        "lighting": lighting,
        "crowd": crowd,
        "crisis_action": crisis_action,
        "is_live": is_live
    }

