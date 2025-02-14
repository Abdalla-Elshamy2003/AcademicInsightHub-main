import streamlit as st
import pandas as pd
from database import get_db
from models import Course, Chapter, Question
from utils import format_ilos  # assumed to be defined in utils.py

# Custom rerun function using meta-refresh (instead of st.experimental_rerun)
def rerun():
    st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)
    st.stop()

st.title("View")

tabs = st.tabs(["View Courses", "View Chapters", "View Questions"])

# ----- Tab 1: View Courses -----
with tabs[0]:
    st.header("Course List")
    db = next(get_db())
    courses = db.query(Course).all()
    if courses:
        for course in courses:
            with st.expander(f"📚 {course.title}"):
                st.write(course.description)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Edit {course.title}", key=f"edit_course_{course.id}"):
                        st.session_state["editing_course"] = course.id
                        st.switch_page("edit")
                with col2:
                    if st.button(f"Delete {course.title}", key=f"delete_course_{course.id}"):
                        db.delete(course)
                        db.commit()
                        rerun()  # Refresh the page after deletion
    else:
        st.info("No courses found.")

# ----- Tab 2: View Chapters -----
with tabs[1]:
    st.header("Chapter List")
    db = next(get_db())
    courses = db.query(Course).all()
    # Allow filtering chapters by course
    selected_course = st.selectbox(
        "Filter by Course",
        options=[(0, "All Courses")] + [(c.id, c.title) for c in courses],
        format_func=lambda x: x[1]
    )
    query = db.query(Chapter)
    if selected_course[0] != 0:
        query = query.filter(Chapter.course_id == selected_course[0])
    chapters = query.all()
    if chapters:
        for chapter in chapters:
            with st.expander(f"📖 {chapter.title}"):
                st.write("**Summary:**")
                st.write(chapter.summary)
                st.write("**Learning Outcomes:**")
                for ilo in format_ilos(chapter.ilos):
                    st.write(f"- {ilo}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Edit {chapter.title}", key=f"edit_chapter_{chapter.id}"):
                        st.session_state["editing_chapter"] = chapter.id
                        st.switch_page("edit")
                with col2:
                    if st.button(f"Delete {chapter.title}", key=f"delete_chapter_{chapter.id}"):
                        db.delete(chapter)
                        db.commit()
                        rerun()
    else:
        st.info("No chapters found.")

# ----- Tab 3: View Questions -----
with tabs[2]:
    st.header("Question List")
    db = next(get_db())
    chapters = db.query(Chapter).all()
    # Filters for questions
    filter_cols = st.columns(3)
    with filter_cols[0]:
        selected_chapter = st.selectbox(
            "Filter by Chapter",
            options=[(0, "All Chapters")] + [(c.id, f"{c.course.title} - {c.title}") for c in chapters],
            format_func=lambda x: x[1]
        )
    with filter_cols[1]:
        difficulty_filter = st.slider("Filter by Difficulty", 1.0, 5.0, (1.0, 5.0), 0.5)
    with filter_cols[2]:
        level_filter = st.multiselect("Filter by Student Level", ["Beginner", "Intermediate", "Advanced"])
    query = db.query(Question)
    if selected_chapter[0] != 0:
        query = query.filter(Question.chapter_id == selected_chapter[0])
    query = query.filter(Question.difficulty.between(difficulty_filter[0], difficulty_filter[1]))
    if level_filter:
        query = query.filter(Question.student_level.in_(level_filter))
    questions = query.all()
    if questions:
        for question in questions:
            with st.expander(f"❓ Question (Difficulty: {question.difficulty})"):
                st.write(question.content)
                st.write(f"**Estimated Time:** {question.estimated_time} minutes")
                st.write(f"**Student Level:** {question.student_level}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Edit Question", key=f"edit_question_{question.id}"):
                        st.session_state["editing_question"] = question.id
                        st.switch_page("edit")
                with col2:
                    if st.button(f"Delete Question", key=f"delete_question_{question.id}"):
                        db.delete(question)
                        db.commit()
                        rerun()
    else:
        st.info("No questions found.")
