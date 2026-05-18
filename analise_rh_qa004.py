import pandas as pd
import numpy as np
from tratamento_dados import carregar_e_limpar_base

# [Nota de Contexto: O df aqui já veio tratado e filtrado pela função 'carregar_e_limpar_base()']
df = carregar_e_limpar_base()

# --- 1. DEFINIÇÃO DE PREMISSAS FINANCEIRAS (BUSINESS CASE) ---
# Segundo a literatura de RH, substituir um funcionário custa entre 1.5 a 2 vezes seu salário anual
FATOR_CUSTO_TURNOVER = 1.5  
PERCENTUAL_AUMENTO_PROPOSTO = 0.05  # Proposta de 5% de aumento salarial para retenção
PROBABILIDADE_RETENCAO_COM_AUMENTO = 0.80  # Assumimos que 80% das pessoas no risco aceitarão e ficarão

# --- 2. CÁLCULO DO IMPACTO FINANCEIRO ATUAL (Cenário de Omissão) ---
# Calculando o salário anualizado de cada funcionário
df['Salario_Anual'] = df['Salario'] * 13  # Considerando 12 meses + 13º salário

# Calculando o custo estimado de perda para CADA funcionário se ele sair
df['Custo_Turnover_Estimado'] = df['Salario_Anual'] * FATOR_CUSTO_TURNOVER

# Filtrando a base para isolar apenas quem está no 'Risco Crítico'
df_risco = df[df['Status_Retencao'] == 'Risco Crítico'].copy()

# Calculando o prejuízo total potencializado (Exposição Financeira ao Risco)
custo_total_risco_pessimista = df_risco['Custo_Turnover_Estimado'].sum()
total_funcionarios_risco = len(df_risco)


# --- 3. SIMULAÇÃO DAESTRATÉGIA DE RETENÇÃO (Cálculo de Investimento) ---
# Quanto custa dar 5% de aumento anual para ESSE grupo que está em risco?
df_risco['Custo_Aumento_Anual'] = (df_risco['Salario'] * PERCENTUAL_AUMENTO_PROPOSTO) * 13
custo_total_investimento_rh = df_risco['Custo_Aumento_Anual'].sum()


# --- 4. CÁLCULO DO RETORNO SOBRE O INVESTIMENTO (ROI) ---
# Se retivermos 80% das pessoas, quantas demissões nós evitamos com sucesso?
demissoes_evitadas = total_funcionarios_risco * PROBABILIDADE_RETENCAO_COM_AUMENTO

# Qual a economia bruta gerada por evitar essas demissões?
economia_bruta = df_risco['Custo_Turnover_Estimado'].sum() * PROBABILIDADE_RETENCAO_COM_AUMENTO

# Economia Líquida = O que economizamos menos o que gastamos dando o aumento de salário
economia_liquida = economia_bruta - custo_total_investimento_rh

# ROI = (Retorno Líquido / Custo do Investimento) * 100
roi_percentual = (economia_liquida / custo_total_investimento_rh) * 100


# --- 5. APRESENTAÇÃO DOS RESULTADOS (DASHBOARD FINANCEIRO) ---
print("====================================================")
print("             BUSINESS CASE: PEOPLE ANALYTICS        ")
print("====================================================")
print(f"Total de talentos em Risco Crítico: {total_funcionarios_risco} funcionários.")
print(f"Exposição Financeira Máxima (Prejuízo Se Todos Saírem): R$ {custo_total_risco_pessimista:,.2f}")
print("----------------------------------------------------")
print(f"Investimento necessário (Aumento de 5% ao ano): R$ {custo_total_investimento_rh:,.2f}")
print(f"Estimativa de demissões evitadas (Eficiência de 80%): {demissoes_evitadas:.1f} profissionais.")
print(f"Economia Bruta em rescisões e contratações: R$ {economia_bruta:,.2f}")
print("----------------------------------------------------")
print(f"ECONOMIA LÍQUIDA PARA A EMPRESA: R$ {economia_liquida:,.2f}")
print(f"ROI DO PROJETO DE RETENÇÃO: {roi_percentual:.2f}%")
print("====================================================")
