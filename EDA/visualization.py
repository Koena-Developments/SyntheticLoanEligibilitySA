import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt

conn = sqlite3.connect("loan_applicants.db")
loan_data = pd.read_sql("SELECT * FROM loan_applicants", conn)
conn.close()

loan_data['income_group'] = pd.cut(
    loan_data['disposable_income'],
    bins=[0, 10000, 20000, 30000, 50000],
    labels=["Low", "Medium", "High", "Very High"]
)


income_approval = loan_data.groupby(['income_group', 'loan_approval_status'], observed=False).size().unstack(fill_value=0)
income_approval.plot(kind='bar', stacked=True)
plt.title("Income Group vs Loan Approval Status")
plt.xlabel("Income Group")
plt.ylabel("Number of Applications")
plt.legend(title="Loan Approval Status")
plt.show()

sns.histplot(data=loan_data, x="credit_score", hue="loan_approval_status", kde=True, palette="muted")
plt.title("Credit Score Distribution by Loan Approval Status")
plt.xlabel("Credit Score")
plt.ylabel("Frequency")
plt.show()

sns.scatterplot(
    data=loan_data,
    x="monthly_repayment",
    y="loan_repayment_period",
    hue="loan_approval_status",
    palette="coolwarm",
)
plt.title("Monthly Repayment vs Loan Repayment Period")
plt.xlabel("Monthly Repayment Amount")
plt.ylabel("Repayment Period (Months)")
plt.show()

loan_data.to_excel("Loan_Insights_Analysis.xlsx", index=False)
print("Insights saved to Loan_Insights_Analysis.xlsx")
