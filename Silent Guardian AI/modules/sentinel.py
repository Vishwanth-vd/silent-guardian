import random
import time
import math

class Sentinel:
    """
    Sentinel - The Real-Time Guardian Watchdog.
    Simulates live bio-metric and environmental sensors.
    """
    def __init__(self):
        self.start_time = time.time()
        self.user_state = {
            "heart_rate": 75,
            "stress_level": 10,  # 0-100
            "movement_speed": 4.5, # km/h
            "audio_level": 40 # dB
        }
        
    def get_live_metrics(self, risk_score=0):
        """
        Returns a dictionary of simulated real-time data.
        factors influence the metrics (e.g., high risk -> higher heart rate).
        """
        elapsed = time.time() - self.start_time
        
        # Simulate Heart Rate variability
        base_hr = 75
        if risk_score > 60:
            base_hr += (risk_score - 60) * 0.8
            
        # Add some noise/sine wave for realism
        hr_noise = math.sin(elapsed) * 5 + random.uniform(-2, 2)
        current_hr = int(base_hr + hr_noise)
        
        # Simulate Audio Levels (dB)
        # Random spikes for "events"
        base_db = 45 if risk_score < 40 else 65
        db_noise = random.uniform(-5, 15)
        current_db = int(base_db + db_noise)
        
        # Stress level correlates with HR + Risk
        stress = int((current_hr - 60) / 2 + (risk_score / 4))
        stress = max(0, min(100, stress))

        self.user_state.update({
            "heart_rate": current_hr,
            "stress_level": stress,
            "audio_level": current_db,
            "timestamp": time.time()
        })
        
        return self.user_state

    def update_user_position(self, path, progress_index):
        """
        Simulates moving along a path.
        path: List of [lat, lon]
        progress_index: current index in path
        """
        if not path or progress_index >= len(path):
            return path[-1] if path else None, progress_index
            
        current_pos = path[progress_index]
        # Next step
        next_idx = progress_index + 1
        return current_pos, next_idx
