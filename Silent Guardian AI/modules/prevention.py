class GuardianAI:
    def suggest_actions(self, risk_score, factors, mode):
        """Generates preventive suggestions based on risk factors."""
        suggestions = []
        
        # General advice based on score
        if risk_score < 30:
            suggestions.append("✅ Environment seems safe. Stay aware of your surroundings.")
        elif risk_score < 70:
            suggestions.append("⚠️ Caution advised. Share your live location with a trusted contact.")
        else:
            suggestions.append("🚨 HIGH RISK DETECTED. Consider changing route or waiting for a group.")
            suggestions.append("📞 Keep emergency SOS ready.")

        # Specific advice based on factors
        for factor in factors:
            if "Lighting" in factor:
                suggestions.append("💡 Use a flashlight or stick to main roads.")
            if "Crowd" in factor:
                if "Stampede" in factor:
                    suggestions.append("🏃 Move diagonally to the crowd flow to exit.")
                elif "Empty" in factor:
                    suggestions.append("👀 Avoid headphones. Stay alert.")
            if "Time" in factor:
                suggestions.append("🕒 Try to travel via monitored zones or ride-share.")

        # Mode specific advice
        if mode == "Women Safety Mode" and risk_score > 40:
             suggestions.append("🛡️ 'She-Team' patrol areas are nearby (Simulated).")
        elif mode == "Elderly Safety Mode":
             suggestions.append("♿ Stick to pavement with railings if available.")

        return suggestions[:4] # Return top 4 unique suggestions

    def get_crisis_alert(self, action):
        """Returns immediate alert text for What-If scenarios."""
        alerts = {
            "Power Failure": "CRITICAL: Visibility dropped. Move to open ground.",
            "Crowd Surge": "DANGER: High probability of crush. Protect chest area.",
            "Road Block": "WARNING: Route compromised. Find nearest landmark.",
            "Medical Emergency": "ALERT: Ambulance access probability is Low in this density."
        }
        return alerts.get(action, "Analyzing Crisis Impact...")

    def get_chat_response(self, user_input, risk_score):
        """Simple rule-based chatbot for the Guardian Companion."""
        user_input = user_input.lower()
        
        if "safe" in user_input:
            if risk_score < 40:
                return "Based on current data, this location appears safe. However, always stay alert."
            else:
                return f"Caution! Current risk score is {risk_score}. I recommend staying in well-lit areas."
        
        elif "route" in user_input or "path" in user_input:
            return "I have analyzed the map. A safer route (marked in Green) is available, though it may take 5 minutes longer."
        
        elif "hotel" in user_input or "hospital" in user_input:
            return "Simulated: There is a safe zone/hospital 1.2km away. Follow the green route."
            
        elif "help" in user_input or "sos" in user_input:
            return "🚨 SOS Initiated! Sending your location to emergency contacts..."
            
        else:
            return "I am your Silent Guardian. I can help you with safety assessments, route planning, and emergency alerts."

