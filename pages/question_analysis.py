import streamlit as st
from database import get_db
from models import Question, Chapter, Course
from utils import show_error, show_success, show_info
import llm_utils
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page title
st.title("Question Analysis with AI")

# Check if user is logged in
if "user" not in st.session_state:
    show_error("Please log in to access this feature.")
    st.stop()

# Check if user has appropriate role
user_role = st.session_state.user.get("role", "").lower()
if user_role not in ["professor", "admin", "teaching_assistant"]:
    show_error("You don't have permission to access this feature.")
    st.stop()

# Check if Groq API key is set
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("⚠️ Groq API key is not set. Please set the GROQ_API_KEY environment variable.")
    st.info("You can set this by creating a .env file with GROQ_API_KEY=your_api_key or by setting it as an environment variable.")
    st.markdown("Get your API key from [Groq Console](https://console.groq.com/)")
    st.stop()

# Main content
st.write("This tool uses AI to analyze questions, rate their difficulty, and suggest improvements based on the course's Intended Learning Outcomes (ILOs).")

# Option to analyze existing question or create a new one
analysis_option = st.radio(
    "Choose an option:",
    ["Analyze Existing Question", "Analyze New Question"]
)

if analysis_option == "Analyze Existing Question":
    # Get courses from database
    db = next(get_db())
    courses = db.query(Course).all()
    
    if not courses:
        st.info("No courses found. Please add a course first.")
        st.stop()
    
    # Course selection
    selected_course = st.selectbox(
        "Select Course",
        options=[(c.id, c.title) for c in courses],
        format_func=lambda x: x[1]
    )
    
    # Get chapters for selected course
    chapters = db.query(Chapter).filter(Chapter.course_id == selected_course[0]).all()
    
    if not chapters:
        st.info(f"No chapters found for course '{selected_course[1]}'. Please add a chapter first.")
        st.stop()
    
    # Chapter selection
    selected_chapter = st.selectbox(
        "Select Chapter",
        options=[(c.id, c.title) for c in chapters],
        format_func=lambda x: x[1]
    )
    
    # Get questions for selected chapter
    questions = db.query(Question).filter(Question.chapter_id == selected_chapter[0]).all()
    
    if not questions:
        st.info(f"No questions found for chapter '{selected_chapter[1]}'. Please add a question first.")
        st.stop()
    
    # Question selection
    selected_question = st.selectbox(
        "Select Question",
        options=[(q.id, q.content[:50] + "..." if len(q.content) > 50 else q.content) for q in questions],
        format_func=lambda x: x[1]
    )
    
    # Get selected question details
    question = db.query(Question).filter(Question.id == selected_question[0]).first()
    chapter = db.query(Chapter).filter(Chapter.id == question.chapter_id).first()
    course = db.query(Course).filter(Course.id == chapter.course_id).first()
    
    # Display question details
    st.subheader("Question Details")
    st.write(f"**Course:** {course.title}")
    st.write(f"**Chapter:** {chapter.title}")
    st.write(f"**Question Type:** {question.question_type or 'Not specified'}")
    st.write(f"**Current Difficulty:** {question.difficulty}")
    st.write(f"**Question Content:**")
    st.write(question.content)
    
    # Display ILOs
    st.subheader("Intended Learning Outcomes (ILOs)")
    if chapter.ilos:
        st.write(chapter.ilos)
    else:
        st.write("No ILOs specified for this chapter.")
    
    # Analyze button
    if st.button("Analyze Question"):
        with st.spinner("Analyzing question with AI... This may take a few moments."):
            try:
                # Call LLM to analyze question
                difficulty_rating, improvement_suggestions = llm_utils.analyze_question(
                    question_content=question.content,
                    question_type=question.question_type or "Unknown",
                    course_title=course.title,
                    chapter_title=chapter.title,
                    ilos=chapter.ilos or "Not specified"
                )
                
                if difficulty_rating is not None:
                    st.subheader("Analysis Results")
                    
                    # Display difficulty rating
                    st.write(f"**AI-Suggested Difficulty Rating:** {difficulty_rating}")
                    
                    # Compare with current difficulty
                    if abs(difficulty_rating - question.difficulty) > 0.5:
                        st.warning(f"The AI-suggested difficulty rating differs significantly from the current rating ({question.difficulty}).")
                    
                    # Option to update difficulty
                    if st.button("Update Difficulty Rating"):
                        question.difficulty = difficulty_rating
                        db.commit()
                        show_success(f"Difficulty rating updated to {difficulty_rating}.")
                
                # Display improvement suggestions
                if improvement_suggestions:
                    st.subheader("Improvement Suggestions")
                    st.write(improvement_suggestions)
                else:
                    st.error("Failed to generate improvement suggestions. Please try again.")
            except Exception as e:
                st.error(f"Error analyzing question: {str(e)}")
                logger.error(f"Error analyzing question: {str(e)}")

