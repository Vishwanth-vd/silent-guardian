from utils import LIGHTING, CROWD

class RiskEngine:
    def __init__(self):
        # Base weights
        self.lighting_weights = {
            "Bright Daylight": 0, "Dusk/Dawn": 20, "Street Lights (Good)": 15,
            "Dim Light": 50, "Pitch Dark": 90
        }
        self.crowd_weights = {
            "Empty": 40, "Sparse": 30, "Moderate": 10,  # "Eyes on the street" theory: moderate is safest
            "Dense": 40, "Stampede Risk": 95
        }
        # Time weights: Risk increases late night
        # Defined as function of hour

    def calculate_time_risk(self, hour):
        if 6 <= hour <= 18: return 0    # Day
        if 18 < hour <= 22: return 20   # Evening
        return 50                       # Late Night (23-5)

    def calculate_risk_score(self, params, mode):
        """
        Computes Risk Score (0-100) and returns (Score, ESI_Label, Factors).
        params: dict with location, lighting, crowd, time_hour, escape_routes
        mode: Guardian Mode (Normal, Women, Elderly)
        """
        score = 0
        factors = []

        # 1. Base Environmental Risk
        l_risk = self.lighting_weights.get(params['lighting'], 0)
        score += l_risk
        if l_risk > 30: factors.append(f"Poor Lighting ({params['lighting']})")

        c_risk = self.crowd_weights.get(params['crowd'], 0)
        score += c_risk
        if c_risk > 40: factors.append(f"High Crowd Risk ({params['crowd']})")

        t_risk = self.calculate_time_risk(params['time_hour'])
        score += t_risk
        if t_risk > 0: factors.append(f"Time of Day ({params['time_hour']}:00)")

        if params['escape_routes'] == 0:
            score += 30
            factors.append("No Escape Routes Available")
        
        # 2. Guardian Mode Adjustments (Vulnerability Amplification)
        if mode == "Women Safety Mode":
            # Amplified risk for darkness and isolation
            if params['lighting'] in ["Dim Light", "Pitch Dark"]:
                score += 20
                factors.append("High Vulnerability Zone (Women Safety)")
            if params['crowd'] == "Empty":
                score += 25
                factors.append("Isolation Risk (Women Safety)")

        elif mode == "Elderly Safety Mode":
            # Amplified risk for crowds and obstacles
            if params['crowd'] in ["Dense", "Stampede Risk"]:
                score += 30
                factors.append("Mobility Risk (Elderly)")
            if params['escape_routes'] < 2:
                score += 20
                factors.append("Evacuation Difficulty (Elderly)")

        # Cap score at 100
        score = min(100, score)

        # 3. Determine Emotional Safety Index (ESI)
        if score < 30:
            esi = "Comfortable"
        elif score < 70:
            esi = "Uneasy"
        else:
            esi = "Unsafe"

        return score, esi, factors
