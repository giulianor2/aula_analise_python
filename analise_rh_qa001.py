import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração para visualização
plt.style.use('ggplot')

# --- PASSO 1: CARGA E HIGIENIZAÇÃO REFINADA ---
df = pd.read_csv('base_rh_bruta_aula.csv')

# Removendo duplicados (Garantindo que cada ID seja único)
df = df.drop_duplicates(subset='ID_Funcionario')

# Limpeza de Salário: Transformando string "R$ 5.000,00" em float 5000.00
# Nota: Tratamos o ponto de milhar e a vírgula decimal se houver
df['Salario'] = df['Salario'].str.replace('R$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
df['Salario'] = pd.to_numeric(df['Salario'], errors='coerce')

# Imputação por Agrupamento: Preenche salários vazios com a média do setor específico
df['Salario'] = df.groupby('Departamento')['Salario'].transform(lambda x: x.fillna(x.mean()))

# --- PASSO 2: ENGENHARIA DE RECURSOS (KPIs) ---
# Cálculo de Tempo de Casa mais preciso
df['Data_Contratacao'] = pd.to_datetime(df['Data_Contratacao'], format='mixed', dayfirst=True)
hoje = pd.to_datetime('today')
df['Anos_Empresa'] = (hoje - df['Data_Contratacao']).dt.days / 365.25

# Criando a Coluna de Risco (Matriz 9-Box simplificada)
# High Performer + Low Satisfaction = Perigo de Turnover
def calcular_status_retencao(row):
    if row['Satisfacao_Trabalho'] < 3 and row['Avaliacao_Desempenho'] >= 4:
        return 'Risco Crítico'
    elif row['Satisfacao_Trabalho'] < 3:
        return 'Desengajado'
    else:
        return 'Estável'

df['Status_Retencao'] = df.apply(calcular_status_retencao, axis=1)

# --- PASSO 3: ANÁLISE DE INSIGHTS (Aprofundamento) ---

# A. Gap Salarial por Gênero (Métrica de Governança)
print("### Média Salarial por Gênero e Departamento ###")
print(df.groupby(['Departamento', 'Genero'])['Salario'].mean().unstack())

# B. Correlação: Será que quem ganha mais está mais satisfeito?
# O insight aqui é verificar se o salário é o único motivador
correlacao = df[['Salario', 'Satisfacao_Trabalho', 'Anos_Empresa']].corr()
print("\n### Matriz de Correlação ###")
print(correlacao)

# --- PASSO 4: VISUALIZAÇÃO E STORYTELLING ---

# Visualizando a distribuição de salários para identificar desigualdades (Histograma)
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Salario', hue='Genero', kde=True, element="step")
plt.title('Distribuição Salarial por Gênero')
plt.show()

# Visualizando o Risco de Turnover (O Insight de Negócio)
plt.figure(figsize=(8, 5))
df['Status_Retencao'].value_counts().plot(kind='bar', color=['skyblue', 'salmon', 'lightgreen'])
plt.title('Panorama de Retenção de Talentos')
plt.ylabel('Quantidade de Funcionários')
plt.xticks(rotation=0)
plt.show()
