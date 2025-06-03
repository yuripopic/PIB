# Bibliotecas
import pandas_datareader.wb as wb
import pandas as pd

# Indicador de PIB
indicador_pib = 'NY.GDP.MKTP.CD'

# Período de ano desejado
inicio = 2009
fim = 2024

# Todos os países ISO3 válidos
todos_paises = wb.get_countries()
paises_validos = todos_paises[~todos_paises['region'].str.contains('Aggregates')]
codigos = paises_validos['iso3c'].dropna().tolist()

# Função para dividir em blocos
def dividir_em_blocos(lista, tamanho=50):
    for i in range(0, len(lista), tamanho):
        yield lista[i:i + tamanho]

dados = []
for bloco in dividir_em_blocos(codigos):
    try:
        df = wb.download(indicator=indicador_pib, country=bloco, start=inicio, end=fim)
        dados.append(df)
    except Exception as e:
        print(f"Erro ao buscar bloco: {bloco}\n{e}")

# Concatenar tudo
df_pib = pd.concat(dados).reset_index()
df_pib.columns = ['País', 'Ano', 'PIB_USD']
df_pib = df_pib.dropna(subset=['PIB_USD'])

# Salvar no Excel
df_pib.to_excel(f"pib_{inicio}_{fim}.xlsx", index=False)
print('\nData Frame salvo!\n')