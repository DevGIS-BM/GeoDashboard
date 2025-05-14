import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# --- Title ---
st.title("🗺️ Carte interactive - Commune de Talilit")

# --- Load GeoDataFrames from session ---
commune = st.session_state.get("talilit")
# education = st.session_state.get("ecole_talilit")
education = st.session_state.get("educ_data")

# Check data availability
if commune is None or education is None:
    st.error("Les couches 'talilit' ou 'ecole_talilit' ne sont pas chargées dans st.session_state.")
else:
    # Ensure CRS is in lat/lon
    if commune.crs != "EPSG:4326":
        commune = commune.to_crs(epsg=4326)
    if education.crs != "EPSG:4326":
        education = education.to_crs(epsg=4326)

    # --- Calculate map center using centroid of commune geometry
    center = commune.geometry.centroid.iloc[0].coords[0][::-1]  # (lat, lon)

    # --- Create folium map ---
    m = folium.Map(location=center, zoom_start=12, tiles="OpenStreetMap")

    # --- Add commune polygon layer with popup ---
    folium.GeoJson(
        commune,
        name="Commune Talilit",
        popup=folium.GeoJsonPopup(
            fields=["region_fr", "province_f", "milieu", "Population", "Sante", "Education"],
            aliases=["Région", "Province", "Milieu", "Population", "Santé", "Éducation"],
            localize=True,
            labels=True,
            style="background-color: yellow;"
        ),
        style_function=lambda x: {
            "fillColor": "#add8e6",
            "color": "blue",
            "weight": 2,
            "fillOpacity": 0.4
        },
    ).add_to(m)

    # --- Add education markers with marker cluster ---
    marker_cluster = MarkerCluster(name="Écoles").add_to(m)

    for _, row in education.iterrows():
        if row.geometry.geom_type == "Point":
            lat, lon = row.geometry.y, row.geometry.x
            popup_html = f"<b>Établissement :</b> {row.get('etablissem', 'Non défini')}"
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=250),
                icon=folium.DivIcon(html="""
                    <div style="background-color: yellow; color: black; border-radius: 50%; width: 30px; height: 30px;
                                display: flex; justify-content: center; align-items: center; border: 2px solid white;">
                        🎓
                    </div>
                """)
            ).add_to(marker_cluster)

    # --- Add layer control ---
    folium.LayerControl().add_to(m)

    # --- Display the map ---
    st_folium(m, width=900, height=600)
