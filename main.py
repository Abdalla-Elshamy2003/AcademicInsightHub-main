import streamlit as st
from database import engine, get_db, init_db
import models
from models import Role, UserRole
import logging
from utils import show_error, show_info, rerun
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Create all database tables (including the users table)
    init_db()
    
    st.set_page_config(
        page_title="Academic Insight Hub",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # --- Authentication Check ---
    if "user" not in st.session_state:
        show_info("Please log in to access the application.")
        # Render the auth page inline (which hides the sidebar)
        import pages.auth as auth
        st.stop()
    
    # --- Header for Logged-In Users ---
    header_cols = st.columns([4, 1])
    with header_cols[0]:
        st.markdown(f"### Welcome to Academic Insight Hub, {st.session_state.user['username']}!")
    with header_cols[1]:
        if st.button("Logout"):
            st.session_state.pop("user")
            rerun()
    
    # --- Navigation Sidebar ---
    # Get user role
    if "user" in st.session_state:
        try:
            db = next(get_db())
            user_role = db.query(UserRole).filter_by(user_id=st.session_state.user["id"]).first()
            if user_role:
                role = db.query(Role).get(user_role.role_id)
                if role:
                    st.session_state.user["role"] = role.name
                    # Parse permissions
                    import json
                    permissions = json.loads(role.permissions)
                    st.session_state.user["permissions"] = permissions
                else:
                    logger.error(f"Role not found for user {st.session_state.user['username']}")
            else:
                logger.error(f"UserRole not found for user {st.session_state.user['username']}")
        except Exception as e:
            logger.error(f"Error getting user role: {str(e)}")
            logger.error(traceback.format_exc())
        
        # Navigation based on role
        role = st.session_state.user.get("role", "").lower()
        
        if role == "admin":
            page = st.sidebar.selectbox(
                "Navigation",
                ["View", "Add", "Analytics Dashboard", "Question Bank", "User Management", "Question Analysis"]
            )
        elif role == "professor":
            page = st.sidebar.selectbox(
                "Navigation",
                ["View", "Add", "Analytics Dashboard", "Question Bank", "Question Analysis"]
            )
        elif role == "teaching_assistant":
            page = st.sidebar.selectbox(
                "Navigation",
                ["View", "Add Questions", "Analytics Dashboard", "Question Analysis"]
            )
        else:  # student role or default
            page = st.sidebar.selectbox(
                "Navigation",
                ["View", "Student Feedback", "My Progress"]
            )
        
        # Display user info in sidebar
        with st.sidebar.expander("User Information"):
            st.write(f"**Username:** {st.session_state.user['username']}")
            st.write(f"**Email:** {st.session_state.user['email']}")
            st.write(f"**Role:** {st.session_state.user.get('role', 'Unknown')}")
    
    # --- Page Routing ---
    try:
        if page == "View":
            st.switch_page("pages/view.py")
        elif page == "Add":
            st.switch_page("pages/add.py")
        elif page == "Add Questions":
            st.switch_page("pages/add.py")
        elif page == "Student Feedback":
            st.switch_page("pages/student_feedback.py")
        elif page == "Analytics Dashboard":
            st.switch_page("pages/Analytics_Dashboard.py")
        elif page == "Question Bank":
            st.switch_page("pages/question_bank.py")
        elif page == "My Progress":
            st.switch_page("pages/my_progress.py")
        elif page == "User Management":
            st.switch_page("pages/user_management.py")
        elif page == "Question Analysis":
            st.switch_page("pages/question_analysis.py")
    except Exception as e:
        show_error(f"Error loading page: {str(e)}")
        logger.error(f"Error loading page '{page}': {str(e)}")
        logger.error(traceback.format_exc())

except Exception as e:
    show_error(f"Application error: {str(e)}")
    logger.error(f"Application error: {str(e)}")
    logger.error(traceback.format_exc())

