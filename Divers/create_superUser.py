import pickle
import streamlit_authenticator as stauth
from pathlib import Path

# Sample user data for adding
name = "Super admin"
username = "super1"
email = "new_user@example.com"
role = "superadmin"
password = "new123"  # Plaintext password

# Hash the password
hashed_password = stauth.Hasher([password]).generate()[0]

# Load existing user data
user_db_path = "data/users.pkl"
if Path(user_db_path).exists():
    with open(user_db_path, "rb") as file:
        user_data = pickle.load(file)
else:
    user_data = {}

# Add new user
user_data[username] = {
    "name": name,
    "email": email,
    "role": role,
    "password": hashed_password
}

# Save the updated user data
with open(user_db_path, "wb") as file:
    pickle.dump(user_data, file)

print("User added successfully!")
