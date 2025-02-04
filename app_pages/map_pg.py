import streamlit as st
import geopandas as gpd
import folium
import branca
from streamlit_folium import st_folium
from folium.plugins import Fullscreen,MarkerCluster
import plotly.express as px


# Title
st.title("Carte interactive et Analyse des Communes")

# Paths of shapefiles
communes = st.session_state["communes_data"]

education=st.session_state["educ_data"]
health= st.session_state["health_data"]
roads=st.session_state["roads"]
douars=st.session_state["douars"]

# @st.cache_data
def create_map(selected_theme, selected_basemap):


    # Map initialization using folium
    m = folium.Map(location=[35, -3.5], tiles=selected_basemap, zoom_start=9)

    # Create colormap using branca for communes
    colormap = branca.colormap.LinearColormap(
        vmin=communes[selected_theme].quantile(0.0),
        vmax=communes[selected_theme].quantile(1),
        colors=["red", "orange", "lightblue", "green", "darkgreen"],
        caption=selected_theme +" par communes",
    )

    # Popup for communes
    popup = folium.GeoJsonPopup(
        fields=["commune_fr", "Population"],
        aliases=["commune", "Population"],
        localize=True,
        labels=True,
        style="background-color: yellow;",
    )

    # Tooltip for communes
    tooltip = folium.GeoJsonTooltip(
        fields=["commune_fr", "Menages"],
        aliases=["commune_fr", "Menages"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )

    # Add communes to the map
    folium.GeoJson(
        communes,
        # style_function=lambda feature: style_function(feature, selected_theme, colormap),
        style_function=lambda x: {
            "fillColor": colormap(x["properties"][selected_theme])
            if x["properties"][selected_theme] is not None
            else "transparent",
            "color": "black",
            "fillOpacity": 0.4,
        },
        tooltip=tooltip,
        popup=popup,
        name="Communes"
    ).add_to(m)

    # Popup for douar
    popup1 = folium.GeoJsonPopup(
        fields=["nom_fr", "type", "milieu", "population", "menage"],
        aliases=["Nom: ", "Type: ", "Milieu: ", "Population: ", "Nombre de ménage: "],
        localize=True,
        labels=True,
        style="background-color: blue;",
    )

    # Add douar to the map
    folium.GeoJson(
        douars,
        name="Douars",
        zoom_on_click=True,
        marker=folium.CircleMarker(color='black', radius=3, fill= True, fill_color='white'),
        tooltip=folium.GeoJsonTooltip(fields=["nom_fr", "type", "milieu"], aliases=["Nom: ", "Type: ", "Milieu: "]),
        popup=popup1,
    ).add_to(m)
    


    # # # Roads
    # def style_function(feature):
    #     return {
    #         "color": "navy",  # Line color
    #         "weight": 2,      # Line thickness
    #         "opacity": 0.8    # Line transparency
    #     }

    # folium.GeoJson(
    #     roads,  # GeoDataFrame
    #     style_function=style_function,  # Apply styling function
    #     name="Routes"
    # ).add_to(m)

    # Education layer
    marker_cluster = MarkerCluster(name="Etablissement scolaires")
    for idx, row in education.iterrows():
        popup_content = f"<b>Etablissement:</b> {row['etablissem']}"
        #icon = folium.Icon(icon="book-open", prefix="fa", color="blue")  # Use FontAwesome school icon
        popup = folium.Popup(popup_content, max_width=300)
        # Custom HTML for a round icon
        round_icon = folium.DivIcon(html=f"""
            <div style="
                background-color: yellow;
                color: black;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                display: flex;
                justify-content: center;
                align-items: center;
                border: 2px solid white;
            ">
                🎓
            </div>
        """)    
            
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=popup,
            icon=round_icon
        ).add_to(marker_cluster)

    marker_cluster.add_to(m)
    
    
    # Santé layer
    marker_cluster2 = MarkerCluster(name="Etablissements sanitaires")
    for idx, row in health.iterrows():
        popup_content = f"<b>Etablissement:</b> {row['etabl_fr']}"
        # icon = folium.Icon(icon="square-h", prefix="fa", color="green")  # Use FontAwesome school icon
        popup = folium.Popup(popup_content, max_width=300)
        
        # Custom HTML for a round icon
        round_icon2 = folium.DivIcon(html=f"""
            <div style="
                background-color: grey;
                color: black;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                display: flex;
                justify-content: center;
                align-items: center;
                border: 2px solid white;
            ">
                🩺
            </div>
        """)          
              
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=popup,
            icon=round_icon2
        ).add_to(marker_cluster2)

    marker_cluster2.add_to(m)

 

    # Adding plugins to the map
    Fullscreen().add_to(m)
    colormap.add_to(m)
       # Add LayerControl
    folium.LayerControl(position="bottomright").add_to(m)

    # Display the map
    # st_folium(m, width=900, height=500)
    return m

# Initialize session state to track map inputs
if "show_map" not in st.session_state:
    st.session_state.show_map = False
if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = "Population"
if "selected_basemap" not in st.session_state:
    st.session_state.selected_basemap = "OpenStreetMap"

# --- Two Columns Layout ---
col1, col2 = st.columns([5, 3])
theme_options=('Population','Sante', 'Education', 'AEP', 'Elec', 'Voirier')

# Column 1: Map and Select Boxes
with col1:
    st.subheader("Carte Interactive")

    # Sidebar inputs (but do not update map state until button click)
    # Sidebar inputs (but ensure `selected_theme` is valid)
    # theme_options = tuple(communes.columns)  # Convert to tuple for compatibility
    
    # selected_theme = st.selectbox(
    #     "Thème",
    #     theme_options,
    #     index=theme_options.index(st.session_state.selected_theme)
    #     if "selected_theme" in st.session_state and st.session_state.selected_theme in theme_options
    #     else 0  # Default to the first option if no valid selection is found
    # )
    
    
    selected_theme = st.selectbox("Thème", theme_options, index=theme_options.index(st.session_state.selected_theme))
    selected_basemap = st.selectbox("Base map", ("OpenStreetMap", "CartoDB positron"), index=("OpenStreetMap",  "CartoDB positron").index(st.session_state.selected_basemap))

    # Show map button
    if st.button("Update Map", type="primary"):
        st.session_state.show_map = True
        st.session_state.selected_theme = selected_theme
        st.session_state.selected_basemap = selected_basemap
        # st.session_state.mapBtn_clicked = True

    # Display the map only if the button was clicked
    if st.session_state.show_map:
        # Generate the map
        map_obj = create_map(st.session_state.selected_theme,st.session_state.selected_basemap)
        st_folium(map_obj, width=900, height=500)


# Column 2: Chart and Select Boxes
with col2:
    st.subheader("Analyse des Communes")
    # communes = get_communes()

    # Chart options
    
# Add button to trigger chart display

    # chart_column = st.selectbox("Select a column for charting", communes.columns)
    chart_column =  st.session_state.selected_theme
    chart_type = st.selectbox("Select chart type", ["Bar", "Pie", "Scatter"])
    # Generate chart based on user input
    if chart_type == "Bar":
        fig = px.bar(communes, x="commune_fr", y=chart_column, title=f"Bar Chart of {chart_column}", labels={"commune_fr": "Commune", chart_column: "Value"})
    elif chart_type == "Pie":
        fig = px.pie(communes, names="commune_fr", values=chart_column, title=f"Pie Chart of {chart_column}")
    elif chart_type == "Scatter":
        fig = px.scatter(communes, x="commune_fr", y=chart_column, title=f"Scatter Plot of {chart_column}", labels={"commune_fr": "Commune", chart_column: "Value"})

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
