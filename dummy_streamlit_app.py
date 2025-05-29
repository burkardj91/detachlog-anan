import streamlit as st
import yaml

# Load users from config.yaml
with open("config.yaml") as f:
    config = yaml.safe_load(f)

st.set_page_config(page_title="🔐 Secure App")

# Session state to track login status
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

# Show login only if not authenticated
if not st.session_state.authenticated:
    st.title("🔐 Login Required")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if username in config['users'] and password == config['users'][username]['password']:
            st.session_state.authenticated = True
            st.session_state.user = username
            st.success(f"✅ Welcome, {username}!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

# Show protected content
if st.session_state.authenticated:
    st.title(f"🎯 Welcome, {st.session_state.user}!")
    st.markdown("""
    Here’s your secure dashboard content.  
    You can now:
    - Upload data
    - Analyze trends
    - Download reports
    """)

    # Example: secure upload
    st.subheader("📂 Upload your file")
    st.file_uploader("Choose a file", type=["csv", "xlsx"])
