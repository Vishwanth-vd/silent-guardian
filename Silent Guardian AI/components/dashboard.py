import streamlit as st
import time
from modules.sentinel import Sentinel

def render_metrics(risk_score, esi, crowd, mode, sentinel_data=None):
    """
    Renders the top KPI row.
    """
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    # Custom CSS Card Helper
    def card(title, value, status, color_class):
        return f"""
        <div class="metric-card {color_class}">
            <div style="font-size: 0.9rem; color: #888;">{title}</div>
            <div style="font-size: 1.8rem; font-weight: bold; color: #fff;">{value}</div>
            <div style="font-size: 0.8rem; margin-top: 5px;">{status}</div>
        </div>
        """

    # Dynamic styling based on Risk
    risk_class = "high-risk" if risk_score > 70 else "safe-risk" if risk_score < 40 else "med-risk"
    
    with kpi1:
        st.markdown(card("Risk Score", f"{risk_score}/100", f"{'Critical' if risk_score > 70 else 'Low' if risk_score < 40 else 'Moderate'}", risk_class), unsafe_allow_html=True)
    
    with kpi2:
        st.markdown(card("Emotional Status", esi, "Community Vibe", "neutral-card"), unsafe_allow_html=True)
    
    # If Live Mode, show Sentinel Data
    if sentinel_data:
        with kpi3:
            st.markdown(card("Heart Rate", f"{sentinel_data['heart_rate']} BPM", f"{sentinel_data['stress_level']}% Stress", "live-card"), unsafe_allow_html=True)
        with kpi4:
            st.markdown(card("Ambience", f"{sentinel_data['audio_level']} dB", "Live Audio Monitor", "live-card"), unsafe_allow_html=True)
    else:
        with kpi3:
            st.markdown(card("Crowd Density", crowd, "Est. People/sqm", "neutral-card"), unsafe_allow_html=True)
        with kpi4:
            st.markdown(card("Active Mode", mode.split()[0], "Protection Level", "neutral-card"), unsafe_allow_html=True)
        
    return kpi1, kpi2, kpi3, kpi4

def render_alert(risk_score):
    if risk_score > 80:
        st.error("⚠️ CRITICAL RISK DETECTED IN THIS ZONE")
