import streamlit as st
from database import get_db
from models import Course, Chapter, Question
from utils import show_success, show_error

st.title("Add New Item")

# Use a dropdown (selectbox) to choose which item to add
option = st.selectbox("Select item to add", ["Course", "Chapter", "Question"])

if option == "Course":
    st.subheader("Add New Course")
    with st.form("course_form"):
        title = st.text_input("Course Title")
        description = st.text_area("Course Description")
        submit = st.form_submit_button("Create Course")
    if submit and title:
        db = next(get_db())
        try:
            new_course = Course(title=title, description=description)
            db.add(new_course)
            db.commit()
            show_success("Course created successfully!")
        except Exception as e:
            show_error(f"Error creating course: {str(e)}")

elif option == "Chapter":
    st.subheader("Add New Chapter")
    db = next(get_db())
    courses = db.query(Course).all()
    with st.form("chapter_form"):
        course_choice = st.selectbox(
            "Select Course",
            options=[(c.id, c.title) for c in courses],
            format_func=lambda x: x[1]
        )
        title = st.text_input("Chapter Title")
        summary = st.text_area("Chapter Summary")
        ilos = st.text_area("Intended Learning Outcomes (One per line)")
        submit = st.form_submit_button("Create Chapter")
    if submit and title and course_choice:
        try:
            new_chapter = Chapter(
                course_id=course_choice[0],
                title=title,
                summary=summary,
                ilos=ilos
            )
            db.add(new_chapter)
            db.commit()
            show_success("Chapter created successfully!")
        except Exception as e:
            show_error(f"Error creating chapter: {str(e)}")

elif option == "Question":
    st.subheader("Add New Question")
    db = next(get_db())
    chapters = db.query(Chapter).all()
    with st.form("question_form"):
        chapter_choice = st.selectbox(
            "Select Chapter",
            options=[(c.id, f"{c.course.title} - {c.title}") for c in chapters],
            format_func=lambda x: x[1]
        )
        content = st.text_area("Question Content")
        difficulty = st.slider("Difficulty Level", 1.0, 5.0, 3.0, 0.5)
        estimated_time = st.number_input("Estimated Time (minutes)", min_value=1, value=5)
        student_level = st.selectbox("Student Level", ["Beginner", "Intermediate", "Advanced"])
        submit = st.form_submit_button("Create Question")
    if submit and content and chapter_choice:
        try:
            new_question = Question(
                chapter_id=chapter_choice[0],
                content=content,
                difficulty=difficulty,
                estimated_time=estimated_time,
                student_level=student_level
            )
            db.add(new_question)
            db.commit()
            show_success("Question created successfully!")
        except Exception as e:
            show_error(f"Error creating question: {str(e)}")
