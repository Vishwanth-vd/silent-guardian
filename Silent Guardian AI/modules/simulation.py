import random
import pandas as pd
import numpy as np
from utils import LOCATIONS, LIGHTING, CROWD, geocode_address


class SafetySimulator:
    def __init__(self):
        pass

    def generate_scenario_inputs(self):
        """Generates random default values for a simulation."""
        return {
            "location": random.choice(LOCATIONS),
            "lighting": random.choice(LIGHTING),
            "crowd": random.choice(CROWD),
            "time_hour": random.randint(0, 23),
            "escape_routes": random.randint(0, 3)
        }

    def get_location_profile(self, location_name):
        """Returns specific risk parameters if a location profile exists."""
        return self.LOCATION_PROFILES.get(location_name, {
            "crowd": "Moderate", "lighting": "Street Lights (Good)"
        })


    # Real-world coordinates for Bangalore (approx)
    REAL_WORLD_LOCATIONS = {
        "Central Bus Stand": [77.5727, 12.9778], # Majestic
        "Bus Stand": [77.5727, 12.9778],         # Majestic (Alias)
        "City University": [77.5878, 12.9723],   # Central College
        "City Street": [77.6067, 12.9755],       # MG Road
        "Crowded Market": [77.5759, 12.9631],    # KR Market
        "Lonely Alley": [77.5925, 12.9774],      # Cubbon Periphery
        "Public Festival": [77.5879, 12.9972],   # Palace Grounds
        "Home": [77.6046, 12.9816],
        "University": [77.5878, 12.9723],
        "City Center": [77.5946, 12.9716],
        "Metro Station": [77.6100, 12.9600]
    }

    LOCATION_PROFILES = {
        "Central Bus Stand": {"crowd": "Dense", "lighting": "Street Lights (Good)"},
        "Bus Stand": {"crowd": "Dense", "lighting": "Street Lights (Good)"},
        "City University": {"crowd": "Moderate", "lighting": "Bright Daylight"},
        "City Street": {"crowd": "Moderate", "lighting": "Street Lights (Good)"},
        "Crowded Market": {"crowd": "Stampede Risk", "lighting": "Dim Light"},
        "Lonely Alley": {"crowd": "Empty", "lighting": "Pitch Dark"},
        "Public Festival": {"crowd": "Stampede Risk", "lighting": "Bright Daylight"},
        "Metro Station": {"crowd": "Dense", "lighting": "Bright Daylight"},
        "Home": {"crowd": "Sparse", "lighting": "Bright Daylight"}
    }


    def generate_heatmap_data(self, center_pos=None, num_points=100):
        """Generates synthetic lat/lon data for risk hotspots around a center point."""
        # Use provided center or default
        if center_pos:
            base_lat, base_lon = center_pos[1], center_pos[0]
        else:
            base_lat, base_lon = 12.9716, 77.5946
        
        data = []
        for _ in range(num_points):
            lat_off = random.uniform(-0.015, 0.015) # tighter cluster
            lon_off = random.uniform(-0.015, 0.015)
            risk = random.random() # 0 to 1 intensity
            data.append([base_lat + lat_off, base_lon + lon_off, risk])
            
        df = pd.DataFrame(data, columns=['lat', 'lon', 'intensity'])
        return df

    def get_community_pulse(self):
        """Simulates community sentiment trends."""
        # 7 days of data
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        safe_counts = [random.randint(50, 100) for _ in days]
        unsafe_counts = [random.randint(5, 30) for _ in days]
        
        return pd.DataFrame({
            "Day": days,
            "Felt Safe": safe_counts,
            "Felt Unsafe": unsafe_counts
        })

    def _get_simulated_coordinates(self, text_input):
        """
        Generates a deterministic lat/lon based on the input text.
        Prioritizes known real-world locations, otherwise hashes.
        """
        if not text_input or text_input == "GPS Location":
            return [77.5946, 12.9716] # Default Center

        # Check for exact match in known locations
        if text_input in self.REAL_WORLD_LOCATIONS:
            return self.REAL_WORLD_LOCATIONS[text_input]

        # Try Geocoding
        geo_coords = geocode_address(text_input)
        if geo_coords:
            return geo_coords
            
        hash_val = hash(text_input)
        # Map hash to a small offset around the center city
        lat_off = (hash_val % 100) / 2000.0  # +/- 0.05
        lon_off = ((hash_val >> 2) % 100) / 2000.0
        
        return [77.5946 + lon_off, 12.9716 + lat_off]

    def run_simulation_step(self, current_params, action=None):
        """
        Modifies parameters based on a 'What-If' action.
        action: 'Power Failure', 'Crowd Surge', 'Medical Emergency', 'Road Block'
        """
        new_params = current_params.copy()
        
        if action == "Power Failure":
            new_params["lighting"] = "Pitch Dark"
        elif action == "Crowd Surge":
            new_params["crowd"] = "Stampede Risk"
        elif action == "Road Block":
            new_params["escape_routes"] = 0
        
        return new_params

    def generate_route(self, start_pos, destination_name):
        """
        Generates routes from dynamic start_pos [lon, lat] to a destination.
        """
        # Hardcoded locations for demo
        destinations = {
            "Home": [77.6046, 12.9816],
            "University": [77.5800, 12.9700],
            "City Center": [77.5946, 12.9716],
            "Metro Station": [77.6100, 12.9600]
        }
        
        start = start_pos
        
        # Look up or simulate destination
        # Look up or simulate destination
        if destination_name in self.REAL_WORLD_LOCATIONS:
            end = self.REAL_WORLD_LOCATIONS[destination_name]
        elif destination_name in destinations:
            end = destinations[destination_name]
        else:
            # Try Geocoding
            geo_coords = geocode_address(destination_name)
            if geo_coords:
                end = geo_coords
            else:
                # Deterministic simulation relative to start so it's not far away
                # This ensures short demo routes even for unknown places
                hash_val = hash(destination_name)
                lat_off = (hash_val % 100) / 3000.0 + 0.005 # Ensure some distance
                lon_off = ((hash_val >> 2) % 100) / 3000.0 + 0.005
                end = [start[0] + lon_off, start[1] + lat_off]
        
        # Determine Midpoints for "Safe" vs "Direct"
        # Direct (Red) is just a straight line with some noise
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        
        risky_path = [
            start,
            [mid_x + 0.002, mid_y - 0.002], # Dark alley deviation
            end
        ]
        
        # Safe Path (Green) - Optimized with more waypoints
        safe_path = [
            start,
            [mid_x * 0.9 + end[0] * 0.1, start[1]], # Move horizontally first
            [mid_x, mid_y + 0.005], # Detour to safe zone
            [end[0], mid_y * 0.9 + start[1] * 0.1], # Align vertically
            end
        ]

        # Risky Path (Red) - Direct cutting through blocks
        risky_path = [
            start,
            [mid_x + 0.002, mid_y - 0.002], # Dark alley deviation
            [mid_x - 0.001, mid_y - 0.001], # Unlit park
            end
        ]
        
        return risky_path, safe_path


