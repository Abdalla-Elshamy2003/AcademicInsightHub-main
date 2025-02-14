# import streamlit as st
# from database import get_db
# from models import Question, StudentFeedback
# from utils import show_success, show_error

# st.title("Rate Questions")

# def submit_feedback():
#     db = next(get_db())
#     questions = db.query(Question).all()
    
#     st.write("### Your Information")
#     student_gpa = st.number_input("Your GPA (0.0 - 4.0)", min_value=0.0, max_value=4.0, value=3.0, step=0.1)
#     attendance_rate = st.number_input("Your Attendance Rate (0% - 100%)", min_value=0.0, max_value=100.0, value=90.0, step=5.0) / 100
    
#     st.write("### Rate Questions")
#     st.write("Please rate the difficulty of each question you've attempted.")
    
#     for question in questions:
#         with st.expander(f"Question #{question.id}"):
#             st.write(question.content)
#             st.write(f"Professor's Estimated Difficulty: {question.difficulty}/5.0")
#             st.write(f"Estimated Time: {question.estimated_time} minutes")
            
#             difficulty_rating = st.slider(
#                 "How difficult did you find this question?",
#                 min_value=1.0,
#                 max_value=5.0,
#                 value=3.0,
#                 step=0.5,
#                 key=f"rating_{question.id}"
#             )
            
#             if st.button("Submit Rating", key=f"submit_{question.id}"):
#                 try:
#                     feedback = StudentFeedback(
#                         question_id=question.id,
#                         difficulty_rating=difficulty_rating,
#                         student_gpa=student_gpa,
#                         attendance_rate=attendance_rate
#                     )
#                     db.add(feedback)
#                     db.commit()
#                     show_success("Thank you for your feedback!")
#                 except Exception as e:
#                     show_error(f"Error submitting feedback: {str(e)}")

# submit_feedback()



import streamlit as st
from database import get_db
from models import Question, StudentFeedback
from utils import show_success, show_error

st.title("Rate Questions")

def submit_feedback():
    db = next(get_db())
    questions = db.query(Question).all()
    
    st.write("### Your Information")
    student_gpa = st.number_input("Your GPA (0.0 - 4.0)", min_value=0.0, max_value=4.0, value=3.0, step=0.1)
    attendance_rate = st.number_input("Your Attendance Rate (0% - 100%)", min_value=0.0, max_value=100.0, value=90.0, step=5.0) / 100
    
    st.write("### Rate Questions")
    st.write("Please rate the difficulty of each question you've attempted.")
    
    for question in questions:
        with st.expander(f"Question #{question.id}"):
            st.write(question.content)
            st.write(f"Professor's Estimated Difficulty: {question.difficulty}/5.0")
            st.write(f"Estimated Time: {question.estimated_time} minutes")
            
            difficulty_rating = st.slider(
                "How difficult did you find this question?",
                min_value=1.0,
                max_value=5.0,
                value=3.0,
                step=0.5,
                key=f"rating_{question.id}"
            )
            
            if st.button("Submit Rating", key=f"submit_{question.id}"):
                try:
                    feedback = StudentFeedback(
                        question_id=question.id,
                        difficulty_rating=difficulty_rating,
                        student_gpa=student_gpa,
                        attendance_rate=attendance_rate
                    )
                    db.add(feedback)
                    db.commit()
                    show_success("Thank you for your feedback!")
                except Exception as e:
                    show_error(f"Error submitting feedback: {str(e)}")

submit_feedback()
