import pickle
import streamlit_authenticator as stauth

# Sample user data for adding
names = ["Ahmed", "Laila","Hassan"]
usernames = ["ahmed1", "laila1","hassan1"]
emails = ["ahmed@geo.com", "laila@geo.com","hassan@geo.com"]
roles = ["admin","viewer","editor"]
passwords = ["abc12", "def23","abcdef"]  # Plaintext passwords

# Hash the passwords
hashed_passwords = stauth.Hasher(passwords).generate()


# Prepare the credentials structure
data = {}


# Add users to the credentials structure
for i, username in enumerate(usernames):
    data[username] = {
        "name": names[i],
        "email": emails[i],
        "role": roles[i],
        "password": hashed_passwords[i]
    }

# Path to save the credentials
user_db_path = "data/users.pkl"

# Save the credentials to the pickle file
with open(user_db_path, "wb") as file:
    pickle.dump(data, file)

print("Credentials saved successfully!")
