'''
Questão 4: ROI de Treinamento e Desenvolvimento
Enunciado: Verifique se as Horas_Treinamento estão impactando a Avaliacao_Desempenho.

Tarefa: Divida as horas de treinamento em 3 faixas: "Baixo" (0-20h), "Médio" (21-60h) e "Alto" (61-100h) e calcule a média de performance de cada grupo.
'''

import pandas as pd
import numpy as np

pd.options.display.float_format = '{:.2f}'.format

# Importando a base bruta
df = pd.read_csv('base_rh_bruta_aula.csv')

# Criando as faixas (bins) [cite: 8, 66]
bins = [0, 20, 60, 100]
labels = ['Baixo', 'Médio', 'Alto']
df['Nivel_Treinamento'] = pd.cut(df['Horas_Treinamento'], bins=bins, labels=labels)

# Analisando o impacto na performance
analise_treinamento = df.groupby('Nivel_Treinamento')['Avaliacao_Desempenho'].mean()

print("Média de Performance por Nível de Treinamento:")
print(analise_treinamento)
