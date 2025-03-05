import streamlit as st
import pandas as pd
from database import get_db
from models import Course, Chapter, Question
from utils import format_ilos, rerun, confirm_action, show_success, show_error, paginate_data
from sqlalchemy import or_

# Custom rerun function using meta-refresh (instead of st.experimental_rerun)
def rerun():
    st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)
    st.stop()
def paginated_questions(db, items_per_page=10):
    # Get total number of questions
    total_questions = db.query(Question).count()
    total_pages = (total_questions + items_per_page - 1) // items_per_page
    
    # Add pagination controls
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
    
    # Get questions for current page
    start = (page - 1) * items_per_page
    questions = db.query(Question).offset(start).limit(items_per_page).all()
    
    return questions
st.title("View")

# Add search functionality
search_term = st.text_input("Search courses, chapters, and questions", "")

tabs = st.tabs(["View Courses", "View Chapters", "View Questions"])

# ----- Tab 1: View Courses -----
with tabs[0]:
    st.header("Course List")
    db = next(get_db())
    
    # Apply search if provided
    if search_term:
        courses = db.query(Course).filter(
            or_(
                Course.title.ilike(f"%{search_term}%"),
                Course.description.ilike(f"%{search_term}%")
            )
        ).all()
    else:
        courses = db.query(Course).all()
    
    # Paginate courses
    if courses:
        paginated_courses = paginate_data(courses, items_per_page=5, key="courses_view")
        
        for course in paginated_courses:
            with st.expander(f"📚 {course.title}"):
                st.write(course.description)
                st.caption(f"Created: {course.created_at.strftime('%Y-%m-%d')}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Edit {course.title}", key=f"edit_course_{course.id}"):
                        st.session_state["editing_course"] = course.id
                        st.switch_page("edit")
                with col2:
                    delete_key = f"delete_course_{course.id}"
                    if delete_key not in st.session_state:
                        st.session_state[delete_key] = False
                    
                    if st.button(f"Delete {course.title}", key=f"delete_btn_course_{course.id}"):
                        st.session_state[delete_key] = True
                    
                    if st.session_state[delete_key]:
                        st.warning(f"Are you sure you want to delete '{course.title}'? This will also delete all chapters and questions within this course.")
                        confirm_col1, confirm_col2 = st.columns(2)
                        with confirm_col1:
                            if st.button("Yes, Delete", key=f"confirm_delete_course_{course.id}"):
                                try:
                                    db.delete(course)
                                    db.commit()
                                    show_success(f"Course '{course.title}' deleted successfully.")
                                    st.session_state[delete_key] = False
                                    rerun()
                                except Exception as e:
                                    db.rollback()
                                    show_error(f"Error deleting course: {str(e)}")
                        with confirm_col2:
                            if st.button("Cancel", key=f"cancel_delete_course_{course.id}"):
                                st.session_state[delete_key] = False
                                rerun()
    else:
        if search_term:
            st.info(f"No courses found matching '{search_term}'.")
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
    
    # Build query with filters
    query = db.query(Chapter)
    if selected_course[0] != 0:
        query = query.filter(Chapter.course_id == selected_course[0])
    
    # Apply search if provided
    if search_term:
        query = query.filter(
            or_(
                Chapter.title.ilike(f"%{search_term}%"),
                Chapter.summary.ilike(f"%{search_term}%"),
                Chapter.ilos.ilike(f"%{search_term}%")
            )
        )
    
    chapters = query.all()
    
    # Paginate chapters
    if chapters:
        paginated_chapters = paginate_data(chapters, items_per_page=5, key="chapters_view")
        
        for chapter in paginated_chapters:
            with st.expander(f"📖 {chapter.title} ({chapter.course.title})"):
                st.write("**Summary:**")
                st.write(chapter.summary)
                st.write("**Learning Outcomes:**")
                for ilo in format_ilos(chapter.ilos):
                    st.write(f"- {ilo}")
                st.caption(f"Created: {chapter.created_at.strftime('%Y-%m-%d')}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Edit {chapter.title}", key=f"edit_chapter_{chapter.id}"):
                        st.session_state["editing_chapter"] = chapter.id
                        st.switch_page("edit")
                with col2:
                    delete_key = f"delete_chapter_{chapter.id}"
                    if delete_key not in st.session_state:
                        st.session_state[delete_key] = False
                    
                    if st.button(f"Delete {chapter.title}", key=f"delete_btn_chapter_{chapter.id}"):
                        st.session_state[delete_key] = True
                    
                    if st.session_state[delete_key]:
                        st.warning(f"Are you sure you want to delete '{chapter.title}'? This will also delete all questions within this chapter.")
                        confirm_col1, confirm_col2 = st.columns(2)
                        with confirm_col1:
                            if st.button("Yes, Delete", key=f"confirm_delete_chapter_{chapter.id}"):
                                try:
                                    db.delete(chapter)
                                    db.commit()
                                    show_success(f"Chapter '{chapter.title}' deleted successfully.")
                                    st.session_state[delete_key] = False
                                    rerun()
                                except Exception as e:
                                    db.rollback()
                                    show_error(f"Error deleting chapter: {str(e)}")
                        with confirm_col2:
                            if st.button("Cancel", key=f"cancel_delete_chapter_{chapter.id}"):
                                st.session_state[delete_key] = False
                                rerun()
    else:
        if search_term:
            st.info(f"No chapters found matching '{search_term}'.")
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
    
    # Build query with filters
    query = db.query(Question)
    if selected_chapter[0] != 0:
        query = query.filter(Question.chapter_id == selected_chapter[0])
    query = query.filter(Question.difficulty.between(difficulty_filter[0], difficulty_filter[1]))
    if level_filter:
        query = query.filter(Question.student_level.in_(level_filter))
    
    # Apply search if provided
    if search_term:
        query = query.filter(
            or_(
                Question.content.ilike(f"%{search_term}%"),
                Question.tags.ilike(f"%{search_term}%"),
                Question.explanation.ilike(f"%{search_term}%")
            )
        )
    
    questions = query.all()
    
    # Paginate questions
    if questions:
        paginated_questions = paginate_data(questions, items_per_page=5, key="questions_view")
        
        for question in paginated_questions:
            with st.expander(f"❓ Question (Difficulty: {question.difficulty})"):
                st.write(question.content)
                st.write(f"**Estimated Time:** {question.estimated_time} minutes")
                st.write(f"**Student Level:** {question.student_level}")
                if question.tags:
                    st.write(f"**Tags:** {question.tags}")
                if question.question_type:
                    st.write(f"**Type:** {question.question_type}")
                st.caption(f"Created: {question.created_at.strftime('%Y-%m-%d')}")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button(f"Edit Question", key=f"edit_question_{question.id}"):
                        st.session_state["editing_question"] = question.id
                        st.switch_page("edit")
                with col2:
                    delete_key = f"delete_question_{question.id}"
                    if delete_key not in st.session_state:
                        st.session_state[delete_key] = False
                    
                    if st.button(f"Delete Question", key=f"delete_btn_question_{question.id}"):
                        st.session_state[delete_key] = True
                    
                    if st.session_state[delete_key]:
                        st.warning(f"Are you sure you want to delete this question?")
                        confirm_col1, confirm_col2 = st.columns(2)
                        with confirm_col1:
                            if st.button("Yes, Delete", key=f"confirm_delete_question_{question.id}"):
                                try:
                                    db.delete(question)
                                    db.commit()
                                    show_success("Question deleted successfully.")
                                    st.session_state[delete_key] = False
                                    rerun()
                                except Exception as e:
                                    db.rollback()
                                    show_error(f"Error deleting question: {str(e)}")
                        with confirm_col2:
                            if st.button("Cancel", key=f"cancel_delete_question_{question.id}"):
                                st.session_state[delete_key] = False
                                rerun()
                with col3:
                    if st.button("Discuss", key=f"discuss_question_{question.id}"):
                        st.session_state["selected_question_id"] = question.id
                        st.switch_page("pages/discussion.py")
                with col4:
                    if st.button("Attempt", key=f"attempt_question_{question.id}"):
                        st.session_state["selected_question_id"] = question.id
                        st.switch_page("pages/question_attempt.py")
    else:
        if search_term:
            st.info(f"No questions found matching '{search_term}'.")
        else:
            st.info("No questions found.")
