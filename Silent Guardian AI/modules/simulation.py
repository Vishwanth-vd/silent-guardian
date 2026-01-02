import random
import pandas as pd
import numpy as np
from utils import LOCATIONS, LIGHTING, CROWD

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

    def generate_heatmap_data(self, num_points=100):
        """Generates synthetic lat/lon data for risk hotspots in a hypothetical city area."""
        # Base coordinates (somewhere in India, e.g., Bangalore center)
        base_lat = 12.9716
        base_lon = 77.5946
        
        data = []
        for _ in range(num_points):
            lat_off = random.uniform(-0.02, 0.02)
            lon_off = random.uniform(-0.02, 0.02)
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
        Generates a deterministic lat/lon based on the input text hash.
        This ensures 'Office' always maps to the same point, but 'Gym' maps elsewhere.
        """
        if not text_input or text_input == "GPS Location":
            return [77.5946, 12.9716] # Default Center
            
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
        if destination_name in destinations:
            end = destinations[destination_name]
        else:
            # Deterministic simulation for unknown inputs
            end = self._get_simulated_coordinates(destination_name)
        
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

