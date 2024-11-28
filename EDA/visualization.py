import matplotlib.pyplot as plt
import seaborn as sns
from data_collection_and_preparation import random_applicants
import pandas as pd

income_vs_approval = random_applicants.groupby('loan_approval_status')['income'].mean()

# plt.figure(figsize=(8, 5))
# sns.barplot(x=income_vs_approval.index, y=income_vs_approval.values, palette="viridis")
# plt.title('Average Income by Loan Approval Status')
# plt.ylabel('Average Income')
# plt.xlabel('Loan Approval Status')
# plt.show()


# plt.figure(figsize=(10, 6))
# sns.boxplot(data=random_applicants, x='loan_approval_status', y='credit_score', palette="pastel")
# plt.title('Credit Score Distribution by Loan Approval Status')
# plt.ylabel('Credit Score')
# plt.xlabel('Loan Approval Status')
# plt.show()


# plt.figure(figsize=(8, 6))
# sns.scatterplot(data=random_applicants, x='loan_amount_requested', y='loan_repayment_period', hue='loan_approval_status', palette="Set2", alpha=0.7)
# plt.title('Loan Amount vs. Repayment Period')
# plt.xlabel('Loan Amount Requested')
# plt.ylabel('Repayment Period (Months)')
# plt.legend(title='Loan Approval Status')
# plt.show()


bins = [0, 20000, 50000, 100000, 150000]
labels = ['Low Income', 'Middle Income', 'Upper Middle Income', 'High Income']
random_applicants['income_group'] = pd.cut(random_applicants['income'], bins=bins, labels=labels)

income_group_approval = random_applicants[random_applicants['loan_approval_status'] == 'Approved'].groupby('income_group').size() / random_applicants.groupby('income_group').size()

plt.figure(figsize=(8, 5))
income_group_approval.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Loan Approval Rate by Income Group')
plt.ylabel('Approval Rate')
plt.xlabel('Income Group')
plt.xticks(rotation=45)
plt.show()
