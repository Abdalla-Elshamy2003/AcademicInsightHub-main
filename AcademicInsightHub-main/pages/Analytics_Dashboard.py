# import streamlit as st
# import pandas as pd
# from database import get_db
# from models import Question, StudentFeedback
# from utils import create_difficulty_chart, create_gpa_correlation_chart

# st.title("Analytics Dashboard")

# def load_analytics_data():
#     db = next(get_db())
    
#     # Question difficulty distribution
#     questions = pd.read_sql(
#         db.query(Question).statement,
#         db.bind
#     )
    
#     # Student feedback analysis
#     feedback = pd.read_sql(
#         db.query(StudentFeedback).statement,
#         db.bind
#     )
    
#     return questions, feedback

# def show_analytics():
#     questions, feedback = load_analytics_data()
    
#     # Question Statistics
#     st.subheader("Question Statistics")
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.metric("Total Questions", len(questions))
#     with col2:
#         st.metric("Average Difficulty", f"{questions['difficulty'].mean():.2f}")
#     with col3:
#         st.metric("Average Time", f"{questions['estimated_time'].mean():.0f} min")
    
#     # Difficulty Distribution
#     st.subheader("Question Difficulty Distribution")
#     st.plotly_chart(create_difficulty_chart(questions), use_container_width=True)
    
#     # Student Performance
#     if not feedback.empty:
#         st.subheader("Student Performance Analysis")
#         st.plotly_chart(create_gpa_correlation_chart(feedback), use_container_width=True)
        
#         # Performance Metrics
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Average Student GPA", f"{feedback['student_gpa'].mean():.2f}")
#         with col2:
#             st.metric("Average Attendance Rate", f"{feedback['attendance_rate'].mean():.1%}")

# show_analytics()
import streamlit as st
import pandas as pd
from database import get_db
from models import Question, StudentFeedback
from utils import create_difficulty_chart, create_gpa_correlation_chart

st.title("Analytics Dashboard")

def load_analytics_data():
    db = next(get_db())
    
    # Question difficulty distribution
    questions = pd.read_sql(
        db.query(Question).statement,
        db.bind
    )
    
    # Student feedback analysis
    feedback = pd.read_sql(
        db.query(StudentFeedback).statement,
        db.bind
    )
    
    return questions, feedback

def show_analytics():
    questions, feedback = load_analytics_data()
    
    # Question Statistics
    st.subheader("Question Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Questions", len(questions))
    with col2:
        st.metric("Average Difficulty", f"{questions['difficulty'].mean():.2f}")
    with col3:
        st.metric("Average Time", f"{questions['estimated_time'].mean():.0f} min")
    
    # Difficulty Distribution
    st.subheader("Question Difficulty Distribution")
    st.plotly_chart(create_difficulty_chart(questions), use_container_width=True)
    
    # Student Performance
    if not feedback.empty:
        st.subheader("Student Performance Analysis")
        st.plotly_chart(create_gpa_correlation_chart(feedback), use_container_width=True)
        
        # Performance Metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Student GPA", f"{feedback['student_gpa'].mean():.2f}")
        with col2:
            st.metric("Average Attendance Rate", f"{feedback['attendance_rate'].mean():.1%}")

show_analytics()
