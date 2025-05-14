
import streamlit as st
import pandas as pd
from datetime import datetime


# Load your DataFrame (replace with your actual source)
df = st.session_state["communes_data"]


# Function to get max/min values along with commune name
def get_max_value(metric):
    row = df.loc[df[metric].idxmax()]
    return f"🔼 {row[metric]} ({row['commune_fr']})"  # Adjust "commune_fr" column name as per dataset

def get_min_value(metric):
    row = df.loc[df[metric].idxmin()]
    return f"🔻 {row[metric]} ({row['commune_fr']})"



# Metrics to display
metrics = ['Population', 'Sante', 'Education', 'AEP', 'Elec', 'Voirier']
max_values = {metric: get_max_value(metric) for metric in metrics}
min_values = {metric: get_min_value(metric) for metric in metrics}

# Calculate category percentages
milieu_counts = df['milieu'].value_counts(normalize=True) * 100
rural_percentage = round(milieu_counts.get("Rural", 0), 2)
urban_percentage = round(milieu_counts.get("Urbain", 0), 2)


# Define function for small metric labels & values
def small_max_metric(column, label, value):
    column.markdown(f"""
        <div >
            <p style='font-size: 14px; margin-bottom: 2px;'>{label}</p>
            <p style='font-size: 16px; font-weight: bold; color: #2912ed;'>{value}</p>
        </div>
    """, unsafe_allow_html=True)

def small_min_metric(column, label, value):
    column.markdown(f"""
        <div >
            <p style='font-size: 14px; margin-bottom: 2px;'>{label}</p>
            <p style='font-size: 16px; font-weight: bold; color: #FF5733;'>{value}</p>
        </div>
    """, unsafe_allow_html=True)    
# Get current date and time
current_datetime = datetime.now().strftime("%A, %B %d, %Y %H:%M")


# 📅 **Date and Time Section**
st.markdown(f"<p class='title'>📅 {current_datetime}</p>", unsafe_allow_html=True)

# 📈 **Global Maximum Metrics**
st.markdown("<h3 class='title'>📈 Global Maximum Metrics</h3>", unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns(3)
    # col1.metric("Max Population", max_values['Population'])
    # col2.metric("Max Sante", max_values['Sante'])
    # col3.metric("Max Education", max_values['Education'])
    
    small_max_metric(col1, "Max Population", max_values['Population'])
    small_max_metric(col2, "Max Sante", max_values['Sante'])
    small_max_metric(col3, "Max Education", max_values['Education'])  
        
    col4, col5, col6 = st.columns(3)
    # col4.metric("Max AEP", max_values['AEP'])
    # col5.metric("Max Elec", max_values['Elec'])
    # col6.metric("Max Voirier", max_values['Voirier'])

    small_max_metric(col4, "Max AEP", max_values['AEP'])
    small_max_metric(col5, "Max Elec", max_values['Elec'])
    small_max_metric(col6, "Max Voirier", max_values['Voirier'])
    


# 📉 **Global Minimum Metrics**
st.markdown("<h3 class='title'>📉 Global Minimum Metrics</h3>", unsafe_allow_html=True)
with st.container():
    col1, col2, col3 = st.columns(3)
    # col1.metric("Min Population", min_values['Population'])
    # col2.metric("Min Sante", min_values['Sante'])
    # col3.metric("Min Education", min_values['Education'])

    small_min_metric(col1,"Min Population", min_values['Population'])
    small_min_metric(col2,"Min Sante", min_values['Sante'])
    small_min_metric(col3,"Min Education", min_values['Education'])
      
    
    
    col4, col5, col6 = st.columns(3)
    # col4.metric("Min AEP", min_values['AEP'])
    # col5.metric("Min Elec", min_values['Elec'])
    # col6.metric("Min Voirier", min_values['Voirier'])
    
    small_min_metric(col4,"Min AEP", min_values['AEP'])
    small_min_metric(col5, "Min Elec", min_values['Elec'])
    small_min_metric(col6, "Min Voirier", min_values['Voirier'])

# 🌆 **Urban vs. Rural Distribution**
st.markdown("<p class='title'>🏡 Urban vs. Rural Distribution</p>", unsafe_allow_html=True)
with st.container():
    col1, col2 = st.columns(2)
    col1.metric("Rural Percentage", f"{rural_percentage}%")
    col2.metric("Urban Percentage", f"{urban_percentage}%")

# 📌 **Additional Insights Section**
with st.expander("📊 View Additional Data Insights"):
    st.write(df.describe())



