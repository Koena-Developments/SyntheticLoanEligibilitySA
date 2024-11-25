from faker import Faker
import pandas as pd
import random

first_names = [
    'Thabo', 'Sipho', 'Nokuthula', 'Nomvula', 'Jacob', 'Nelson', 
    'Pieter', 'Johannes', 'Elize', 'Leanne', 'Abongile', 'Zanele'
]

last_names = [
    'Dlamini', 'Mokoena', 'Nkosi', 'Botha', 'van der Merwe', 
    'Zulu', 'Naidoo', 'Pillay', 'Mahlangu', 'Masuku', 'Sithole'
]
fake = Faker('en')
south_african_cities = ['Johannesburg', 'Cape Town', 'Durban', 'Pretoria', 'Port Elizabeth', 'Bloemfontein', 'Polokwane']

def generate_sa_id():
    birth_date = f"{random.randint(79, 99):02}{random.randint(1, 12):02}{random.randint(1, 31):02}"
    random_digits = f"{random.randint(0, 9999):04}"
    citizenship = random.choice(['0', '1'])
    gender = random.choice(['0', '1'])
    return f"{birth_date}{random_digits}{citizenship}{gender}"

def generate_sa_phone_number():
    return f"+27 {random.randint(100000000, 999999999)}"

def generate_sa_name():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name} {last_name}"

def generate_sa_address():
    return f"{random.choice(south_african_cities)}, South Africa"


# need to change the fact that the loan_repayment_months are randomly generated, it should depend the amount of the loan and the amount that the loan_requester wants to pay 
#  consider 
def generate_data():
    """
    Generates synthetic financial data and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the generated data.
    """
    data = [
        {
            'household_id': i,
            'full_name': generate_sa_name(),
            'age': random.randint(20, 60),
            'gender': random.choice(['Male', 'Female']),
            'location': random.choice(['Urban', 'Rural']),
            'address': generate_sa_address(),
            'industry': random.choice(['Government', 'Mining', 'Private']),
            'income': random.randint(3000, 50000),
            'expenses': random.randint(2000, 40000),
            'job_status': 'Formally Employed',
            'credit_score': random.randint(300, 850),
            'loan_amount_requested': random.randint(1000, 50000),
            'loan_repayment_months': random.choice([6, 12, 24, 36]),
            'sa_id': generate_sa_id(),
            'phone_number': generate_sa_phone_number()
        }
        for i in range(1, 1001)
    ]
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_data()

    df = df.drop_duplicates(subset='full_name')

    df.to_csv("synthetic_financial_data.csv", index=False)
    print("Synthetic financial data with unique names saved to 'synthetic_financial_data.csv'.")
