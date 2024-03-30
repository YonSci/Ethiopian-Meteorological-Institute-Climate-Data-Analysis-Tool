import bcrypt
import pickle

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def create_and_save_credentials(user_password_list, filename="user_credentials.pkl"):
    credentials = {}

    for username, password in user_password_list:
        hashed_password = hash_password(password)
        credentials[username] = {"hashed_password": hashed_password}

    with open(filename, "wb") as file:
        pickle.dump(credentials, file)

if __name__ == "__main__":
    # List of usernames and passwords
    user_password_list = [
        ("yonas", "yonas1234"),
        ("teferi", "teferi1234"),
        # Add more users as needed
    ]

    # Create and save hashed credentials
    create_and_save_credentials(user_password_list)

