import pandas as pd
import random
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#  Cleaning code 
def connection_and_retrieval_of_database_info():
    """
        purpose of method is to create a connection 
        to the database
    """
    engine = create_engine('sqlite:///HouseHold_data.db')  
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine


engine = connection_and_retrieval_of_database_info()

df = pd.read_sql('SELECT * FROM households', engine)

random_applicants = df.sample(n=130, random_state=42)  

random_applicants['loan_amount_requested'] = [random.uniform(10000, 100000) for _ in range(len(random_applicants))]

random_applicants['loan_repayment_period'] = [random.randint(12, 60) for _ in range(len(random_applicants))]

if 'disposable_income' not in random_applicants.columns or 'debt_to_income_ratio' not in random_applicants.columns:
    raise ValueError("Required fields 'disposable_income' and 'debt_to_income_ratio' are missing in the database.")


"""
             **** TOP FIXES **** 

  1. We need to identify exactly why some high income status people still get rejected for loans
     even when they meet requirements           




     Let us think about factors affecting the process of getting loan approved

     1. credit_score
     2. disposable_income 
     3. loan_amount_requested
     4. debt_to_income_ratio
     

    KEY : 
    months_to_pay, m_t_p
    loan_amount_requested, l_a_r


    if loan_amount greater than 50000 to 100000 && credit_Score >=680 && debt_to_income_ratio < 0.5:
       return approved, months_to_pay, how_much_to_pay_back_p/m = l_a_r/m_t_p, full_name
    elif loan_amount greater than 10000 to 50000 && credit_score <=550 && debt_to_income_ratio < 0.6:
        return approved, months_to_pay, how_much_to_pay_back_p/m = l_a_r/m_t_p, full_name
    elif loan_amount greater than 5000 but less than 10000 and credt_score >= 500 and debt_to_income_ratio < 0.4
        return conditionally approved, months_to_pay, how_much_to_pay_back_p/m = l_a_r/m_t_p, full_name
    else:
        return rejected, 0, 0, full_name

"""

STARTING_AMOUNT=50000
HIGHEST_AMOUNT = 100000
tenK = 10000
FiveK = 5000

def new_loan_approval_method(row):
    if STARTING_AMOUNT < row['loan_amount_requested'] < HIGHEST_AMOUNT and row['credit_score'] >= 680 and row['debt_to_income_ratio'] < 0.5:
        return 'Approved',12, row['loan_amount_requested'] / 12, row['full_name']
    elif tenK < row['loan_amount_requested'] <=STARTING_AMOUNT and row['credit_score'] >=550 and row['debt_to_income_ratio'] < 0.6:
        return 'Approved', 18, row['loan_amount_requested']/ 18, row['full_name']
    elif FiveK < row['loan_amount_requested'] < tenK and row['credit_score'] >= 500 and row['debt_to_income_ratio'] < 0.4:
        return 'Conditionally Approved',24, row['loan_amount_requested']/24, row['full_name']
    elif row['disposable_income'] >= (tenK) and row['credit_score'] >= 500 and row['debt_to_income_ratio'] < 0.7:
        return 'Conditionally Accepted', 48, row['loan_amount_requested']/48, row['full_name']
    else:
        return 'Rejected', 0, 0, row['full_name']


# def loan_approval(row):
#     if row['credit_score'] >= 650 and row['debt_to_income_ratio'] < 0.7 and row['disposable_income'] > 10000:
#         return 'Approved', 24, row['loan_amount_requested'] / 24, row['full_name']
#     elif row['credit_score'] >= 500 and row['debt_to_income_ratio'] < 0.5 and row['disposable_income'] > 3000:
#         return 'Conditionally Approved', 12, row['loan_amount_requested'] / 12, row['full_name']
#     else:
#         return 'Rejected', 0, 0, row['full_name']






random_applicants['loan_approval_status'], random_applicants['loan_repayment_period'], random_applicants['monthly_repayment'], random_applicants['full_name'] = zip(*random_applicants.apply(new_loan_approval_method, axis=1))

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
