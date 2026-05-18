# tratamento_dados.py
import pandas as pd
import numpy as np

def carregar_e_limpar_base(caminho_csv='base_rh_bruta_aula.csv'):
    """
    Função que centraliza a carga, higienização e engenharia de recursos
    da base de dados de RH. Retorna um DataFrame pronto para uso.
    """
    # 1. Carga dos dados
    df = pd.read_csv(caminho_csv)

    # 2. Remoção de duplicados
    df = df.drop_duplicates(subset='ID_Funcionario')
    
    #mapeamento = {'Recursso Humanos': 'Recursos Humanos', 'T.I.': #'TI'}
    #df['Departamento'] = df['Departamento'].replace(mapeamento)

    # 3. Limpeza de salário (conversão para float)
    df['Salario'] = df['Salario'].astype(str).str.replace('R$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
    df['Salario'] = pd.to_numeric(df['Salario'], errors='coerce')

    # TRATAMENTO DE NANs PARA O MACHINE LEARNING:
    # Opção A: Preencher idades e satisfações vazias com a mediana delas (Mais recomendado para não perder dados)
    mediana_idade = df['Idade'].median()
    df['Idade'] = df['Idade'].fillna(mediana_idade)

    mediana_satisfacao = df['Satisfacao_Trabalho'].median()
    df['Satisfacao_Trabalho'] = df['Satisfacao_Trabalho'].fillna(mediana_satisfacao)

    # Opção B (Alternativa radical): Apenas deletar qualquer linha que ainda tenha ficado com NaN
    # df = df.dropna(subset=['Salario', 'Idade', 'Satisfacao_Trabalho'])

    # 4. Imputação de salários vazios com a média do departamento
    df['Salario'] = df.groupby('Departamento')['Salario'].transform(lambda x: x.fillna(x.mean()))

    # 5. Engenharia de Recursos: Criando coluna de Status de Retenção
    def calcular_status_retencao(row):
        if row['Satisfacao_Trabalho'] < 3 and row['Avaliacao_Desempenho'] >= 4:
            return 'Risco Crítico'
        elif row['Satisfacao_Trabalho'] < 3:
            return 'Desengajado'
        else:
            return 'Estável'

    df['Status_Retencao'] = df.apply(calcular_status_retencao, axis=1)
    
    # Retorna o DataFrame limpo e preparado para o script que o chamou
    return df
