import streamlit as st
import yaml
from swiftclient.client import Connection
import os

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
    uploaded = st.file_uploader("Choose a file", type=["csv", "xlsx", "dat"])

    if uploaded:
        file_path = f"/tmp/{uploaded.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded.read())
        st.success("✅ File saved locally")

        # === Try Swift Upload ===
        if "swift" in st.secrets:
            try:
                st.info("🔄 Initializing Swift connection...")

                swift_cfg = st.secrets["swift"]
                conn = Connection(
                    authurl=swift_cfg["authurl"],
                    user=swift_cfg["user"],
                    key=swift_cfg["key"],
                    os_options={
                        "project_id": swift_cfg["project_id"],
                        "user_domain_name": swift_cfg["user_domain_name"],
                        "project_domain_name": swift_cfg["project_domain_name"],
                        "region_name": swift_cfg["region_name"],
                        "auth_version": "3"
                    },
                    auth_version="3"
                )
                st.success("🔗 Connected to Swift")

                container = "detachlog-anon"
                st.write(f"📤 Uploading to container `{container}`...")

                with open(file_path, "rb") as f:
                    conn.put_container(container)
                    conn.put_object(container, uploaded.name, contents=f)
                st.success("☁️ Upload to Swift successful!")

            except Exception as e:
                st.error("❌ Swift upload failed.")
                st.exception(e)
        else:
            st.warning("⚠️ Swift credentials not found in Streamlit secrets.")
