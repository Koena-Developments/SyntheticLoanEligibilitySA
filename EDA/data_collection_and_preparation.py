import pandas as pd
import random
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///HouseHold_data.db')  
Session = sessionmaker(bind=engine)
session = Session()

df = pd.read_sql('SELECT * FROM households', engine)

random_applicants = df.sample(n=130, random_state=42)  

random_applicants['loan_amount_requested'] = [random.uniform(10000, 100000) for _ in range(len(random_applicants))]

random_applicants['loan_repayment_period'] = [random.randint(12, 60) for _ in range(len(random_applicants))]

if 'disposable_income' not in random_applicants.columns or 'debt_to_income_ratio' not in random_applicants.columns:
    raise ValueError("Required fields 'disposable_income' and 'debt_to_income_ratio' are missing in the database.")


def loan_approval(row):
    if row['credit_score'] >= 650 and row['debt_to_income_ratio'] < 0.7 and row['disposable_income'] > 10000:
        return 'Approved', 12, row['loan_amount_requested'] / 12, row['full_name']
    elif row['credit_score'] >= 500 and row['debt_to_income_ratio'] < 0.4 and row['disposable_income'] > 3000:
        return 'Conditionally Approved', 24, row['loan_amount_requested'] / 24, row['full_name']
    else:
        return 'Rejected', 0, 0, row['full_name']

random_applicants['loan_approval_status'], random_applicants['loan_repayment_period'], random_applicants['monthly_repayment'], random_applicants['full_name'] = zip(*random_applicants.apply(loan_approval, axis=1))

loan_engine = create_engine('sqlite:///loan_applicants.db')  

Base = declarative_base()

class LoanApplicant(Base):
    __tablename__ = 'loan_applicants'
    
    id = Column(Integer, primary_key=True)
    household_id = Column(Integer)
    full_name = Column(String)
    loan_approval_status = Column(String)
    loan_repayment_period = Column(Integer)
    monthly_repayment = Column(Float)
    credit_score=Column(Integer)
    disposable_income = Column(Float)
    debt_to_income_ratio = Column(Float)
    loan_amount_requested = Column(Float)
    

Base.metadata.create_all(loan_engine)  

LoanApplicantSession = sessionmaker(bind=loan_engine)
loan_applicant_session = LoanApplicantSession()

for _, row in random_applicants.iterrows():
    loan_applicant = LoanApplicant(
        household_id=row['household_id'],
        full_name = row['full_name'],
        loan_approval_status=row['loan_approval_status'],
        loan_repayment_period=row['loan_repayment_period'],
        monthly_repayment=row['monthly_repayment'],
        credit_score=row['credit_score'],
        disposable_income=row['disposable_income'],
        debt_to_income_ratio=row['debt_to_income_ratio'],
        loan_amount_requested=row['loan_amount_requested']
    )
    loan_applicant_session.add(loan_applicant)


loan_applicant_session.commit() 
loan_applicant_session.close()

print(f"Loan applicants' results have been successfully stored in the 'loan_applicants.db' database.")
