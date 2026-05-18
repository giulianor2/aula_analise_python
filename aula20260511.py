import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregar a base de dados
df = pd.read_csv('base_rh_bruta_aula.csv')

# 1. Remover Duplicados baseados no ID_Funcionario
df = df.drop_duplicates(subset='ID_Funcionario')

# 2. Corrigir Coluna Salário (Remover 'R$', pontos e tratar vazios)
df['Salario'] = df['Salario'].str.replace('R$', '', regex=False).str.replace('.', '', regex=False)
df['Salario'] = pd.to_numeric(df['Salario'], errors='coerce')

# Preencher salários vazios com a média do departamento
df['Salario'] = df.groupby('Departamento')['Salario'].transform(lambda x: x.fillna(x.mean()))

# 3. Padronizar Departamentos
mapeamento = {'Recursso Humanos': 'Recursos Humanos', 'T.I.': 'TI'}
df['Departamento'] = df['Departamento'].replace(mapeamento)

# 4. Tratar Idades Absurdas (< 18 ou > 100) com a Mediana
mediana_idade = df['Idade'].median()
df.loc[(df['Idade'] < 18 ) | (df['Idade'] > 100), 'Idade'] = mediana_idade

# Converter data de contratação
df['Data_Contratacao'] = pd.to_datetime(df['Data_Contratacao'], format='mixed', dayfirst=True)
hoje = pd.to_datetime('today')

# Tempo de Casa (Anos)
df['Tempo_Casa_Anos'] = (hoje - df['Data_Contratacao']).dt.days / 365

# Alerta de Turnover
def verificar_risco(row):
    if row['Satisfacao_Trabalho'] < 3 and row['Avaliacao_Desempenho'] >= 4:
        return "Risco de Perda"
    return "Estável"

df['Alerta_Turnover'] = df.apply(verificar_risco, axis=1)

# A. Gap de Gênero e Salário
gap_salarial = df.groupby(['Departamento', 'Genero'])['Salario'].mean().unstack()
print(gap_salarial)

# B. Visualização: Pizza - Nível de Educação
df['Nivel_Educacao'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Distribuição por Nível de Educação')
plt.show()

