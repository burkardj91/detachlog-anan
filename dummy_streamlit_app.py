import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# === Configuration ===
names = ['Alice Smith', 'Bob Jones']
usernames = ['alice', 'bob']
passwords = ['abc123', 'def456']  # Plaintext initially

# === Hash the passwords ===
hashed_passwords = stauth.Hasher(passwords).generate()

# === YAML-style config dictionary ===
config = {
    'credentials': {
        'usernames': {
            usernames[i]: {
                'name': names[i],
                'password': hashed_passwords[i]
            } for i in range(len(usernames))
        }
    },
    'cookie': {
        'name': 'my_app_cookie',
        'key': 'some_secret_key',
        'expiry_days': 30
    },
    'preauthorized': {
        'emails': []
    }
}

# === Authenticator ===
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login('Login', 'main')

# === App Logic ===
if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.title(f"🎯 Welcome {name}!")
    st.success("You have access to the protected app.")
    # Your app content here
    st.write("This is your Streamlit dashboard.")

elif authentication_status is False:
    st.error("Username/password is incorrect.")
elif authentication_status is None:
    st.warning("Please enter your username and password.")
