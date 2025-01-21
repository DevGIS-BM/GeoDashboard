import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
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

# Authentication Parameters
cookie_expiry_days = 30
cookie_key = 'abcd123'
cookie_name = 'streamlit_auth'

# Load user data from pickle (hashed passwords)
user_db_path = "data/users.pkl"
if Path(user_db_path).exists():
    with open(user_db_path, "rb") as file:
        user_data = pickle.load(file)
        
    # Debugging: Check the structure of user_data
    print(user_data)  # Print the structure of user_data       
else:
    user_data = {}
    print('KO')


# names = [user['name'] for user in user_data.values()]
# usernames = [user['username'] for user in user_data.values()]
# hashed_passwords = [user['password'] for user in user_data.values()]

# Prepare data in the required format
usernames = list(user_data.keys())  # Extracting usernames directly from the dictionary keys
names = [user_data[username]['name'] for username in usernames]  # Extracting names from the user data
hashed_passwords = [user_data[username]['password'] for username in usernames]  # Extracting hashed passwords

# Initialize the authenticator



authenticator = stauth.Authenticate(
    names, 
    usernames, 
    hashed_passwords, 
    cookie_name, 
    cookie_key, 
    cookie_expiry_days
)

# Login Form
name, authentication_status, username = authenticator.login("Login", "main")

# Load role from the user data
role = user_data.get(username, {}).get('role') if authentication_status else None

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome, {name}!")

    # Sidebar Navigation
    # Define Pages
    h = st.Page("app_pages/home_pg.py", title="🖥️ Home")
    p1 = st.Page("app_pages/chart_pg.py", title="📉 Graphes")
    p2 = st.Page("app_pages/map_pg.py", title="🗺️ Carte interactive")
    sr = st.Page("app_pages/search_pg.py", title="🔍 Recherche")
    stg = st.Page("app_pages/settings_pg.py", title="⚙️ Paramètres")
    
    # Only add the "Update Data" page if the user is the admin (Ahmed Hassan)
    update_data_page = None
    manage_users_page = None
    if (role == "admin") or (role == "superadmin"):  
        update_data_page = st.Page("app_pages/update_data.py", title="📝 Actualiser les données")

    if role == "superadmin":  
        manage_users_page = st.Page("app_pages/manage_users.py", title="👤 Gestion des utilisateurs")    
    
    # Sidebar Navigation (only add pages that are not None)
    pages = {
        "Home": [h],
        "Dashboard": [p1, p2],
        "Tools": [sr, stg],
    }

    if update_data_page:
        pages["Admin Tools"] = [update_data_page]  # Add the "Update Data" page under Admin Tools
        
    if manage_users_page:
        if "Admin Tools" in pages:
            pages["Admin Tools"].append(manage_users_page)  # Add the "Manage Users" page if it's already there
        else:
            pages["Admin Tools"] = [manage_users_page]  # If not, create the "Admin Tools" page
    
    pg = st.navigation(pages)
    pg.run()

elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
