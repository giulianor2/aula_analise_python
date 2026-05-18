'''
Questão 3: Análise de Equidade Salarial por Gênero
Enunciado: Como parte da postura ética e conformidade, a empresa precisa verificar disparidades salariais.  Tarefa: Calcule a média salarial por Departamento e Genero. Identifique visualmente se há gaps significativos.
'''
import pandas as pd
import numpy as np

pd.options.display.float_format = '{:.2f}'.format

# Importando a base bruta
df = pd.read_csv('base_rh_bruta_aula.csv')

# Primeiro, saneamento do salário (necessário antes do cálculo) [cite: 1]
df['Salario'] = df['Salario'].str.replace('R$ ', '', regex=False).str.replace('.', '', regex=False)
df['Salario'] = pd.to_numeric(df['Salario'], errors='coerce')

# Agrupamento para análise de equidade [cite: 1]
equidade = df.groupby(['Departamento', 'Genero'])['Salario'].mean().unstack()

print("Média Salarial por Gênero e Departamento:")
print(equidade)

