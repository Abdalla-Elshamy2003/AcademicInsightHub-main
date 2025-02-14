# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import os
# from sqlalchemy import create_engine
# # Create SQLAlchemy engine
# engine = create_engine('sqlite:///abdalla.db')
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Create SQLAlchemy engine
engine = create_engine('sqlite:///abdalla.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
