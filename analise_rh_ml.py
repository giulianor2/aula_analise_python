import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tratamento_dados import carregar_e_limpar_base

# Importando ferramentas essenciais do Scikit-Learn
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# [Nota: O 'df' aqui já foi carregado e higienizado previamente]
df = carregar_e_limpar_base()

# Vamos simular que criamos a coluna alvo 'Saiu_da_Empresa' (0 = Ficou, 1 = Saiu) para supervisionar o modelo,
# ou usaremos a regra de risco como proxy se for uma base 100% ativa.
# Para este exemplo, usaremos variáveis preditoras numéricas estáveis.


# =========================================================================
# PARTE 1: CLASSIFICAÇÃO (ÁRVORE DE DECISÃO) - PREVISÃO DE CHURN / TURNOVER
# =========================================================================

# 1.1 Selecionando as Variáveis Recurso (X) e a Variável Alvo (y)
# Queremos prever o risco com base em variáveis numéricas brutas (evitando usar o Status de Retenção que nós mesmos criamos)
X = df[['Salario', 'Idade', 'Satisfacao_Trabalho', 'Avaliacao_Desempenho']]

# Criando um alvo binário real fictício baseado no desengajamento/risco para o modelo aprender o padrão
y = df['Status_Retencao'].apply(lambda x: 1 if x in ['Risco Crítico', 'Desengajado'] else 0)

# 1.2 Dividindo os dados em Treino (70%) e Teste (30%)
# Isso evita o "Overfitting" (quando o modelo decora os dados em vez de aprender)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# 1.3 Inicializando e Treinando o Modelo de Árvore de Decisão
# Definimos max_depth=3 para a árvore não crescer demais e podermos explicar visualmente na aula
modelo_churn = DecisionTreeClassifier(max_depth=3, random_state=42)
modelo_churn.fit(X_train, y_train)

# 1.4 Avaliando o Modelo
predicoes = modelo_churn.predict(X_test)
acuracia = accuracy_score(y_test, predicoes)

print("====================================================")
print(f"EFICIÊNCIA DO MODELO DE PREVISÃO DE CHURN: {acuracia*100:.2f}%")
print("====================================================")

# 1.5 Plotando a Árvore de Decisão (Visualização Didática)
plt.figure(figsize=(15, 8))
plot_tree(modelo_churn, feature_names=X.columns, class_names=['Estável', 'Alerta Churn'], filled=True, rounded=True)
plt.title("Árvore de Decisão: Como o algoritmo pensa para prever a saída de um funcionário")
plt.show()


# =========================================================================
# PARTE 2: AGRUPAMENTO (K-MEANS) - CRIANDO "PERSONAS" DE FUNCIONÁRIOS
# =========================================================================

# 2.1 Selecionando características para agrupamento
recursos_cluster = df[['Salario', 'Idade', 'Satisfacao_Trabalho']]

# 2.2 Padronização dos Dados (Essencial para o K-Means!)
# Como Salário vai até 15000 e Idade vai até 60, o K-Means acharia que o Salário é mais importante.
# O StandardScaler deixa todas as variáveis na mesma escala de relevância (Média 0, Variância 1)
scaler = StandardScaler()
dados_padronizados = scaler.fit_transform(recursos_cluster)

# 2.3 Treinando o K-Means para criar 3 Grupos (Personas) distintos
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['Cluster_Persona'] = kmeans.fit_predict(dados_padronizados)

# 2.4 Analisando o perfil médio de cada grupo criado pelo algoritmo
print("\n### PERFIL DAS PERSONAS CRIADAS PELO K-MEANS ###")
perfil_personas = df.groupby('Cluster_Persona')[['Salario', 'Idade', 'Satisfacao_Trabalho', 'Avaliacao_Desempenho']].mean()
print(perfil_personas)

# 2.5 Plotando o gráfico de Personas (Scatter Plot Colorido por Cluster)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Idade', y='Salario', hue='Cluster_Persona', palette='Accent', s=100)
plt.title('Segmentação K-Means: Mapeamento de Personas Corporativas')
plt.xlabel('Idade')
plt.ylabel('Salário Mensal (R$)')
plt.legend(title='Persona ID')
plt.show()
