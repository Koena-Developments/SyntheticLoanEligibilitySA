from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()

class Household(Base):
    __tablename__ = 'households'
    
    id = Column(Integer, primary_key=True)
    household_id = Column(Integer, unique=True)
    full_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    location = Column(String)
    address = Column(String)
    industry = Column(String)
    income = Column(Integer)
    expenses = Column(Integer)
    disposable_income = Column(Integer)
    debt_to_income_ratio = Column(Float)
    job_status = Column(String)
    credit_score = Column(Integer)
    sa_id = Column(String)
    phone_number = Column(String)
    
engine = create_engine('sqlite:///HouseHold_data.db', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def load_data(df):
    for _, row in df.iterrows():
        household = Household(
            household_id=row['household_id'],
            full_name=row['full_name'],
            age=row['age'],
            gender=row['gender'],
            location=row['location'],
            address=row['address'],
            industry=row['industry'],
            income=row['income'],
            expenses=row['expenses'],
            disposable_income=row['disposable_income'],
            debt_to_income_ratio=row['debt_to_income_ratio'],
            job_status=row['job_status'],
            credit_score=row['credit_score'],
            sa_id=row['sa_id'],
            phone_number=row['phone_number']
        )
        session.add(household)


    session.commit()

if __name__ == "__main__":
    df = pd.read_csv('transformed_financial_data.csv')
    load_data(df)
    session.close()
    print("Data loaded successfully into the database.")
