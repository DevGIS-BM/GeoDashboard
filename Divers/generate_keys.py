import pickle
from pathlib import Path
import streamlit_authenticator as stauth

# Plain text passwords
passwords = ['abcde', 'abcdef']

# Generate hashed passwords
hashed_passwords = stauth.Hasher(passwords).generate()

# Save hashed passwords to a pickle file
file_path = Path(__file__).parent / 'hashed_pwd.pkl'
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
