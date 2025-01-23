import pickle
from pathlib import Path
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