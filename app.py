import os
import streamlit as st
from dotenv import load_dotenv
from auth import Authenticator

load_dotenv()

# emails of users that are allowed to login
allowed_users = os.getenv("ALLOWED_USERS").split(",")

st.title("Streamlit Google Auth")

authenticator = Authenticator(
    allowed_users=allowed_users,
    token_key=os.getenv("TOKEN_KEY"),
    secret_path="credentials.json",
    redirect_uri="http://localhost:8501",
)
authenticator.check_auth()
authenticator.login()

# show content that requires login
if st.session_state["connected"]:
    st.write(f"welcome! {st.session_state['user_info'].get('email')}")
    if st.button("Log out"):
        authenticator.logout()

if not st.session_state["connected"]:
    st.write("you have to log in first ...")