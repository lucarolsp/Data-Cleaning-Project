## Data Cleaning Project

-This project presents methods used in data cleaning

-An important step in developing a data analysis pipeline

## Project Objective

-To demonstrate the importance of the cleaning stage, as it ensures data reliability and consistency

## Methods Used

### The Python language was used

### Starting with importing libraries
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import statistics as stats
    import seaborn as sns
### Import do dataset
    df=pd.read_csv("dataset1.csv")
### Dataset Information Visualization
     df.head()
     df.infor()
     df.describe()
     
### Null Count
### Checking null behavior using bar chart and heatmap graphs
    missing_counts = data_costumer.isnull().sum()
    plt.figure(figsize=(10,6))
    missing_counts.plot(kind='bar')
    plt.title("Missing Values Count per Column")
    plt.ylabel("Number of Missing")
    plt.xlabel("Columns")
    plt.xticks(rotation=45)
    plt.show()


    plt.figure(figsize=(12,6))
    sns.heatmap(data_costumer.isnull(), cbar=False, cmap="magma")
    plt.title("Missing Values Heatmap")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    plt.show()

- Important for understanding the behavior and verifying whether it will be possible to remove them

### Column Standardization
### Duplicate Count
### Function Creation:
    # tratamento de outliers
    def iqr_bounds()
    
### Feature engineering (Categorization)

## Conclusion
- Summary
