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
    job_status = Column(String)
    credit_score = Column(Integer)
    loan_amount_requested = Column(Integer)
    loan_repayment_months = Column(Integer)
    sa_id = Column(String)
    phone_number = Column(String)

class AnalysisResult(Base):
    __tablename__ = 'analysis_results'
    
    id = Column(Integer, primary_key=True)
    household_id = Column(Integer)
    disposable_income = Column(Integer)
    debt_to_income_ratio = Column(Float)

engine = create_engine('sqlite:///HouseHold_data.db', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def load_data(df):
    for index, row in df.iterrows():
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
            job_status=row['job_status'],
            credit_score=row['credit_score'],
            loan_amount_requested=row['loan_amount_requested'],
            loan_repayment_months=row['loan_repayment_months'],
            sa_id=row['sa_id'],
            phone_number=row['phone_number']
        )
        session.add(household)

    session.commit()

    for index, row in df.iterrows():
        disposable_income = row['income'] - row['expenses']
        debt_to_income_ratio = row['loan_amount_requested'] / row['income'] if row['income'] != 0 else 0
        
        analysis_result = AnalysisResult(
            household_id=row['household_id'],
            disposable_income=disposable_income,
            debt_to_income_ratio=debt_to_income_ratio
        )
        session.add(analysis_result)

    session.commit()

df = pd.read_csv('synthetic_financial_data.csv')  
load_data(df)

session.close()
