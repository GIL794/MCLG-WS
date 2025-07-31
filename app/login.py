# commented out for now


""" import streamlit as st
from app.utils.auth import register_user, authenticate_user
import bcrypt
import time

SESSION_TIMEOUT = 3600  # 1 hour
if 'login_time' in st.session_state and time.time() - st.session_state['login_time'] > SESSION_TIMEOUT:
    st.session_state['logged_in'] = False
    st.warning("Session expired. Please log in again.")
    st.experimental_rerun()

def render_login_ui():
    """
#Render the login and registration page.
"""
    st.title("Login or Register")

    # Tabs for Login and Registration
    tab1, tab2 = st.tabs(["Login", "Register"])

    # Login Tab
    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_button = st.button("Login")

        if login_button:
            success, result = authenticate_user(username, password)
            if success:
                st.session_state["logged_in"] = True
                st.session_state["username"] = result["username"]
                st.session_state["records"] = result.get("records", [])
                st.session_state['login_time'] = time.time()
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error(result)

    # Registration Tab
    with tab2:
        st.subheader("Register")
        reg_username = st.text_input("Username", key="register_username")
        reg_password = st.text_input("Password", type="password", key="register_password")
        register_button = st.button("Register")

        if register_button:
            success, message = register_user(reg_username, reg_password)
            if success:
                st.success(message)
            else:
                st.error(message)

hashed_password = bcrypt.hashpw("password1".encode("utf-8"), bcrypt.gensalt())
print(hashed_password)
"""