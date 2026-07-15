import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import os
warnings.filterwarnings('ignore')

df = pd.read_csv(r'C:\Users\ARUN\Desktop\hr-analytics\data\hr_employee_cleaned.csv')
df.columns = df.columns.str.lower().str.replace(' ', '_')

os.makedirs('outputs', exist_ok=True)

print("=== BASIC INFO ===")
print(f"Shape: {df.shape}")
print(f"\nAttrition Distribution:\n{df['attrition'].value_counts()}")
print(f"Missing Values: {df.isnull().sum().sum()}")

sns.set_theme(style='whitegrid', palette='muted')
COLORS = {'Yes': '#e74c3c', 'No': '#2ecc71'}

# PLOT 1 — Attrition Overview
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Attrition Overview', fontsize=16, fontweight='bold')
counts = df['attrition'].value_counts()
axes[0].pie(counts, labels=counts.index, autopct='%1.1f%%',
            colors=['#2ecc71','#e74c3c'], startangle=90)
axes[0].set_title('Attrition Split')
sns.countplot(data=df, x='attrition', palette=COLORS, ax=axes[1])
axes[1].set_title('Attrition Count')
for p in axes[1].patches:
    axes[1].annotate(f'{int(p.get_height())}',
                     (p.get_x()+p.get_width()/2, p.get_height()),
                     ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/01_attrition_overview.png', dpi=150)
plt.close()
print("✓ Plot 1 saved")

# PLOT 2 — Attrition by Department & Job Role
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Attrition by Department & Job Role', fontsize=16, fontweight='bold')
dept_attr = df.groupby('department')['attrition'].apply(
    lambda x: (x=='Yes').sum()/len(x)*100).sort_values(ascending=False)
dept_attr.plot(kind='bar', ax=axes[0], color='#e74c3c', edgecolor='white')
axes[0].set_title('Attrition Rate % by Department')
axes[0].set_ylabel('Attrition Rate %')
axes[0].tick_params(axis='x', rotation=15)
for p in axes[0].patches:
    axes[0].annotate(f'{p.get_height():.1f}%',
                     (p.get_x()+p.get_width()/2, p.get_height()),
                     ha='center', va='bottom')
role_attr = df.groupby('jobrole')['attrition'].apply(
    lambda x: (x=='Yes').sum()/len(x)*100).sort_values(ascending=False)
role_attr.plot(kind='barh', ax=axes[1], color='#3498db', edgecolor='white')
axes[1].set_title('Attrition Rate % by Job Role')
plt.tight_layout()
plt.savefig('outputs/02_dept_jobrole_attrition.png', dpi=150)
plt.close()
print("✓ Plot 2 saved")

# PLOT 3 — Age Analysis
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Age Analysis', fontsize=16, fontweight='bold')
for label, grp in df.groupby('attrition'):
    axes[0].hist(grp['age'], bins=20, alpha=0.6, label=label, color=COLORS[label])
axes[0].set_title('Age Distribution by Attrition')
axes[0].set_xlabel('Age')
axes[0].legend()
sns.boxplot(data=df, x='attrition', y='age', palette=COLORS, ax=axes[1])
axes[1].set_title('Age Boxplot by Attrition')
plt.tight_layout()
plt.savefig('outputs/03_age_analysis.png', dpi=150)
plt.close()
print("✓ Plot 3 saved")

# PLOT 4 — Salary Analysis
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Salary Analysis', fontsize=16, fontweight='bold')
sns.boxplot(data=df, x='attrition', y='monthlyincome', palette=COLORS, ax=axes[0])
axes[0].set_title('Monthly Income by Attrition')
role_salary = df.groupby('jobrole')['monthlyincome'].mean().sort_values(ascending=False)
role_salary.plot(kind='barh', ax=axes[1], color='#9b59b6', edgecolor='white')
axes[1].set_title('Avg Monthly Income by Job Role')
plt.tight_layout()
plt.savefig('outputs/04_salary_analysis.png', dpi=150)
plt.close()
print("✓ Plot 4 saved")

# PLOT 5 — Overtime Impact
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Overtime Impact on Attrition', fontsize=16, fontweight='bold')
ot_attr = df.groupby(['overtime','attrition']).size().unstack()
ot_attr.plot(kind='bar', ax=axes[0], color=['#2ecc71','#e74c3c'], edgecolor='white')
axes[0].set_title('Overtime vs Attrition Count')
axes[0].tick_params(axis='x', rotation=0)
axes[0].legend(title='Attrition')
ot_rate = df.groupby('overtime')['attrition'].apply(
    lambda x: (x=='Yes').sum()/len(x)*100)
ot_rate.plot(kind='bar', ax=axes[1], color=['#27ae60','#c0392b'], edgecolor='white')
axes[1].set_title('Attrition Rate % by Overtime')
axes[1].tick_params(axis='x', rotation=0)
for p in axes[1].patches:
    axes[1].annotate(f'{p.get_height():.1f}%',
                     (p.get_x()+p.get_width()/2, p.get_height()),
                     ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/05_overtime_impact.png', dpi=150)
plt.close()
print("✓ Plot 5 saved")

# PLOT 6 — Correlation Heatmap
fig, ax = plt.subplots(figsize=(14, 10))
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
corr = df[numeric_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, linewidths=0.5, ax=ax, annot_kws={'size':7})
ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/06_correlation_heatmap.png', dpi=150)
plt.close()
print("✓ Plot 6 saved")

# PLOT 7 — Job Satisfaction & Work Life Balance
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Satisfaction & Work Life Balance', fontsize=16, fontweight='bold')
js_rate = df.groupby('jobsatisfaction')['attrition'].apply(
    lambda x: (x=='Yes').sum()/len(x)*100)
js_rate.plot(kind='bar', ax=axes[0], color='#e67e22', edgecolor='white')
axes[0].set_title('Attrition Rate % by Job Satisfaction')
axes[0].set_xlabel('Job Satisfaction (1=Low, 4=Very High)')
axes[0].tick_params(axis='x', rotation=0)
wlb_rate = df.groupby('worklifebalance')['attrition'].apply(
    lambda x: (x=='Yes').sum()/len(x)*100)
wlb_rate.plot(kind='bar', ax=axes[1], color='#1abc9c', edgecolor='white')
axes[1].set_title('Attrition Rate % by Work Life Balance')
axes[1].set_xlabel('Work Life Balance (1=Bad, 4=Best)')
axes[1].tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.savefig('outputs/07_satisfaction_wlb.png', dpi=150)
plt.close()
print("✓ Plot 7 saved")

# PLOT 8 — Gender & Marital Status
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Gender & Marital Status Analysis', fontsize=16, fontweight='bold')
gender_attr = df.groupby(['gender','attrition']).size().unstack()
gender_attr.plot(kind='bar', ax=axes[0], color=['#2ecc71','#e74c3c'], edgecolor='white')
axes[0].set_title('Attrition by Gender')
axes[0].tick_params(axis='x', rotation=0)
axes[0].legend(title='Attrition')
marital_rate = df.groupby('maritalstatus')['attrition'].apply(
    lambda x: (x=='Yes').sum()/len(x)*100).sort_values(ascending=False)
marital_rate.plot(kind='bar', ax=axes[1], color='#8e44ad', edgecolor='white')
axes[1].set_title('Attrition Rate % by Marital Status')
axes[1].tick_params(axis='x', rotation=0)
for p in axes[1].patches:
    axes[1].annotate(f'{p.get_height():.1f}%',
                     (p.get_x()+p.get_width()/2, p.get_height()),
                     ha='center', va='bottom', fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/08_gender_marital.png', dpi=150)
plt.close()
print("✓ Plot 8 saved")

# KEY INSIGHTS
print("\n=== KEY BUSINESS INSIGHTS ===")
print(f"1. Overall attrition rate: {(df['attrition']=='Yes').mean()*100:.1f}%")
print(f"2. Avg income - Left:    ₹{df[df['attrition']=='Yes']['monthlyincome'].mean():,.0f}")
print(f"   Avg income - Stayed:  ₹{df[df['attrition']=='No']['monthlyincome'].mean():,.0f}")
print(f"3. Overtime attrition:   {df[df['overtime']=='Yes']['attrition'].eq('Yes').mean()*100:.1f}%")
print(f"   No overtime attrition:{df[df['overtime']=='No']['attrition'].eq('Yes').mean()*100:.1f}%")
print(f"4. Highest attrition dept: {df.groupby('department')['attrition'].apply(lambda x: (x=='Yes').mean()*100).idxmax()}")
print(f"5. Single employee attrition: {df[df['maritalstatus']=='Single']['attrition'].eq('Yes').mean()*100:.1f}%")
print("\n✓ All 8 plots saved to outputs/ folder!")