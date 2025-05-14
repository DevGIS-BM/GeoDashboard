import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# --- Title ---
st.title("🗺️ Carte interactive - Commune de Driouch")

# --- Load GeoDataFrames from session ---
commune = st.session_state.get("driouch")
mosque = st.session_state.get("mosque_driouch")
quartier= st.session_state.get("quartier_driouch")
reseau=st.session_state.get("res_driouch")

# Check data availability
if commune is None or mosque is None:
    st.error("Les couches 'driouch' ou 'mosque_driouch' ne sont pas chargées dans st.session_state.")
else:
    # Ensure CRS is in lat/lon
    if commune.crs != "EPSG:4326":
        commune = commune.to_crs(epsg=4326)
    if mosque.crs != "EPSG:4326":
        mosque = mosque.to_crs(epsg=4326)

    # --- Calculate map center using centroid of commune geometry
    center = commune.geometry.centroid.iloc[0].coords[0][::-1]  # (lat, lon)

    # --- Create folium map ---
    m = folium.Map(location=center, zoom_start=14, tiles="OpenStreetMap")

    # --- Add commune polygon layer with popup ---
    folium.GeoJson(
        commune,
        name="Commune Driouch",
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
    marker_cluster = MarkerCluster(name="Mosquées").add_to(m)

    for _, row in mosque.iterrows():
        if row.geometry.geom_type == "Point":
            lat, lon = row.geometry.y, row.geometry.x
            popup_html = f"<b>Nom :</b> {row.get('Le_nom_de', 'Non défini')}<br><b>Imam :</b> {row.get('Imam', 'Non défini')}<br><b>Joumaa :</b> {row.get('joumaa', 'Non défini')}<br>"

            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=250),
                icon=folium.DivIcon(html="""
                    <div style="background-color: yellow; color: black; border-radius: 50%; width: 30px; height: 30px;
                                display: flex; justify-content: center; align-items: center; border: 2px solid white;">
                        🕌
                    </div>
                """)
            ).add_to(marker_cluster)
            
    # Add douar to the map
    popup1 = folium.GeoJsonPopup(
        fields=['Province', 'Nom_Quarti', 'Type_Quart', 'Population', 'Accessibil'],
        aliases=["Province", "Nom du quartier", "Type du quartier", "Population", "Accessibilité"],
        localize=True,
        labels=True,
        style="background-color: blue;",
    )
    folium.GeoJson(
        quartier,
        name="Quartier",
        zoom_on_click=True,
        marker=folium.CircleMarker(color='black', radius=3, fill= True, fill_color='white'),
        popup=popup1,
    ).add_to(m)

    # folium.GeoJson(
    #     reseau,
    #     name="Réseau",
    #     zoom_on_click=True,
    #     marker=folium.CircleMarker(color='blue', radius=2, fill= True, fill_color='white'),
    # ).add_to(m)  

    # --- Add layer control ---
    folium.LayerControl().add_to(m)

    # --- Display the map ---
    st_folium(m, width=900, height=600)
