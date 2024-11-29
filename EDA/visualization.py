import matplotlib.pyplot as plt
import seaborn as sns
from data_collection_and_preparation import random_applicants
import pandas as pd

income_vs_approval = random_applicants.groupby('loan_approval_status')['income'].mean()

# LOAN AMOUNT VS REPAYMENT PERIOD 
plt.figure(figsize=(8, 6))
sns.scatterplot(data=random_applicants, x='loan_amount_requested', y='loan_repayment_period', hue='loan_approval_status', palette="Set2", alpha=0.7)
plt.title('Loan Amount vs. Repayment Period')
plt.xlabel('Loan Amount Requested')
plt.ylabel('Repayment Period (Months)')
plt.legend(title='Loan Approval Status')
plt.show()























