# # import streamlit as st
# # from database import get_db
# # from models import Course, Chapter
# # from utils import show_success, show_error, format_ilos

# # st.title("Chapter Management")

# # def create_chapter():
# #     db = next(get_db())
# #     courses = db.query(Course).all()
    
# #     with st.form("chapter_form"):
# #         course_id = st.selectbox(
# #             "Select Course",
# #             options=[(c.id, c.title) for c in courses],
# #             format_func=lambda x: x[1]
# #         )
        
# #         title = st.text_input("Chapter Title")
# #         summary = st.text_area("Chapter Summary")
# #         ilos = st.text_area("Intended Learning Outcomes (One per line)")
        
# #         submit = st.form_submit_button("Create Chapter")
        
# #         if submit and title and course_id:
# #             try:
# #                 new_chapter = Chapter(
# #                     course_id=course_id[0],
# #                     title=title,
# #                     summary=summary,
# #                     ilos=ilos
# #                 )
# #                 db.add(new_chapter)
# #                 db.commit()
# #                 show_success("Chapter created successfully!")
# #             except Exception as e:
# #                 show_error(f"Error creating chapter: {str(e)}")

# # def list_chapters():
# #     db = next(get_db())
# #     courses = db.query(Course).all()
    
# #     selected_course = st.selectbox(
# #         "Filter by Course",
# #         options=[(0, "All Courses")] + [(c.id, c.title) for c in courses],
# #         format_func=lambda x: x[1]
# #     )
    
# #     query = db.query(Chapter)
# #     if selected_course[0] != 0:
# #         query = query.filter(Chapter.course_id == selected_course[0])
    
# #     chapters = query.all()
    
# #     for chapter in chapters:
# #         with st.expander(f"📖 {chapter.title}"):
# #             st.write("**Summary:**")
# #             st.write(chapter.summary)
            
# #             st.write("**Learning Outcomes:**")
# #             for ilo in format_ilos(chapter.ilos):
# #                 st.write(f"- {ilo}")
            
# #             col1, col2 = st.columns(2)
# #             with col1:
# #                 if st.button(f"Edit {chapter.title}", key=f"edit_{chapter.id}"):
# #                     st.session_state["editing_chapter"] = chapter.id
# #             with col2:
# #                 if st.button(f"Delete {chapter.title}", key=f"delete_{chapter.id}"):
# #                     db.delete(chapter)
# #                     db.commit()
# #                     st.experimental_rerun()

# # # Page layout
# # col1, col2 = st.columns([2, 1])

# # with col1:
# #     st.subheader("Chapter List")
# #     list_chapters()

# # with col2:
# #     st.subheader("Add New Chapter")
# #     create_chapter()



# import streamlit as st
# from database import get_db
# from models import Course, Chapter
# from utils import show_success, show_error, format_ilos

# st.title("Chapter Management")

# def create_chapter():
#     db = next(get_db())
#     courses = db.query(Course).all()
    
#     with st.form("chapter_form"):
#         course_id = st.selectbox(
#             "Select Course",
#             options=[(c.id, c.title) for c in courses],
#             format_func=lambda x: x[1]
#         )
        
#         title = st.text_input("Chapter Title")
#         summary = st.text_area("Chapter Summary")
#         ilos = st.text_area("Intended Learning Outcomes (One per line)")
        
#         submit = st.form_submit_button("Create Chapter")
        
#         if submit and title and course_id:
#             try:
#                 new_chapter = Chapter(
#                     course_id=course_id[0],
#                     title=title,
#                     summary=summary,
#                     ilos=ilos
#                 )
#                 db.add(new_chapter)
#                 db.commit()
#                 show_success("Chapter created successfully!")
#             except Exception as e:
#                 show_error(f"Error creating chapter: {str(e)}")

# def list_chapters():
#     db = next(get_db())
#     courses = db.query(Course).all()
    
#     selected_course = st.selectbox(
#         "Filter by Course",
#         options=[(0, "All Courses")] + [(c.id, c.title) for c in courses],
#         format_func=lambda x: x[1]
#     )
    
#     query = db.query(Chapter)
#     if selected_course[0] != 0:
#         query = query.filter(Chapter.course_id == selected_course[0])
    
#     chapters = query.all()
    
#     for chapter in chapters:
#         with st.expander(f"📖 {chapter.title}"):
#             st.write("**Summary:**")
#             st.write(chapter.summary)
            
#             st.write("**Learning Outcomes:**")
#             for ilo in format_ilos(chapter.ilos):
#                 st.write(f"- {ilo}")
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button(f"Edit {chapter.title}", key=f"edit_{chapter.id}"):
#                     st.session_state["editing_chapter"] = chapter.id
#             with col2:
#                 if st.button(f"Delete {chapter.title}", key=f"delete_{chapter.id}"):
#                     db.delete(chapter)
#                     db.commit()
#                     st.experimental_rerun()

# # Page layout
# col1, col2 = st.columns([2, 1])

# with col1:
#     st.subheader("Chapter List")
#     list_chapters()

# with col2:
#     st.subheader("Add New Chapter")
#     create_chapter()
