import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tratamento_dados import carregar_e_limpar_base

# Configurando o estilo visual
sns.set_theme(style="whitegrid")

# Chamando a função para obter o DataFrame já tratado
df = carregar_e_limpar_base()

# --- 1. HISTOGRAMA DE DISTRIBUIÇÃO SALARIAL ---
plt.figure(figsize=(10, 5))
# Agora o 'df' existe e está limpo!
sns.histplot(data=df, x='Salario', kde=True, color='royalblue', bins=15)
plt.title('Concentração Salarial da Empresa: Onde está a maior parte da folha?', fontsize=14, pad=15)
plt.xlabel('Faixa Salarial (R$)', fontsize=12)
plt.ylabel('Quantidade de Funcionários', fontsize=12)
plt.show()

# --- 2. HEATMAP (MAPA DE CALOR): DEPARTAMENTO VS. EDUCAÇÃO ---
matriz_educacao = pd.crosstab(df['Departamento'], df['Nivel_Educacao'])
plt.figure(figsize=(10, 6))
sns.heatmap(matriz_educacao, annot=True, fmt='d', cmap='YlGnBu', cbar=True)
plt.title('Matriz de Qualificação: Cruzamento de Departamento por Nível de Educação', fontsize=14, pad=15)
plt.xlabel('Nível de Educação', fontsize=12)
plt.ylabel('Departamento', fontsize=12)
plt.show()

# --- 3. GRÁFICO DE DISPERSÃO (SCATTER PLOT) ---
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Avaliacao_Desempenho', y='Salario', hue='Status_Retencao', palette='Set2', s=100)
plt.axvline(df['Avaliacao_Desempenho'].mean(), color='red', linestyle='--', label='Média de Desempenho')
plt.axhline(df['Salario'].mean(), color='black', linestyle='--', label='Média Salarial')
plt.title('Análise de Meritocracia: O salário acompanha a entrega?', fontsize=14, pad=15)
plt.xlabel('Avaliação de Desempenho (1 a 5)', fontsize=12)
plt.ylabel('Salário Mensal (R$)', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
