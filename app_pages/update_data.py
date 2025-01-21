import streamlit as st
import geopandas as gpd
from datetime import datetime
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

st.title("📝 Update Data")
st.markdown("Use this page to update the communes data.")

# Get username from session state (passed from app.py)
admin_username = st.session_state["username"]

# Get communes data from session state
data = st.session_state["communes_data"]

# Display editable DataFrame
st.write("### Communes Data")
edited_data = st.data_editor(data.drop(columns="geometry", errors="ignore"), num_rows="dynamic")

# Function to log changes
def log_changes(log_entry, log_path):
    # Load existing logs if available
    try:
        log_df = pd.read_csv(log_path)
    except FileNotFoundError:
        log_df = pd.DataFrame(columns=["username", "timestamp", "action", "data_name", "before_n_rows", "after_n_rows"])
    
    # Create a DataFrame for the new log entry
    new_log_df = pd.DataFrame([log_entry])

    # Concatenate the existing logs with the new entry
    log_df = pd.concat([log_df, new_log_df], ignore_index=True)

    # Save the updated log to file
    log_df.to_csv(log_path, index=False)

# Function to send email with log file
def send_email_with_log(log_path, super_admin_email):
    try:
        # Email configuration
        sender_email = "dev.bousta@gmail.com"
        sender_password = "ryre ldtg bajx zpru"  # Use an app password for better security
        subject = "Data Update Log Notification"

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = super_admin_email
        msg['Subject'] = subject
        body = f"Dear Super Admin,\n\nThe data has been updated by {admin_username}.\nPlease find the attached log file for details.\n\nBest regards,\nYour System"
        msg.attach(MIMEText(body, 'plain'))

        # Attach the log file
        attachment = open(log_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={log_path.split('/')[-1]}')
        msg.attach(part)
        attachment.close()

        # Set up the server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use your email provider's SMTP server
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        st.success("Log file emailed to super admin successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Save Changes
if st.button("Save Changes"):
    try:
        # Store the initial row count
        before_n_rows = len(data)

        # Update session state data
        data.update(edited_data)
        st.session_state["communes_data"] = data
        st.session_state["data_updated"] = True  # Mark data as updated

        # Store the updated row count
        after_n_rows = len(data)

        # Save updated data to file
        communes_path = r"data/communes.shp"
        data.to_file(communes_path, driver="ESRI Shapefile")

        # Log the changes
        log_entry = {
            "username": admin_username,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": "Data updated",
            "data_name": "communes.shp",  # Name of the edited data
            "before_n_rows": before_n_rows,
            "after_n_rows": after_n_rows,
        }
        log_path = r"data/update_log.csv"
        log_changes(log_entry, log_path)

        # Email the log file to super admin
        super_admin_email = "bousta.mahfoud@gmail.com"  # Replace with actual super admin email
        send_email_with_log(log_path, super_admin_email)

        st.success(f"Data updated successfully by {admin_username}! Changes will reflect on other pages.")
    except Exception as e:
        st.error(f"Error saving data: {e}")
