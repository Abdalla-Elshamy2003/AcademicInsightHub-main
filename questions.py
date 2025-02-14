# # import streamlit as st
# # from database import get_db
# # from models import Chapter, Question
# # from utils import show_success, show_error

# # st.title("Question Bank")

# # def create_question():
# #     db = next(get_db())
# #     chapters = db.query(Chapter).all()
    
# #     with st.form("question_form"):
# #         chapter_id = st.selectbox(
# #             "Select Chapter",
# #             options=[(c.id, f"{c.course.title} - {c.title}") for c in chapters],
# #             format_func=lambda x: x[1]
# #         )
        
# #         content = st.text_area("Question Content")
# #         difficulty = st.slider("Difficulty Level", 1.0, 5.0, 3.0, 0.5)
# #         estimated_time = st.number_input("Estimated Time (minutes)", min_value=1, value=5)
# #         student_level = st.selectbox(
# #             "Student Level",
# #             ["Beginner", "Intermediate", "Advanced"]
# #         )
        
# #         submit = st.form_submit_button("Create Question")
        
# #         if submit and content and chapter_id:
# #             try:
# #                 new_question = Question(
# #                     chapter_id=chapter_id[0],
# #                     content=content,
# #                     difficulty=difficulty,
# #                     estimated_time=estimated_time,
# #                     student_level=student_level
# #                 )
# #                 db.add(new_question)
# #                 db.commit()
# #                 show_success("Question created successfully!")
# #             except Exception as e:
# #                 show_error(f"Error creating question: {str(e)}")

# # def list_questions():
# #     db = next(get_db())
# #     chapters = db.query(Chapter).all()
    
# #     filters = st.columns(3)
# #     with filters[0]:
# #         selected_chapter = st.selectbox(
# #             "Filter by Chapter",
# #             options=[(0, "All Chapters")] + [(c.id, f"{c.course.title} - {c.title}") for c in chapters],
# #             format_func=lambda x: x[1]
# #         )
    
# #     with filters[1]:
# #         difficulty_filter = st.slider(
# #             "Filter by Difficulty",
# #             1.0, 5.0, (1.0, 5.0), 0.5
# #         )
    
# #     with filters[2]:
# #         level_filter = st.multiselect(
# #             "Filter by Student Level",
# #             ["Beginner", "Intermediate", "Advanced"]
# #         )
    
# #     query = db.query(Question)
# #     if selected_chapter[0] != 0:
# #         query = query.filter(Question.chapter_id == selected_chapter[0])
    
# #     query = query.filter(Question.difficulty.between(difficulty_filter[0], difficulty_filter[1]))
    
# #     if level_filter:
# #         query = query.filter(Question.student_level.in_(level_filter))
    
# #     questions = query.all()
    
# #     for question in questions:
# #         with st.expander(f"❓ Question (Difficulty: {question.difficulty})"):
# #             st.write(question.content)
# #             st.write(f"**Estimated Time:** {question.estimated_time} minutes")
# #             st.write(f"**Student Level:** {question.student_level}")
            
# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 if st.button(f"Edit Question", key=f"edit_{question.id}"):
# #                     st.session_state["editing_question"] = question.id
# #             with col2:
# #                 if st.button(f"Delete Question", key=f"delete_{question.id}"):
# #                     db.delete(question)
# #                     db.commit()
# #                     st.experimental_rerun()

# # # Page layout
# # col1, col2 = st.columns([2, 1])

# # with col1:
# #     st.subheader("Question List")
# #     list_questions()

# # with col2:
# #     st.subheader("Add New Question")
# #     create_question()


# import streamlit as st
# from database import get_db
# from models import Chapter, Question
# from utils import show_success, show_error

# st.title("Question Bank")

# def create_question():
#     db = next(get_db())
#     chapters = db.query(Chapter).all()
    
#     with st.form("question_form"):
#         chapter_id = st.selectbox(
#             "Select Chapter",
#             options=[(c.id, f"{c.course.title} - {c.title}") for c in chapters],
#             format_func=lambda x: x[1]
#         )
        
#         content = st.text_area("Question Content")
#         difficulty = st.slider("Difficulty Level", 1.0, 5.0, 3.0, 0.5)
#         estimated_time = st.number_input("Estimated Time (minutes)", min_value=1, value=5)
#         student_level = st.selectbox(
#             "Student Level",
#             ["Beginner", "Intermediate", "Advanced"]
#         )
        
#         submit = st.form_submit_button("Create Question")
        
#         if submit and content and chapter_id:
#             try:
#                 new_question = Question(
#                     chapter_id=chapter_id[0],
#                     content=content,
#                     difficulty=difficulty,
#                     estimated_time=estimated_time,
#                     student_level=student_level
#                 )
#                 db.add(new_question)
#                 db.commit()
#                 show_success("Question created successfully!")
#             except Exception as e:
#                 show_error(f"Error creating question: {str(e)}")

# def list_questions():
#     db = next(get_db())
#     chapters = db.query(Chapter).all()
    
#     filters = st.columns(3)
#     with filters[0]:
#         selected_chapter = st.selectbox(
#             "Filter by Chapter",
#             options=[(0, "All Chapters")] + [(c.id, f"{c.course.title} - {c.title}") for c in chapters],
#             format_func=lambda x: x[1]
#         )
    
#     with filters[1]:
#         difficulty_filter = st.slider(
#             "Filter by Difficulty",
#             1.0, 5.0, (1.0, 5.0), 0.5
#         )
    
#     with filters[2]:
#         level_filter = st.multiselect(
#             "Filter by Student Level",
#             ["Beginner", "Intermediate", "Advanced"]
#         )
    
#     query = db.query(Question)
#     if selected_chapter[0] != 0:
#         query = query.filter(Question.chapter_id == selected_chapter[0])
    
#     query = query.filter(Question.difficulty.between(difficulty_filter[0], difficulty_filter[1]))
    
#     if level_filter:
#         query = query.filter(Question.student_level.in_(level_filter))
    
#     questions = query.all()
    
#     for question in questions:
#         with st.expander(f"❓ Question (Difficulty: {question.difficulty})"):
#             st.write(question.content)
#             st.write(f"**Estimated Time:** {question.estimated_time} minutes")
#             st.write(f"**Student Level:** {question.student_level}")
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button(f"Edit Question", key=f"edit_{question.id}"):
#                     st.session_state["editing_question"] = question.id
#             with col2:
#                 if st.button(f"Delete Question", key=f"delete_{question.id}"):
#                     db.delete(question)
#                     db.commit()
#                     st.experimental_rerun()

# # Page layout
# col1, col2 = st.columns([2, 1])

# with col1:
#     st.subheader("Question List")
#     list_questions()

# with col2:
#     st.subheader("Add New Question")
#     create_question()
