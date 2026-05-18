import pandas as pd
import matplotlib.pyplot as plt

# 1. Carregar os dados
df = pd.read_csv('dados_saude_brutos_aula.csv')

# 2. Tratamento de Dados: Converter horários para minutos para calcular a espera
def converter_para_minutos(horario):
    h, m = map(int, horario.split(':'))
    return h * 60 + m

df['CheckIn_Min'] = df['Hora_CheckIn'].apply(converter_para_minutos)
df['Inicio_Min'] = df['Hora_Inicio_Consulta'].apply(converter_para_minutos)

# Calcular Tempo de Espera na Recepção (antes da triagem/médico)
df['Espera_Recepcao_Min'] = df['Inicio_Min'] - df['CheckIn_Min']

# 3. Análise 1: Eficiência dos Canais de Marcação (Taxa de No-Show)
# Converter No_Show para numérico para facilitar cálculo
df['No_Show_Num'] = df['No_Show'].map({'Sim': 1, 'Não': 0})
eficiencia_canal = df.groupby('Canal_Marcacao')['No_Show_Num'].mean() * 100

# 4. Análise 2: O impacto do ambiente no Feedback
# Vamos ver a média de Ruído e Temperatura para notas baixas vs notas altas
impacto_ambiente = df.groupby('Feedback_Apos_Consulta')[['Nivel_Ruido_DB', 'Temp_Sala_Espera_C', 'Ocupacao_Assentos_Perc']].mean()

# 5. Análise 3: Custos e Experiência por Especialidade
custo_experiencia = df.groupby('Especialidade')[['Custo_Material_Gasto_RS', 'Anos_Experiencia_Medico', 'Solicitacao_Exames']].mean()

# --- EXIBIÇÃO DOS RESULTADOS ---

print("--- 1. TAXA DE ABSENTEÍSMO (NO-SHOW) POR CANAL ---")
print(eficiencia_canal.sort_values())
print("\nInsight: Canais com menor porcentagem são mais eficientes.\n")

print("--- 2. IMPACTO DO AMBIENTE NO FEEDBACK DO PACIENTE ---")
print(impacto_ambiente)
print("\nInsight: Verifique se notas 1 e 2 apresentam Ruído ou Ocupação mais altos.\n")

print("--- 3. MÉDIA DE CUSTOS E EXAMES POR ESPECIALIDADE ---")
print(custo_experiencia)

# 6. Identificação de "Anomalias" (Gargalos)
gargalo_espera = df[df['Espera_Recepcao_Min'] > 40][['ID_Paciente_Anonimo', 'Especialidade', 'Espera_Recepcao_Min', 'Feedback_Apos_Consulta']]
print("\n--- PACIENTES COM ESPERA ACIMA DE 40 MIN ---")
print(gargalo_espera.head())


# Gráfico de Canais vs No-Show
eficiencia_canal.plot(kind='bar', color='skyblue')
plt.title('Taxa de Faltas (No-Show) por Canal')
plt.ylabel('Porcentagem (%)')
plt.savefig('grafico_noshow.png')