else:  # Analyze New Question
    # Get courses from database
    db = next(get_db())
    courses = db.query(Course).all()
    
    if not courses:
        st.info("No courses found. Please add a course first.")
        st.stop()
    
    # Course selection
    selected_course = st.selectbox(
        "Select Course",
        options=[(c.id, c.title) for c in courses],
        format_func=lambda x: x[1]
    )
    
    # Get chapters for selected course
    chapters = db.query(Chapter).filter(Chapter.course_id == selected_course[0]).all()
    
    if not chapters:
        st.info(f"No chapters found for course '{selected_course[1]}'. Please add a chapter first.")
        st.stop()
    
    # Chapter selection
    selected_chapter = st.selectbox(
        "Select Chapter",
        options=[(c.id, c.title) for c in chapters],
        format_func=lambda x: x[1]
    )
    
    # Get selected chapter details
    chapter = db.query(Chapter).filter(Chapter.id == selected_chapter[0]).first()
    course = db.query(Course).filter(Course.id == chapter.course_id).first()
    
    # Display ILOs
    st.subheader("Intended Learning Outcomes (ILOs)")
    if chapter.ilos:
        st.write(chapter.ilos)
    else:
        st.write("No ILOs specified for this chapter.")
    
    # Question input form
    st.subheader("New Question")
    question_type = st.selectbox(
        "Question Type",
        options=["Multiple Choice", "True/False", "Essay", "Short Answer"]
    )
    question_content = st.text_area("Question Content", height=150)
    
    # Analyze button
    if st.button("Analyze Question"):
        if not question_content.strip():
            show_error("Please enter question content.")
        else:
            with st.spinner("Analyzing question with AI... This may take a few moments."):
                try:
                    # Call LLM to analyze question
                    difficulty_rating, improvement_suggestions = llm_utils.analyze_question(
                        question_content=question_content,
                        question_type=question_type,
                        course_title=course.title,
                        chapter_title=chapter.title,
                        ilos=chapter.ilos or "Not specified"
                    )
                    
                    if difficulty_rating is not None:
                        st.subheader("Analysis Results")
                        st.write(f"**AI-Suggested Difficulty Rating:** {difficulty_rating}")
                    
                    # Display improvement suggestions
                    if improvement_suggestions:
                        st.subheader("Improvement Suggestions")
                        st.write(improvement_suggestions)
                    else:
                        st.error("Failed to generate improvement suggestions. Please try again.")
                    
                    # Option to add question with suggested difficulty
                    if difficulty_rating is not None:
                        add_col1, add_col2 = st.columns(2)
                        with add_col1:
                            if st.button("Add Question with Suggested Difficulty"):
                                # Create new question
                                new_question = Question(
                                    chapter_id=chapter.id,
                                    content=question_content,
                                    difficulty=difficulty_rating,
                                    question_type=question_type,
                                    student_level="Intermediate",  # Default value
                                    created_at=datetime.utcnow(),
                                    updated_at=datetime.utcnow()
                                )
                                
                                try:
                                    db.add(new_question)
                                    db.commit()
                                    show_success("Question added successfully with AI-suggested difficulty rating.")
                                    
                                    # Clear form
                                    question_content = ""
                                    st.rerun()
                                except Exception as e:
                                    db.rollback()
                                    show_error(f"Error adding question: {str(e)}")
                        
                        with add_col2:
                            # Add option to modify question based on suggestions before adding
                            if st.button("Edit Question Before Adding"):
                                st.session_state["editing_question_content"] = question_content
                                st.session_state["editing_question_type"] = question_type
                                st.session_state["editing_question_difficulty"] = difficulty_rating
                                st.session_state["editing_question_chapter_id"] = chapter.id
                                st.rerun()
                except Exception as e:
                    st.error(f"Error analyzing question: {str(e)}")
                    logger.error(f"Error analyzing question: {str(e)}")

# If editing a question before adding
if "editing_question_content" in st.session_state:
    st.subheader("Edit Question Before Adding")
    edited_content = st.text_area("Question Content", value=st.session_state["editing_question_content"], height=150)
    edited_type = st.selectbox("Question Type", options=["Multiple Choice", "True/False", "Essay", "Short Answer"], index=["Multiple Choice", "True/False", "Essay", "Short Answer"].index(st.session_state["editing_question_type"]))
    edited_difficulty = st.slider("Difficulty", min_value=1.0, max_value=5.0, value=st.session_state["editing_question_difficulty"], step=0.1)
    
    if st.button("Add Edited Question"):
        # Create new question with edited content
        new_question = Question(
            chapter_id=st.session_state["editing_question_chapter_id"],
            content=edited_content,
            difficulty=edited_difficulty,
            question_type=edited_type,
            student_level="Intermediate",  # Default value
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        try:
            db = next(get_db())
            db.add(new_question)
            db.commit()
            show_success("Question added successfully!")
            
            # Clear session state
            for key in ["editing_question_content", "editing_question_type", "editing_question_difficulty", "editing_question_chapter_id"]:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.rerun()
        except Exception as e:
            db.rollback()
            show_error(f"Error adding question: {str(e)}")
    
    if st.button("Cancel Editing"):
        # Clear session state
        for key in ["editing_question_content", "editing_question_type", "editing_question_difficulty", "editing_question_chapter_id"]:
            if key in st.session_state:
                del st.session_state[key]
        
        st.rerun()

# Add navigation buttons
st.markdown("---")
if st.button("Back to Questions"):
    st.switch_page("pages/view.py") 