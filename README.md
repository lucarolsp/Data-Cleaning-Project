## Projeto Data Cleaning
- Esse projeto apresenta métodos utilizados na limpeza dos dados
- Etapa importante no desenvolvimento de um pepiline de Análises de dados 

## obejtivo do Projeto 
- Mostrar a importância da etapa de limpeza, pois garante confiabilidade e consistência dos dados 

## Métodos Utilizas
### Foi utilizado a linguagem Python
### Iniciando com a importação de bibliotecas
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import statistics as stats
    import seaborn as sns
### Importação do dataset
    df=pd.read_csv("dataset1.csv")
### Visualização das informações do dataset
     df.head()
     df.infor()
     df.describe()
### Contagem de nulos
### Verificação do comportamento dos nulos com gráfico 'bar chart' e 'Heatmap'
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

  (importante para entender o comportamento e verificar se será possivel apaga-lós)
### Padronização de colunas 
### Contagem de duplicatas
### Criação de funções:
    # tratamento de outliers
    def iqr_bounds()
    
### Feature engineering (categorização )

## Finalização 
- Sumário 
