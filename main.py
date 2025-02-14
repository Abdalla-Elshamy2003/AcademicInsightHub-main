import streamlit as st
from database import engine
import models

# Create all database tables (including the users table)
models.Base.metadata.create_all(bind=engine)

st.set_page_config(
    page_title="Educational Platform",
    page_icon="📚",
    layout="wide"
)

# --- Authentication Check ---
if "user" not in st.session_state:
    st.info("Please log in to access the application.")
    # Render the auth page inline (which hides the sidebar)
    import pages.auth as auth
    st.stop()

# --- Header for Logged-In Users ---
header_cols = st.columns([4, 1])
with header_cols[0]:
    st.markdown(f"### Welcome, {st.session_state.user['username']}!")
with header_cols[1]:
    if st.button("Logout"):
        st.session_state.pop("user")
        st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)
        st.stop()

# --- Navigation Sidebar ---
page = st.sidebar.selectbox(
    "Navigation",
    ["View", "Add", "Student Feedback", "Analytics"]
)

if page == "View":
    st.switch_page("view")
elif page == "Add":
    st.switch_page("add")
elif page == "Student Feedback":
    st.switch_page("student_feedback")
elif page == "Analytics":
    st.switch_page("analytics")

