import streamlit as st
import pydeck as pdk

def render_map(sim_module, safe_path, risky_path, heatmap_data, user_pos=[77.5946, 12.9716]):
    st.markdown("### 📍 Live Safety Navigation")
    
    # Safe Path (Green)
    layer_safe = pdk.Layer(
        "PathLayer",
        data=[{"path": safe_path, "color": [76, 175, 80]}],
        get_path="path",
        get_color="color",
        width_scale=20,
        width_min_pixels=5,
        pickable=True
    )
    
    # Risky Path (Red)
    layer_risk = pdk.Layer(
        "PathLayer",
        data=[{"path": risky_path, "color": [255, 82, 82]}],
        get_path="path",
        get_color="color",
        width_scale=20,
        width_min_pixels=5,
        pickable=True
    )
    
    # Heatmap
    layer_heat = pdk.Layer(
        "HeatmapLayer",
        heatmap_data,
        get_position=["lon", "lat"],
        get_weight="intensity",
        radius_pixels=60,
    )
    
    # User Position Marker
    layer_user = pdk.Layer(
        "ScatterplotLayer",
        data=[{"position": user_pos, "color": [0, 128, 255], "radius": 50}],
        get_position="position",
        get_color="color",
        get_radius="radius",
        pickable=True,
    )

    # Calculate View State (Midpoint of Path)
    if safe_path and len(safe_path) > 0:
        # safe_path is list of [lon, lat]
        lats = [p[1] for p in safe_path]
        lons = [p[0] for p in safe_path]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
        zoom_level = 13 # A bit wider to see the route
    else:
        center_lat = user_pos[1]
        center_lon = user_pos[0]
        zoom_level = 14

    view_state = pdk.ViewState(
        latitude=center_lat, 
        longitude=center_lon, 
        zoom=zoom_level, 
        pitch=50
    )
    
    st.markdown("### 🗺️ Sentinel Safety Map")
    st.pydeck_chart(pdk.Deck(
        layers=[layer_heat, layer_safe, layer_risk, layer_user], 
        initial_view_state=view_state,
        map_style=pdk.map_styles.CARTO_DARK
    ))

def render_google_maps_embed(source, destination):
    """
    Renders an embedded Google Map for direction visualization.
    Note: 'output=embed' is invalid for modern Directions API without API Key, 
    so we use the 'search' or basic 'place' embed, or a workaround.
    Ref: https://www.google.com/maps?q=...&output=embed
    """
    st.markdown("### 🚦 Google Maps Traffic & Route Preview")
    
    # Clean inputs
    src = source.replace(" ", "+")
    dst = destination.replace(" ", "+")
    
    # Try the older embed format which sometimes works for simple queries
    # or just show the destination area
    embed_url = f"https://www.google.com/maps?saddr={src}&daddr={dst}&output=embed"
    
    st.components.v1.iframe(embed_url, height=500, scrolling=True)
    
    # Legend/Route Info
    c1, c2 = st.columns(2)
    with c1:
        st.success("**✅ Recommended Route**\n\nETA: 12 min • Well Lit")
    with c2:
        st.error("**❌ Avoid Area**\n\nHigh Risk • Reports of dark spots")
