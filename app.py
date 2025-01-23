import yaml
import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path
import geopandas as gpd



st.set_page_config(layout="wide")
# Initialize Shared Data
@st.cache_data
def load_data(file_path):
    gdf = gpd.read_file(file_path)
    return gdf

if "communes_data" not in st.session_state:
    communes_path = r"data/communes.shp"
    st.session_state["communes_data"] = load_data(communes_path)
    
if "douars" not in st.session_state:
    douars_path = r"data/douars_Rif.shp"
    st.session_state["douars"] = load_data(douars_path)

if "educ_data" not in st.session_state:
    educ_path = r"data/education_province.shp"
    st.session_state["educ_data"] = load_data(educ_path)

if "health_data" not in st.session_state:
    health_path = r"data/CRS_Province.shp"
    st.session_state["health_data"] = load_data(health_path)

if "roads" not in st.session_state:
    roads_path = r"data/routes.shp"
    st.session_state["roads"] = load_data(roads_path)

# Configuration for the YAML credentials file
user_db_path = "data/credentials.yaml"

# Load user data from YAML file
if Path(user_db_path).exists():
    with open(user_db_path, "r") as file:
        user_data = yaml.safe_load(file)
else:
    st.error(f"Credentials file not found: {user_db_path}")
    st.stop()

# Validate YAML structure
if (
    "credentials" not in user_data or 
    "usernames" not in user_data["credentials"] or 
    not isinstance(user_data["credentials"]["usernames"], dict)
):
    st.error("Invalid user data structure in users.yaml.")
    st.stop()

# Extract user credentials
credentials = user_data["credentials"]["usernames"]
usernames = list(credentials.keys())
names = [credentials[username]["name"] for username in usernames]
hashed_passwords = [credentials[username]["password"] for username in usernames]

# Authentication Parameters
cookie_expiry_days = 30
cookie_key = "abcd123"
cookie_name = "streamlit_auth"

# Initialize the authenticator
authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    cookie_name,
    cookie_key,
    cookie_expiry_days,
)

# Login Form
name, authentication_status, username = authenticator.login("Login", "main")

# Load role from the user data
role = credentials.get(username, {}).get("role") if authentication_status else None

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome, {name}!")

    # Sidebar Navigation
    h = st.Page("app_pages/home_pg.py", title="🖥️ Home")
    p1 = st.Page("app_pages/chart_pg.py", title="📉 Graphes")
    p2 = st.Page("app_pages/map_pg.py", title="🗺️ Carte interactive")
    sr = st.Page("app_pages/search_pg.py", title="🔍 Recherche")
    stg = st.Page("app_pages/settings_pg.py", title="⚙️ Paramètres")
    
    # Add admin and superadmin tools
    update_data_page = None
    manage_users_page = None
    if role in {"admin", "superadmin"}:
        update_data_page = st.Page("app_pages/update_data.py", title="📝 Actualiser les données")
    if role == "superadmin":
        manage_users_page = st.Page("app_pages/manage_users.py", title="👤 Gestion des utilisateurs")
    
    # Sidebar Navigation
    pages = {
        "Home": [h],
        "Dashboard": [p1, p2],
        "Tools": [sr, stg],
    }
    if update_data_page:
        pages["Admin Tools"] = [update_data_page]
    if manage_users_page:
        if "Admin Tools" in pages:
            pages["Admin Tools"].append(manage_users_page)
        else:
            pages["Admin Tools"] = [manage_users_page]
    
    pg = st.navigation(pages)
    pg.run()

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
