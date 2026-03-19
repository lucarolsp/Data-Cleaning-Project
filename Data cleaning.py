
# Data Cleaning Project -
# Complete Cleaning and Transformation Pipeline


# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as stats
import seaborn as sns
from tqdm import tqdm
import random
import warnings
# ! pip install sqlalchemy - for database connection if needed
# ! pip install sqlalchemy pandas - for database connection if needed

from sqlalchemy import create_engine

# import dataset
data_costumer = pd.read_csv(r'C:\Users\suelm\Documents\1_PROJETOS DE ANALISE DE DADOS\PROJETOS\DATA CLEANING\dataset1.csv')
data_costumer.head(10)
data_costumer.columns

# dataset info
data_costumer.info()

# dataset description
data_costumer.describe()


# check missing values
data_costumer.isnull().sum()

# Missing Values Heatmap
plt.figure(figsize=(12,6))
sns.heatmap(data_costumer.isnull(), cbar=False, cmap="magma")
plt.title("Missing Values Heatmap")
plt.xlabel("Columns")
plt.ylabel("Rows")
plt.show()

# Missing values bar chart
missing_counts = data_costumer.isnull().sum()

plt.figure(figsize=(10,6))
missing_counts.plot(kind='bar')
plt.title("Missing Values Count per Column")
plt.ylabel("Number of Missing")
plt.xlabel("Columns")
plt.xticks(rotation=45)
plt.show()

# Important charts to observe how missing data behaves, as it impacts analysis

# total missing values
data_costumer.isnull().sum().sum()

# check duplicates
data_costumer.duplicated().sum()


# Keep first occurrence of each email
data_costumer = data_costumer[~(data_costumer['email'].notna() & data_costumer.duplicated(subset=['email'], keep='first'))]
data_costumer.reset_index(drop=True, inplace=True)

print(f"\n  After cleaning: {len(data_costumer):,} rows ({len(data_costumer) - len(data_costumer)} removed)")


# Column standardization

# Names: strip and title case
data_costumer['nome'] = data_costumer['nome'].str.strip().str.title()

# Email: strip and lowercase
data_costumer['email'] = data_costumer['email'].str.strip().str.lower()

# Status: strip and title case
data_costumer['status_cliente'] = data_costumer['status_cliente'].str.strip().str.title()

# Basic email validation
email_valido_mask = data_costumer['email'].str.contains(r'^[\w\.-]+@[\w\.-]+\.\w+$', na=False)
emails_invalidos = (~email_valido_mask & data_costumer['email'].notna()).sum()
data_costumer.loc[~email_valido_mask & data_costumer['email'].notna(), 'email'] = np.nan
print(f"   Invalid emails converted to NaN: {emails_invalidos}")

# Credit score: round to integer
data_costumer['score_credito'] = data_costumer['score_credito'].round(0)

# Status distribution
print(f"\n   Status distribution after standardization:")
print(data_costumer['status_cliente'].value_counts().to_string())
print(f"\n    Standardization completed")


# OUTLIER TREATMENT

def iqr_bounds(series, multiplier=1.5):
    """Calculate lower and upper bounds using IQR method."""
    Q1, Q3 = series.quantile([0.25, 0.75])
    IQR = Q3 - Q1
    return Q1 - multiplier * IQR, Q3 + multiplier * IQR

cols_outlier = ['renda_mensal', 'valor_compras_total', 'score_credito']

stats_before = data_costumer[cols_outlier].describe().T[['min', 'max', 'mean', 'std']].round(2)

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Outliers: Before and After Treatment', fontsize=15, fontweight='bold')

for i, col in enumerate(cols_outlier):
    axes[0, i].boxplot(data_costumer[col].dropna(), patch_artist=True,
                       boxprops=dict(facecolor='#FFB3B3'))
    axes[0, i].set_title(f'{col}\n(BEFORE)', fontsize=11)
    axes[0, i].set_ylabel('Value')

for col in cols_outlier:
    if col == 'renda_mensal':
        n_neg = (data_costumer[col] < 0).sum()
        data_costumer.loc[data_costumer[col] < 0, col] = np.nan
        print(f"   {col}: {n_neg} negative values → NaN (business rule)")

    low, high = iqr_bounds(data_costumer[col].dropna(), multiplier=3.0)
    n_out_low = (data_costumer[col] < low).sum()
    n_out_high = (data_costumer[col] > high).sum()
    data_costumer[col] = data_costumer[col].clip(lower=max(0, low), upper=high)
    print(f"   {col}: {n_out_low + n_out_high} outliers treated by IQR")

stats_after = data_costumer[cols_outlier].describe().T[['min', 'max', 'mean', 'std']].round(2)

for i, col in enumerate(cols_outlier):
    axes[1, i].boxplot(data_costumer[col].dropna(), patch_artist=True,
                       boxprops=dict(facecolor='#B3D9FF'))
    axes[1, i].set_title(f'{col}\n(AFTER)', fontsize=11)

plt.tight_layout()
plt.close()


# MISSING VALUES TREATMENT

missing_before = data_costumer.isnull().sum()

# numeric → median
num_cols_missing = ['renda_mensal', 'score_credito']
for col in num_cols_missing:
    median = data_costumer[col].median()
    n_miss = data_costumer[col].isnull().sum()
    data_costumer[col] = data_costumer[col].fillna(median)
    print(f"   {col}: {n_miss} NaN → median")

# satisfaction → group median
data_costumer['satisfacao'] = data_costumer.groupby('status_cliente')['satisfacao'].transform(
    lambda x: x.fillna(x.median())
)
data_costumer['satisfacao'] = data_costumer['satisfacao'].fillna(data_costumer['satisfacao'].median()).round(0)

# email/phone flags
data_costumer['email_disponivel'] = data_costumer['email'].notna().astype(int)
data_costumer['telefone_disponivel'] = data_costumer['telefone'].notna().astype(int)
data_costumer['email'] = data_costumer['email'].fillna('unknown@email.com')
data_costumer['telefone'] = data_costumer['telefone'].fillna('Not provided')

missing_after = data_costumer.isnull().sum()


# FEATURE ENGINEERING

today = pd.Timestamp.now()

data_costumer['idade'] = data_costumer['data_nascimento'].apply(
    lambda x: (today - pd.Timestamp(x)).days // 365 if pd.notna(x) else np.nan
)

data_costumer['faixa_etaria'] = pd.cut(
    data_costumer['idade'],
    bins=[0, 25, 35, 50, 65, 120],
    labels=['18-25', '26-35', '36-50', '51-65', '65+'],
    right=False
)

data_costumer['meses_relacionamento'] = ((today - data_costumer['data_cadastro']).dt.days / 30.44).round(1)

data_costumer['ticket_medio'] = np.where(
    data_costumer['num_produtos'] > 0,
    data_costumer['valor_compras_total'] / data_costumer['num_produtos'],
    0
)

# FINAL SUMMARY

print("\n" + "=" * 60)
print("  FINAL PIPELINE SUMMARY")
print("=" * 60)

summary = {
    'Raw rows': data_costumer.shape[0],
    'Clean rows': len(data_costumer),
    'Original columns': data_costumer.shape[1],
    'Final columns': len(data_costumer.columns),
    'Missing values': data_costumer.isnull().sum().sum(),
}

for k, v in summary.items():
    print(f"   {k:<30} {v}")