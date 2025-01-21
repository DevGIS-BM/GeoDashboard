import streamlit as st
import random
import string
import streamlit_authenticator as stauth
import smtplib
from email.mime.text import MIMEText
from pathlib import Path
import pickle

# Function to generate a random password
def generate_password(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st

# Function to send email with attachment (for password sending)
def send_email(user_email, username, password):
    try:
        # Email configuration
        sender_email = "dev.bousta@gmail.com"  # Replace with your email
        sender_password = "ryre ldtg bajx zpru"  # Use an app-specific password for better security
        subject = "Your Account Credentials"



        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = user_email
        msg['Subject'] = subject

        # Create the email body
        body = f"Hello {username},\n\nYour account has been created with the following credentials:\nUsername: {username}\nPassword: {password}"
        msg.attach(MIMEText(body, 'plain'))

        # Set up the SMTP server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use the appropriate SMTP server for your email provider
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)  # Log in using the sender's email and app password
        server.sendmail(sender_email, user_email, msg.as_string())  # Send the email
        server.quit()  # Close the connection

        st.success(f"Account details for {username} have been sent to {user_email}.")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Load user data (this will be the new user database using pickle)
user_db_path = "data/users.pkl"
if Path(user_db_path).exists():
    with open(user_db_path, "rb") as file:
        user_data = pickle.load(file)
else:
    user_data = {}

# Superadmin user interface
st.title("Manage Users")

# Input fields for new user creation
st.subheader("Create New User")
new_name = st.text_input("Name")
new_username = st.text_input("Username")
new_email = st.text_input("Email")
new_role = st.selectbox("Role", ["user", "admin"])

if st.button("Create User"):
    # Generate random password
    new_password = generate_password()

    # Hash the password using streamlit_authenticator
    hasher = stauth.Hasher([new_password])
    hashed_password = hasher.generate()[0]

    # Add user to the database
    user_data[new_username] = {
        "name": new_name,
        "email": new_email,
        "role": new_role,
        "password": hashed_password
    }
    
    # Save the updated user data to pickle file
    with open(user_db_path, "wb") as file:
        pickle.dump(user_data, file)

    # Send the password to the user via email
    send_email(new_email, new_username, new_password)

    st.success(f"User {new_username} created successfully. The password has been sent to their email.")

# User management options
st.subheader("Manage Existing Users")
user_to_manage = st.selectbox("Select a user to manage", list(user_data.keys()))

if user_to_manage:
    user_details = user_data[user_to_manage]
    st.write(f"Name: {user_details['name']}")
    st.write(f"Username: {user_details['username']}")
    st.write(f"Email: {user_details['email']}")
    st.write(f"Role: {user_details['role']}")

    # Role change option
    new_role = st.selectbox("Change role", ["user", "admin","superadmin"], index=["user", "admin","superadmin"].index(user_details["role"]))
    if st.button("Change Role"):
        user_data[user_to_manage]["role"] = new_role
        # Save the updated user data to pickle file
        with open(user_db_path, "wb") as file:
            pickle.dump(user_data, file)
        st.success(f"User {user_to_manage}'s role has been updated to {new_role}.")

    # Delete user option
    if st.button("Delete User"):
        del user_data[user_to_manage]
        # Save the updated user data to pickle file
        with open(user_db_path, "wb") as file:
            pickle.dump(user_data, file)
        st.success(f"User {user_to_manage} has been deleted.")
