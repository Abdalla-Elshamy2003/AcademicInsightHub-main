import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_db
from models import StudentProgress, Question, Chapter, Course
from utils import show_error, show_info
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page title
st.title("My Progress")

# Check if user is logged in
if "user" not in st.session_state:
    show_error("Please log in to view your progress.")
    st.stop()

# Get user ID from session
user_id = st.session_state.user["id"]

# Get user progress data
db = next(get_db())
progress_data = db.query(
    StudentProgress, Question, Chapter, Course
).join(
    Question, StudentProgress.question_id == Question.id
).join(
    Chapter, Question.chapter_id == Chapter.id
).join(
    Course, Chapter.course_id == Course.id
).filter(
    StudentProgress.user_id == user_id
).all()

if not progress_data:
    st.info("You haven't attempted any questions yet. Start practicing to see your progress!")
    st.stop()

# Create DataFrame for analysis
data = []
for progress, question, chapter, course in progress_data:
    data.append({
        "question_id": question.id,
        "question": question.content[:50] + "..." if len(question.content) > 50 else question.content,
        "chapter": chapter.title,
        "course": course.title,
        "attempts": progress.attempts,
        "correct": progress.correct,
        "difficulty": question.difficulty,
        "last_attempt": progress.last_attempt_date,
        "question_type": question.question_type
    })

df = pd.DataFrame(data)

# Display summary statistics
st.header("Summary Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Questions Attempted", len(df))
    
with col2:
    success_rate = round(df["correct"].mean() * 100, 1) if not df.empty else 0
    st.metric("Success Rate", f"{success_rate}%")
    
with col3:
    avg_attempts = round(df["attempts"].mean(), 1) if not df.empty else 0
    st.metric("Average Attempts per Question", avg_attempts)

# Progress over time
st.header("Progress Over Time")

# Group by date and calculate metrics
df["date"] = pd.to_datetime(df["last_attempt"]).dt.date
time_data = df.groupby("date").agg({
    "question_id": "count",
    "correct": "mean"
}).reset_index()
time_data["correct"] = time_data["correct"] * 100  # Convert to percentage

# Create line chart
fig = px.line(
    time_data, 
    x="date", 
    y=["question_id", "correct"],
    labels={"value": "Count / Percentage", "date": "Date", "variable": "Metric"},
    title="Your Progress Over Time",
    color_discrete_map={"question_id": "blue", "correct": "green"}
)
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# Performance by difficulty
st.header("Performance by Difficulty")
difficulty_data = df.groupby("difficulty").agg({
    "question_id": "count",
    "correct": "mean",
    "attempts": "mean"
}).reset_index()
difficulty_data["correct"] = difficulty_data["correct"] * 100  # Convert to percentage

fig = px.bar(
    difficulty_data,
    x="difficulty",
    y="correct",
    title="Success Rate by Difficulty Level",
    labels={"difficulty": "Difficulty Level", "correct": "Success Rate (%)"},
    color="correct",
    color_continuous_scale=["red", "yellow", "green"]
)
st.plotly_chart(fig, use_container_width=True)

# Performance by course
st.header("Performance by Course")
course_data = df.groupby("course").agg({
    "question_id": "count",
    "correct": "mean"
}).reset_index()
course_data["correct"] = course_data["correct"] * 100  # Convert to percentage

fig = px.bar(
    course_data,
    x="course",
    y="correct",
    title="Success Rate by Course",
    labels={"course": "Course", "correct": "Success Rate (%)"},
    color="correct",
    color_continuous_scale=["red", "yellow", "green"]
)
st.plotly_chart(fig, use_container_width=True)

# Recent activity
st.header("Recent Activity")
recent_df = df.sort_values("last_attempt", ascending=False).head(10)

for _, row in recent_df.iterrows():
    with st.expander(f"{row['course']} - {row['chapter']} - {row['question'][:30]}..."):
        st.write(f"**Course:** {row['course']}")
        st.write(f"**Chapter:** {row['chapter']}")
        st.write(f"**Question Type:** {row['question_type']}")
        st.write(f"**Difficulty:** {row['difficulty']}")
        st.write(f"**Attempts:** {row['attempts']}")
        st.write(f"**Correct:** {'Yes' if row['correct'] else 'No'}")
        st.write(f"**Last Attempt:** {row['last_attempt']}")
        
        # Add button to retry question
        if st.button(f"Retry Question", key=f"retry_{row['question_id']}"):
            st.session_state["selected_question_id"] = row["question_id"]
            st.switch_page("pages/question_attempt.py") 