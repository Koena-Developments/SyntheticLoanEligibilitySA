import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('transformed_financial_data.csv')

def calculate_emi(principal, rate, months):
    try:
        r = rate / 12 
        emi = (principal * r * (1 + r)**months) / ((1 + r)**months - 1)
        return emi
    except ZeroDivisionError:
        return 0

df['emi'] = df.apply(
    lambda row: calculate_emi(
        row['loan_amount_requested'],
        rate=0.08,  
        months=row['loan_repayment_months']
    ),
    axis=1
)

def determine_loan_status(row):
    if row['credit_score'] > 650 and row['debt_to_income_ratio'] < 0.3:
        return "Accept"
    elif 500 <= row['credit_score'] <= 650 or 0.3 <= row['debt_to_income_ratio'] <= 0.5:
        return "Conditional Accept"
    else:
        return "Reject"

df['loan_status'] = df.apply(determine_loan_status, axis=1)

df['adjusted_months'] = df.apply(
    lambda row: row['loan_amount_requested'] / row['disposable_income'] if row['disposable_income'] > 0 else 'rejected',
    axis=1
)

def process_months(value):
    if isinstance(value, (int, float)):
        if value < 1:
            days = round(value * 30)
            return f"{days} days"
        else:
            months = round(value)
            return f"{months} months"
    return value

df['adjusted_months'] = df['adjusted_months'].apply(process_months)

print("Full DataFrame (Preview):")
print(df.head())

approved_df = df[
    (df['loan_status'].isin(['Accept', 'Conditional Accept'])) &
    (df['adjusted_months'] != 'rejected')
]

print("\nFiltered DataFrame (Preview):")
print(approved_df.head())

engine = create_engine('sqlite:///approved_loans.db')

approved_df.to_sql('approved_applicants', con=engine, if_exists='replace', index=False)

print("\nApproved applicants without 'rejected' adjusted_months have been saved to 'approved_loans.db'.")
