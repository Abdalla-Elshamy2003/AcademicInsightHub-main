from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # In production, store hashed passwords

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    chapters = relationship("Chapter", back_populates="course")

class Chapter(Base):
    __tablename__ = "chapters"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String(100), nullable=False)
    summary = Column(Text)
    ilos = Column(Text)  # Intended Learning Outcomes
    
    course = relationship("Course", back_populates="chapters")
    questions = relationship("Question", back_populates="chapter")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    content = Column(Text, nullable=False)
    difficulty = Column(Float)  # 1-5 scale
    estimated_time = Column(Integer)  # in minutes
    student_level = Column(String(20))  # Beginner, Intermediate, Advanced
    
    chapter = relationship("Chapter", back_populates="questions")
    feedback = relationship("StudentFeedback", back_populates="question")

class StudentFeedback(Base):
    __tablename__ = "student_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    difficulty_rating = Column(Float)
    student_gpa = Column(Float)
    attendance_rate = Column(Float)
    
    question = relationship("Question", back_populates="feedback")
