import bcrypt
import yaml
from pathlib import Path

# Define initial user data
initial_users = {
    "credentials": {
        "usernames": {
            "admin": {
                "name": "Admin User",
                "email": "admin@example.com",
                "role": "superadmin",
                "password": None  # Placeholder for hashed password
            }
        }
    }
}

# Path to the credentials file
credentials_path = Path("data/credentials.yaml")
credentials_path.parent.mkdir(exist_ok=True, parents=True)

# Prompt for admin password
password = input("Enter the admin password: ").strip()
hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Update the initial user data with the hashed password
initial_users["credentials"]["usernames"]["admin"]["password"] = hashed_password

# Save credentials to a YAML file
with open(credentials_path, "w") as file:
    yaml.dump(initial_users, file)

print(f"Credentials saved to {credentials_path}")
