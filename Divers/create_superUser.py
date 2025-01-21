import pickle
import streamlit_authenticator as stauth
from pathlib import Path

# Sample user data for adding
name = ["Super admin","user1"]
username = ["super1","user1"]
email = ["supe1r@example.com","user1@example.com"]
role = ["superadmin","user"]
password = ["abc123","123abc"] # Plaintext password

# Hash the password
hashed_password = stauth.Hasher(password).generate()

# Load existing user data
user_db_path = "data/users.pkl"
if Path(user_db_path).exists():
    with open(user_db_path, "rb") as file:
        user_data = pickle.load(file)
else:
    user_data = {}

# Add new user
for user in username:
    i=username.index(user)
    user_data[user] = {
        "name": name[i],
        "email": email[i],
        "role": role[i],
        "password": hashed_password[i]
    }

# Save the updated user data
with open(user_db_path, "wb") as file:
    pickle.dump(user_data, file)

print("User added successfully!")
