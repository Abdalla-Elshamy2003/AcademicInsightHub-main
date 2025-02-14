import streamlit as st
from database import get_db
from models import User
from sqlalchemy.exc import IntegrityError
import hashlib

# --- Helper: hash passwords ---
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# --- Helper: rerun using meta refresh (since experimental_rerun isn't available) ---
def rerun():
    st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)
    st.stop()

# --- Initialize authentication view ---
if "auth_view" not in st.session_state:
    st.session_state.auth_view = "login"

# --- Hide the sidebar on the auth page ---
hide_sidebar_style = """
    <style>
    [data-testid="stSidebar"] { display: none; }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# --- LOGIN VIEW ---
if st.session_state.auth_view == "login":
    st.title("Login")
    with st.form("login_form"):
        username_or_email = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        login_submit = st.form_submit_button("Login")
    # Place "Register" and "Forgot Password?" buttons side by side
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register"):
            st.session_state.auth_view = "register"
            rerun()
    with col2:
        if st.button("Forgot Password?"):
            st.session_state.auth_view = "forgot"
            rerun()
    
    if login_submit:
        db = next(get_db())
        hashed = hash_password(password)
        user = db.query(User).filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()
        if user and user.password == hashed:
            st.session_state["user"] = {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
            st.success("Logged in successfully! Redirecting to Analytics...")
            st.switch_page("analytics")  # Ensure your analytics page file is named analytics.py
            st.stop()
        else:
            st.error("Invalid credentials. Please try again.")

# --- REGISTER VIEW ---
elif st.session_state.auth_view == "register":
    st.title("Register")
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        register_submit = st.form_submit_button("Register")
    if register_submit:
        if password != confirm_password:
            st.error("Passwords do not match.")
        else:
            db = next(get_db())
            hashed = hash_password(password)
            new_user = User(username=username, email=email, password=hashed)
            try:
                db.add(new_user)
                db.commit()
                st.success("Registration successful! Please log in.")
                st.session_state.auth_view = "login"
                rerun()
            except IntegrityError:
                db.rollback()
                st.error("Username or email already exists.")
            except Exception as e:
                db.rollback()
                st.error(f"An error occurred: {str(e)}")
    if st.button("Back to Login"):
        st.session_state.auth_view = "login"
        rerun()

# --- FORGOT PASSWORD VIEW ---
elif st.session_state.auth_view == "forgot":
    st.title("Forgot Password")
    with st.form("forgot_password_form"):
        email = st.text_input("Enter your registered email")
        forgot_submit = st.form_submit_button("Reset Password")
    if forgot_submit:
        db = next(get_db())
        user = db.query(User).filter(User.email == email).first()
        if user:
            st.success("A password reset link has been sent to your email (simulation).")
        else:
            st.error("Email not found. Please check your email or register.")
    if st.button("Back to Login"):
        st.session_state.auth_view = "login"
        rerun()
