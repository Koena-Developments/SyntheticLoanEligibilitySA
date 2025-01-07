import pandas as pd
from Extract import generate_data
import numpy as np 

def clean_data(df):
    """
    Cleans the input DataFrame by handling missing values, outliers,
    and dropping duplicate names.

    Parameters:
        df (pd.DataFrame): Input DataFrame to clean.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = df.drop_duplicates(subset=['full_name'], keep='first')

    for col in ['income', 'expenses', 'credit_score']:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())

    for col in ['gender', 'location', 'industry', 'job_status']:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mode()[0])

    df['income'] = df['income'].apply(lambda x: min(x, 50000))
    df['expenses'] = df['expenses'].apply(lambda x: min(x, 10000))
    df['credit_score'] = df['credit_score'].apply(lambda x: min(max(x, 300), 850))

    return df


def add_calculated_fields(df):
    """
    Adds calculated fields such as disposable income and debt-to-income ratio.

    Parameters:
        df (pd.DataFrame): Input DataFrame with cleaned data.

    Returns:
        pd.DataFrame: DataFrame with additional calculated fields.
    """
    df['disposable_income'] = df['income'] - df['expenses']

    df['debt_to_income_ratio'] = df.apply(
        lambda row: row['expenses'] / row['income'] if row['income'] > 0 else float('inf'),
        axis=1
    )

    return df


def transform_data(df):
    """
    Transforms the data by cleaning it and adding calculated fields.

    Args:
        df (pd.DataFrame): The raw data DataFrame.

    Returns:
        pd.DataFrame: The transformed data.
    """
    df = clean_data(df)
    df = add_calculated_fields(df)

    return df


if __name__ == "__main__":
    df = pd.read_csv("synthetic_financial_data.csv")
    
    transformed_df = transform_data(df)
    
    transformed_df.to_csv("transformed_financial_data.csv", index=False)
    print("Transformed data saved to 'transformed_financial_data.csv'.")
