import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["Yonas Mersha", "Asaminew Teshome", "Teferi Demissie", "Melesse Lemma", "Bezuneh Sego"]
usernames = ["yonas", "asaminew", "teferi", "melesse", "bezuneh" ]
passwords = ["yonas123", "asaminew123", "teferi123", "melesse123", "bezuneh123"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
