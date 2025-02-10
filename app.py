import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import geopandas as gpd

# Set page configuration
st.set_page_config(layout="wide")



# Initialize session state for authentication
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None
if "name" not in st.session_state:
    st.session_state["name"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None

# Load data function
@st.cache_data
def load_data(file_path):
    gdf = gpd.read_file(file_path)
    return gdf

# Lostad and cache data in session state
if "communes_data" not in st.session_state:
    communes_path = r"data/Communes.geojson"
    st.session_state["communes_data"] = load_data(communes_path)
    
if "douars" not in st.session_state:
    douars_path = r"data/douars.geojson"
    st.session_state["douars"] = load_data(douars_path)

if "educ_data" not in st.session_state:
    educ_path = r"data/education_province.geojson"
    st.session_state["educ_data"] = load_data(educ_path)

if "health_data" not in st.session_state:
    health_path = r"data/CRS_Province.geojson"
    st.session_state["health_data"] = load_data(health_path)

if "roads" not in st.session_state:
    roads_path = r"data/routes.geojson"
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
else:
    user_data = {}

# Extract usernames, names, and hashed passwords
usernames = list(user_data.keys()) 
names = [user_data[username]['name'] for username in usernames] 
hashed_passwords = [user_data[username]['password'] for username in usernames]

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

# Update session state based on authentication status
if authentication_status:
    st.session_state["authentication_status"] = True
    st.session_state["name"] = name
    st.session_state["username"] = username
elif authentication_status is False:
    st.session_state["authentication_status"] = False
    st.session_state["name"] = None
    st.session_state["username"] = None
elif authentication_status is None:
    st.session_state["authentication_status"] = None
    st.session_state["name"] = None
    st.session_state["username"] = None

# Ensure role loading only when user is authenticated
role = user_data.get(username, {}).get('role') if st.session_state["authentication_status"] else None

# Display app or login page based on authentication status
if st.session_state["authentication_status"]:
    try:
        # Wrap the sidebar inside the authentication condition
        with st.sidebar:
            st.title(f"Welcome, {st.session_state['name']}!")
            if authenticator.logout("Logout", "sidebar"):
                # Reset session state on logout
                st.session_state["authentication_status"] = False
                st.session_state["name"] = None
                st.session_state["username"] = None
                # st.experimental_rerun()
                st.rerun()  # Force rerun to display the login page
                

            # if authenticator.logout("Logout", "sidebar"):
            #     # # Clear session state
            #     for key in list(st.session_state.keys()):
            #         del st.session_state[key]
                    
                # Redirect to the main page (e.g., "home.py")
                # st.switch_page("app_pages/home_pg.py")  # Replace with your actual login page path
                # Use JavaScript to redirect
                # st.markdown('<meta http-equiv="refresh" content="0;URL=https://www.google.com/">', unsafe_allow_html=True)


            # if st.button('Logout'):
            #     authenticator.logout(location='unrendered')
            #     st.experimental_rerun()

                
                
        # Sidebar Navigation
        h = st.Page("app_pages/home_pg.py", title="🖥️ Home")
        p1 = st.Page("app_pages/chart_pg.py", title="📉 Graphes")
        p2 = st.Page("app_pages/map_pg.py", title="🗺️ Carte interactive")
        sr = st.Page("app_pages/search_pg.py", title="🔍 Recherche")
        stg = st.Page("app_pages/settings_pg.py", title="⚙️ Paramètres")

        # Only add the "Update Data" page if the user is the admin or editor
        update_data_page = None
        manage_users_page = None
        if (role == "admin") or (role == "editor"):  
            update_data_page = st.Page("app_pages/update_data.py", title="📝 Actualiser les données")

        if role == "admin":  
            manage_users_page = st.Page("app_pages/manage_users.py", title="👤 Gestion des utilisateurs")    

        # Sidebar Navigation (only add pages that are not None)
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
        
        # Run the navigation
        pg = st.navigation(pages)
        pg.run()
    except KeyError:
        pass  # ignore it
    except Exception as err:
        st.error(f'Unexpected exception {err}')
        raise Exception(err)
elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")
