import pandas as pd
from Extract import generate_data
import numpy as np  # For numerical operations

def clean_data(df):
    """
    Cleans the input DataFrame by handling missing values, outliers,
    and dropping duplicate names.

    Parameters:
        df (pd.DataFrame): Input DataFrame to clean.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    # Drop duplicate names
    df = df.drop_duplicates(subset=['full_name'], keep='first')

    # Fill missing values for numeric columns with the mean
    for col in ['income', 'expenses', 'credit_score']:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mean())

    # Fill missing values for categorical columns with the mode
    for col in ['gender', 'location', 'industry', 'job_status']:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mode()[0])

    # Cap numeric fields
    df['income'] = df['income'].apply(lambda x: min(x, 50000))
    df['expenses'] = df['expenses'].apply(lambda x: min(x, 40000))
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
    # Calculate disposable income
    df['disposable_income'] = df['income'] - df['expenses']

    # Calculate debt-to-income ratio
    df['debt_to_income_ratio'] = df.apply(
        lambda row: row['expenses'] / row['income'] if row['income'] > 0 else float('inf'),
        axis=1
    )

    return df


def transform_data(df):
    """
    Transforms the data by cleaning it, adding calculated fields, and applying loan decisioning logic.

    Args:
        df (pd.DataFrame): The raw data DataFrame.

    Returns:
        pd.DataFrame: The transformed data.
    """
    # Clean the data
    df = clean_data(df)

    # Add calculated fields
    df = add_calculated_fields(df)

    # Loan decision logic
    def determine_loan_status(row):
        if row['credit_score'] > 650 and row['debt_to_income_ratio'] < 0.4:
            return "Approved"
        elif 500 <= row['credit_score'] <= 650 or 0.4 <= row['debt_to_income_ratio'] <= 0.5:
            return "Conditional Approval"
        else:
            return "Rejected"

    # Apply loan decision logic
    df['loan_approval_status'] = df.apply(determine_loan_status, axis=1)

    return df


if __name__ == "__main__":
    # Load data
    df = pd.read_csv("synthetic_financial_data.csv")
    
    # Transform data
    transformed_df = transform_data(df)
    
    # Save the transformed data
    transformed_df.to_csv("transformed_financial_data.csv", index=False)
    print("Transformed data saved to 'transformed_financial_data.csv'.")
