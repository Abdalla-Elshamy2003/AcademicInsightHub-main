import streamlit as st
from database import get_db
from models import User, Role, UserRole
from sqlalchemy.exc import IntegrityError
from utils import (
    hash_password, verify_password, validate_email, 
    validate_username, validate_password_strength,
    show_success, show_error, show_warning, show_info, rerun
)
from datetime import datetime
import json

# --- Initialize authentication view ---
if "auth_view" not in st.session_state:
    st.session_state.auth_view = "login"

# --- LOGIN VIEW ---
if st.session_state.auth_view == "login":
    st.title("Login")
    with st.form("login_form"):
        username_or_email = st.text_input("Username or Email")
        password = st.text_input("Password", type="password")
        login_submit = st.form_submit_button("Login")
        
    if login_submit:
        if username_or_email and password:
            db = next(get_db())
            user = db.query(User).filter(
                (User.username == username_or_email) | (User.email == username_or_email)
            ).first()
            
            if user and verify_password(user.password, password, user.salt):
                # Get user role
                user_role = db.query(UserRole).filter_by(user_id=user.id).first()
                role = db.query(Role).filter(Role.id == user_role.role_id).first() if user_role else None
                
                # Update last login time
                user.last_login = datetime.utcnow()
                db.commit()
                
                # Store user info in session state
                st.session_state["user"] = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": role.name if role else None
                }
                
                # Parse permissions if role exists
                if role:
                    permissions = json.loads(role.permissions)
                    st.session_state.user["permissions"] = permissions
                
                show_success("Login successful!")
                # Force a full page rerun to apply session state changes
                st.rerun()
            else:
                show_error("Invalid credentials")
        else:
            show_error("Please fill in all fields")

    # Registration link
    if st.button("Create an Account"):
        st.session_state.auth_view = "register"
        rerun()

# --- REGISTER VIEW ---
elif st.session_state.auth_view == "register":
    st.title("Register")
    
    # Get available roles from database
    db = next(get_db())
    available_roles = [role.name.capitalize() for role in db.query(Role).all() 
                      if role.name.lower() != "admin"]  # Exclude admin role from registration
    
    with st.form("register_form"):
        username = st.text_input("Username (3-50 characters, alphanumeric)")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password", 
                               help="At least 8 characters with uppercase, lowercase, number, and special character")
        confirm_password = st.text_input("Confirm Password", type="password")
        role_type = st.selectbox("Register as", available_roles)
        submit = st.form_submit_button("Register")
    
    if submit:
        # Validate all inputs
        valid_inputs = True
        
        if not username or not email or not password or not confirm_password:
            show_error("Please fill in all fields")
            valid_inputs = False
        
        if valid_inputs and not validate_username(username):
            show_error("Username must be 3-50 characters and contain only letters, numbers, and underscores")
            valid_inputs = False
            
        if valid_inputs and not validate_email(email):
            show_error("Please enter a valid email address")
            valid_inputs = False
            
        if valid_inputs:
            is_strong, message = validate_password_strength(password)
            if not is_strong:
                show_error(message)
                valid_inputs = False
                
        if valid_inputs and password != confirm_password:
            show_error("Passwords do not match")
            valid_inputs = False
            
        if valid_inputs:
            # Check if role exists
            role = db.query(Role).filter_by(name=role_type.lower()).first()
            if not role:
                show_error("Role not found. Please run init_db.py first")
                valid_inputs = False
                
        if valid_inputs:
            # Create new user with secure password
            hashed_password, salt = hash_password(password)
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                salt=salt,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            try:
                # Add user and role
                db.add(new_user)
                db.flush()  # Get the user ID
                
                user_role = UserRole(
                    user_id=new_user.id, 
                    role_id=role.id,
                    created_at=datetime.utcnow()
                )
                db.add(user_role)
                db.commit()
                
                show_success("Registration successful! Please login.")
                st.session_state.auth_view = "login"
                rerun()
            except IntegrityError:
                db.rollback()
                show_error("Username or email already exists")
            except Exception as e:
                db.rollback()
                show_error(f"An error occurred: {str(e)}")

    if st.button("Back to Login"):
        st.session_state.auth_view = "login"
        rerun()

# --- FORGOT PASSWORD VIEW ---
elif st.session_state.auth_view == "forgot_password":
    st.title("Reset Password")
    
    with st.form("reset_password_form"):
        email = st.text_input("Email")
        submit = st.form_submit_button("Send Reset Link")
    
    if submit and email:
        if validate_email(email):
            # In a real application, this would send an email with a reset link
            # For this demo, we'll just show a success message
            show_info("If an account with this email exists, a password reset link will be sent.")
            # In a real app, you would generate a token, store it, and send an email
        else:
            show_error("Please enter a valid email address")
    
    if st.button("Back to Login"):
        st.session_state.auth_view = "login"
        rerun()

# Add a forgot password link to the login page
if st.session_state.auth_view == "login":
    if st.button("Forgot Password?"):
        st.session_state.auth_view = "forgot_password"
        rerun()
