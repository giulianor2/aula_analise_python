# Filtragem lógica (Boolean Indexing)
'''
Questão 2: Identificação Preventiva de Burnout
Enunciado: A retenção de talentos é uma meta estratégica. Identifique colaboradores que possuem Alta Performance (Avaliação $\ge$ 4) mas Baixa Satisfação (Satisfação $\le$ 2).  Tarefa: Crie um DataFrame chamado risco_burnout e conte quantos funcionários estão nessa situação.
'''

import pandas as pd
import numpy as np

pd.options.display.float_format = '{:.2f}'.format

# Importando a base bruta
df = pd.read_csv('base_rh_bruta_aula.csv')

risco_burnout = df[(df['Avaliacao_Desempenho'] >= 4) & (df['Satisfacao_Trabalho'] <= 2)]

# Exibindo o resultado
print(f"Total de talentos em risco de burnout: {len(risco_burnout)}")
print(risco_burnout[['Nome', 'Departamento', 'Cargo']])
