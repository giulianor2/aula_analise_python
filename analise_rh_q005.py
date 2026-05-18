'''
Questão 5: Visualização de Escolaridade (Storytelling)
Enunciado: Prepare um insight visual para o público não técnico sobre a composição acadêmica da empresa.  Tarefa: Gere um gráfico de pizza mostrando o percentual de colaboradores por Nivel_Educacao.
'''
import pandas as pd
import numpy as np

pd.options.display.float_format = '{:.2f}'.format

# Importando a base bruta
df = pd.read_csv('base_rh_bruta_aula.csv')

import matplotlib.pyplot as plt

# Contagem de valores e plotagem 
df['Nivel_Educacao'].value_counts().plot(kind='bar')
plt.title('Distribuição de Escolaridade na TechSolutions')
plt.ylabel('') # Remove o label do eixo Y para estética
plt.show()

