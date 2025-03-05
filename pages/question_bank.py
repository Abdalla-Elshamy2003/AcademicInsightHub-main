import streamlit as st
import pandas as pd
from database import get_db
from models import Question

def question_bank_page():
    st.title("Question Bank Management")
    
    # Export functionality
    if st.button("Export Questions"):
        db = next(get_db())
        questions = db.query(Question).all()
        
        df = pd.DataFrame([{
            'content': q.content,
            'difficulty': q.difficulty,
            'estimated_time': q.estimated_time,
            'student_level': q.student_level
        } for q in questions])
        
        csv = df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            csv,
            "questions.csv",
            "text/csv",
            key='download-csv'
        )
    
    # Import functionality
    uploaded_file = st.file_uploader("Import Questions", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if st.button("Import Questions"):
            db = next(get_db())
            for _, row in df.iterrows():
                question = Question(**row.to_dict())
                db.add(question)
            db.commit()
            st.success("Questions imported successfully!")