# # import streamlit as st
# # from database import get_db
# # from models import Course
# # from utils import show_success, show_error

# # st.title("Course Management")

# # def create_course():
# #     with st.form("course_form"):
# #         title = st.text_input("Course Title")
# #         description = st.text_area("Course Description")
# #         submit = st.form_submit_button("Create Course")
        
# #         if submit and title:
# #             try:
# #                 db = next(get_db())
# #                 new_course = Course(title=title, description=description)
# #                 db.add(new_course)
# #                 db.commit()
# #                 show_success("Course created successfully!")
# #             except Exception as e:
# #                 show_error(f"Error creating course: {str(e)}")

# # def list_courses():
# #     db = next(get_db())
# #     courses = db.query(Course).all()
    
# #     for course in courses:
# #         with st.expander(f"📚 {course.title}"):
# #             st.write(course.description)
            
# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 if st.button(f"Edit {course.title}", key=f"edit_{course.id}"):
# #                     st.session_state["editing_course"] = course.id
# #             with col2:
# #                 if st.button(f"Delete {course.title}", key=f"delete_{course.id}"):
# #                     db.delete(course)
# #                     db.commit()
# #                     st.experimental_rerun()

# # # Page layout
# # col1, col2 = st.columns([2, 1])

# # with col1:
# #     st.subheader("Course List")
# #     list_courses()

# # with col2:
# #     st.subheader("Add New Course")
# #     create_course()


# import streamlit as st
# from database import get_db
# from models import Course
# from utils import show_success, show_error

# st.title("Course Management")

# def create_course():
#     with st.form("course_form"):
#         title = st.text_input("Course Title")
#         description = st.text_area("Course Description")
#         submit = st.form_submit_button("Create Course")
        
#         if submit and title:
#             try:
#                 db = next(get_db())
#                 new_course = Course(title=title, description=description)
#                 db.add(new_course)
#                 db.commit()
#                 show_success("Course created successfully!")
#             except Exception as e:
#                 show_error(f"Error creating course: {str(e)}")

# def list_courses():
#     db = next(get_db())
#     courses = db.query(Course).all()
    
#     for course in courses:
#         with st.expander(f"📚 {course.title}"):
#             st.write(course.description)
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button(f"Edit {course.title}", key=f"edit_{course.id}"):
#                     st.session_state["editing_course"] = course.id
#             with col2:
#                 if st.button(f"Delete {course.title}", key=f"delete_{course.id}"):
#                     db.delete(course)
#                     db.commit()
#                     st.experimental_rerun()

# # Page layout
# col1, col2 = st.columns([2, 1])

# with col1:
#     st.subheader("Course List")
#     list_courses()

# with col2:
#     st.subheader("Add New Course")
#     create_course()
