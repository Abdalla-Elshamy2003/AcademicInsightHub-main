import streamlit as st
import plotly.express as px
import pandas as pd

def show_success(message):
    st.success(message)

def show_error(message):
    st.error(message)

def create_difficulty_chart(data):
    fig = px.histogram(
        data,
        x="difficulty",
        title="Question Difficulty Distribution",
        labels={"difficulty": "Difficulty Level", "count": "Number of Questions"},
        nbins=20
    )
    return fig

def create_gpa_correlation_chart(data):
    fig = px.scatter(
        data,
        x="student_gpa",
        y="difficulty_rating",
        title="GPA vs Perceived Difficulty",
        labels={
            "student_gpa": "Student GPA",
            "difficulty_rating": "Perceived Difficulty"
        }
    )
    return fig

def format_ilos(ilos_text):
    """Convert ILOs text to formatted list"""
    if not ilos_text:
        return []
    return [ilo.strip() for ilo in ilos_text.split('\n') if ilo.strip()]
