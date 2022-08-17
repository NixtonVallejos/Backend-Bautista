from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'postgres://cyzrzhxcvsprnn:b5ae4ea01fc60c83cb4b70b13fbce3e8578487487875089db579826039ac4a9e@ec2-54-86-224-85.compute-1.amazonaws.com:5432/d5o0p1ftaajhvh'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()