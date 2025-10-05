import os
import requests
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
    if "google_creds" in st.session_state:
        creds = st.session_state["google_creds"]

        # The Google creds object isn't directly JSON serializable.
        # You need to convert it into a dictionary.
        creds_dict = {
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes,
            "id_token": creds.id_token,
            "expiry": creds.expiry.isoformat(), # Convert datetime to string
        }

        try:
            # Define the Flask backend URL
            backend_url = "http://127.0.0.1:5000/gmail-access"

            # Make a POST request with the credentials
            response = requests.post(backend_url, json=creds_dict)
            response.raise_for_status() # Raise an exception for bad status codes

            st.success("Credentials sent to backend successfully!")
            st.write("Backend response:", response.json())

        except requests.exceptions.RequestException as e:
            st.error(f"Error sending credentials to backend: {e}")
    if st.button("Log out"):
        authenticator.logout()

if not st.session_state["connected"]:
    st.write("you have to log in first ...")