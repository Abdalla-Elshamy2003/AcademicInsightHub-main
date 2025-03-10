# import streamlit as st
# import pandas as pd
# from database import get_db
# from models import Question, StudentFeedback
# from utils import create_difficulty_chart, create_gpa_correlation_chart

# st.title("Analytics Dashboard")

# def load_analytics_data():
#     db = next(get_db())
    
#     # Question difficulty distribution
#     questions = pd.read_sql(
#         db.query(Question).statement,
#         db.bind
#     )
    
#     # Student feedback analysis
#     feedback = pd.read_sql(
#         db.query(StudentFeedback).statement,
#         db.bind
#     )
    
#     return questions, feedback

# def show_analytics():
#     questions, feedback = load_analytics_data()
    
#     # Question Statistics
#     st.subheader("Question Statistics")
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.metric("Total Questions", len(questions))
#     with col2:
#         st.metric("Average Difficulty", f"{questions['difficulty'].mean():.2f}")
#     with col3:
#         st.metric("Average Time", f"{questions['estimated_time'].mean():.0f} min")
    
#     # Difficulty Distribution
#     st.subheader("Question Difficulty Distribution")
#     st.plotly_chart(create_difficulty_chart(questions), use_container_width=True)
    
#     # Student Performance
#     if not feedback.empty:
#         st.subheader("Student Performance Analysis")
#         st.plotly_chart(create_gpa_correlation_chart(feedback), use_container_width=True)
        
#         # Performance Metrics
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Average Student GPA", f"{feedback['student_gpa'].mean():.2f}")
#         with col2:
#             st.metric("Average Attendance Rate", f"{feedback['attendance_rate'].mean():.1%}")

# show_analytics()
import streamlit as st
import pandas as pd
from database import get_db
from models import Question, StudentFeedback, StudentProgress, Course, Chapter
from sqlalchemy import func
from utils import create_difficulty_chart, create_gpa_correlation_chart, cache_data
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@cache_data(ttl_seconds=300)
def get_analytics_data():
    """Get analytics data from the database with caching."""
    db = next(get_db())
    
    # Get question difficulty data
    difficulty_data = db.query(
        Question.difficulty,
        func.count(Question.id).label('count')
    ).group_by(Question.difficulty).all()
    
    # Get student feedback data
    feedback_data = db.query(
        StudentFeedback.difficulty_rating,
        StudentFeedback.student_gpa,
        Question.difficulty
    ).join(Question).all()
    
    # Get student progress data
    progress_data = db.query(
        StudentProgress.correct,
        func.count(StudentProgress.id).label('count')
    ).group_by(StudentProgress.correct).all()
    
    # Get course and chapter counts
    course_count = db.query(func.count(Course.id)).scalar()
    chapter_count = db.query(func.count(Chapter.id)).scalar()
    question_count = db.query(func.count(Question.id)).scalar()
    
    # Get average difficulty by course
    course_difficulty = db.query(
        Course.title,
        func.avg(Question.difficulty).label('avg_difficulty')
    ).join(Chapter).join(Question).group_by(Course.id).all()
    
    return {
        'difficulty_data': difficulty_data,
        'feedback_data': feedback_data,
        'progress_data': progress_data,
        'course_count': course_count,
        'chapter_count': chapter_count,
        'question_count': question_count,
        'course_difficulty': course_difficulty
    }

def show_analytics():
    """Display the analytics dashboard."""
    st.markdown("## Analytics Dashboard")
    
    try:
        # Get data
        data = get_analytics_data()
        
        # Display summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Courses", data['course_count'])
        with col2:
            st.metric("Total Chapters", data['chapter_count'])
        with col3:
            st.metric("Total Questions", data['question_count'])
        
        # Create difficulty distribution chart
        st.markdown("### Question Difficulty Distribution")
        if data['difficulty_data']:
            df_difficulty = pd.DataFrame(data['difficulty_data'], columns=['difficulty', 'count'])
            chart = create_difficulty_chart(df_difficulty)
            st.plotly_chart(chart, use_container_width=True)
        else:
            st.info("No question difficulty data available.")
        
        # Create GPA correlation chart
        st.markdown("### Student GPA vs. Perceived Difficulty")
        if data['feedback_data']:
            df_gpa = pd.DataFrame(data['feedback_data'], columns=['perceived_difficulty', 'student_gpa', 'actual_difficulty'])
            chart = create_gpa_correlation_chart(df_gpa)
            st.plotly_chart(chart, use_container_width=True)
        else:
            st.info("No student feedback data available.")
        
        # Create success rate chart
        st.markdown("### Student Success Rate")
        if data['progress_data']:
            success_data = {row[0]: row[1] for row in data['progress_data']}
            correct = success_data.get(True, 0)
            incorrect = success_data.get(False, 0)
            total = correct + incorrect
            
            if total > 0:
                success_rate = (correct / total) * 100
                st.progress(success_rate / 100)
                st.write(f"Success Rate: {success_rate:.1f}%")
            else:
                st.info("No student progress data available.")
        else:
            st.info("No student progress data available.")
        
        # Course difficulty comparison
        st.markdown("### Average Difficulty by Course")
        if data['course_difficulty']:
            df_course = pd.DataFrame(data['course_difficulty'], columns=['course', 'avg_difficulty'])
            df_course = df_course.sort_values('avg_difficulty', ascending=False)
            
            # Create a bar chart
            import plotly.express as px
            fig = px.bar(
                df_course, 
                x='course', 
                y='avg_difficulty',
                title='Average Question Difficulty by Course',
                labels={'course': 'Course', 'avg_difficulty': 'Average Difficulty'},
                color='avg_difficulty',
                color_continuous_scale='RdYlGn_r'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No course difficulty data available.")
            
    except Exception as e:
        logger.error(f"Error displaying analytics: {str(e)}")
        st.error(f"Error loading analytics data: {str(e)}")

# For backward compatibility - this will be called when the file is run directly
if __name__ == "__main__":
    st.title("Analytics Dashboard")
    show_analytics()
