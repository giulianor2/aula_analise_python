'''
Questão 1: Saneamento de Datas e Tempo de Casa
Enunciado: O banco de dados apresenta datas em múltiplos formatos (Brasileiro e ISO). Para calcular o "Tempo de Casa" em anos, é necessário padronizar a coluna Data_Contratacao.

Tarefa: Converta a coluna para o formato de data correto e crie uma nova coluna Tempo_Casa_Anos baseada na data atual (2026).
'''

import pandas as pd
import numpy as np

pd.options.display.float_format = '{:.2f}'.format

# Importando a base bruta
df = pd.read_csv('base_rh_bruta_aula.csv')

# Conversão com 'mixed' para tratar formatos conflitantes [cite: 1]
df['Data_Contratacao'] = pd.to_datetime(df['Data_Contratacao'], dayfirst=True, format='mixed')

# Cálculo do tempo de casa em anos [cite: 1]
data_atual = pd.to_datetime('2026-05-11') # Data atual conforme contexto
df['Tempo_Casa_Anos'] = (data_atual - df['Data_Contratacao']).dt.days / 365

print(df[['Nome', 'Data_Contratacao', 'Tempo_Casa_Anos']].head())
