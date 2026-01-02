import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="Silent Guardian AI",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def load_css():
    # Load External CSS
    with open('assets/style.css') as f:
        st.markdown('<style>' + f.read() + '</style>', unsafe_allow_html=True)
    
def get_gps_location():
    """
    Simulates a 'Get GPS' button by injecting JS.
    In a real app, this would use the browser's Geolocation API.
    For this prototype, we'll use a Streamlit-friendly workaround or simulation.
    """
    # Simple JS to get location and reload page with params
    # Note: This is an advanced technique. For simplicity/reliability in this environment, 
    # we will use the 'Locate Me' button logic in app.py to trigger this.
    pass

LOCATIONS = ["City Street", "Crowded Market", "Bus Stand", "Lonely Alley", "Public Festival"]
LIGHTING = ["Bright Daylight", "Dusk/Dawn", "Street Lights (Good)", "Dim Light", "Pitch Dark"]
CROWD = ["Empty", "Sparse", "Moderate", "Dense", "Stampede Risk"]
MODES = ["Normal Mode", "Women Safety Mode", "Elderly Safety Mode"]

@st.cache_data
def reverse_geocode(lat, lon):
    """
    Fetches address from coordinates using OpenStreetMap Nominatim API (Free).
    """
    try:
        import urllib.request
        import json
        
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'SilentGuardianAI/1.0'})
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get('display_name', "Unknown Location")
    except Exception as e:
        return f"GPS Location ({lat:.4f}, {lon:.4f})"
