import bcrypt
import pickle
from pathlib import Path

# Example user credentials
usernames = ["yonas", "teferi"]
passwords = ["yon", "tef"]

# Hash the passwords
hashed_passwords = [bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) for password in passwords]

# Print the hashed passwords to verify
print("Hashed Passwords:")
for hp in hashed_passwords:
    print(hp)

# Save the hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
