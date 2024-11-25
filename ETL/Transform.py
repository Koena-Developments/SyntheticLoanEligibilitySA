import pandas as pd
from Extract import generate_data

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
            df[col].fillna(df[col].mean(), inplace=True)

    for col in ['gender', 'location', 'industry', 'job_status']:
        if col in df.columns:
            df[col].fillna(df[col].mode()[0], inplace=True)

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
    df['disposable_income'] = df['income'] - df['expenses']
    df['debt_to_income_ratio'] = df.apply(
        lambda row: row['expenses'] / row['income'] if row['income'] > 0 else None,
        axis=1
    )
    return df

def transform_data(df):
    """
    Cleans and transforms the input DataFrame by adding calculated fields.

    Parameters:
        df (pd.DataFrame): Input DataFrame to transform.

    Returns:
        pd.DataFrame: Transformed DataFrame.
    """
    df = clean_data(df)
    df = add_calculated_fields(df)
    return df

if __name__ == "__main__":
    df = generate_data()

    transformed_df = transform_data(df)

    transformed_df.to_csv("transformed_financial_data.csv", index=False)
    print("Transformed data saved to 'transformed_financial_data.csv'.")
