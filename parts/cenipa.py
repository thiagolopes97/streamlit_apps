'''
    2º Projeto da Masterclass de visão computacional do mestre Carlos Melo
    #FamíliaSigmoidal
'''

# Importação das bibliotecas
import streamlit as st
import pandas as pd
import pydeck as pdk
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# Link original do dataset: https://raw.githubusercontent.com/carlosfab/curso_data_science_na_pratica/master/modulo_02/ocorrencias_aviacao.csv
#DATA_URL = "https://raw.githubusercontent.com/thiagolopes97/CENIPA_Visu/master/data/ocorrencias_aviacao.csv"
DATA_URL = "data/ocorrencias_aviacao.csv"
@st.cache
def load_data():
    """
    Carrega os dados de ocorrências aeronáuticas do CENIPA.

    :return: DataFrame com colunas selecionadas.
    """
    columns = {
        'ocorrencia_latitude': 'latitude',
        'ocorrencia_longitude': 'longitude',
        'ocorrencia_dia': 'data',
        'ocorrencia_classificacao': 'classificacao',
        'ocorrencia_tipo': 'tipo',
        'ocorrencia_tipo_categoria': 'tipo_categoria',
        'ocorrencia_tipo_icao': 'tipo_icao',
        'ocorrencia_aerodromo': 'aerodromo',
        'ocorrencia_cidade': 'cidade',
        'investigacao_status': 'status',
        'divulgacao_relatorio_numero': 'relatorio_numero',
        'total_aeronaves_envolvidas': 'aeronaves_envolvidas'
    }

    data = pd.read_csv(DATA_URL, index_col='codigo_ocorrencia')
    data = data.rename(columns=columns)
    data.data = data.data + " " + data.ocorrencia_horario
    data.data = pd.to_datetime(data.data)
    data = data[list(columns.values())]

    return data

dict_day = { 0: "Segunda",
             1: "Terça",
             2: "Quarta",
             3: "Quinta",
             4: "Sexta",
             5: "Sábado",
             6: "Domingo"
            }

dict_month ={1: "Janeiro",
             2: "Fevereiro",
             3: "Março",
             4: "Abril",
             5: "Maio",
             6: "Junho",
             7: "Julho",
             8: "Agosto",
             9: "Setembro",
             10: "Outubro",
             11: "Novembro",
             12: "Dezembro"
            }

# Carregando a página Projeto Cenipa
def cenipa_func():
    # Carregar dados
    df = load_data()
    # Limpar outliers de localização
    df = df[(df.longitude < -25) & (df.longitude > -80) & (df.latitude > -45) & (df.latitude < 10)]
    labels = df.classificacao.unique().tolist()
    tipo = df.tipo_categoria.unique().tolist()

    # SIDEBAR
    st.sidebar.header("Thiago Lopes - CENIPAVisu")
    st.sidebar.markdown("App para analisar dados de acidentes aêoro.")

    # Informação no rodapé da Sidebar
    st.sidebar.markdown(""" A base de dados de ocorrências aeronáuticas é gerenciada pelo ***Centro de 
                        Investigação e Prevenção de Acidentes Aeronáuticos (CENIPA)***.
                        """)

    # Parâmetros e número de ocorrências
    st.sidebar.header("Parâmetros selecionados")
    info_sidebar = st.sidebar.empty()  # placeholder, para informações filtradas que só serão carregadas depois
    progress = st.sidebar.empty()
    porcent = st.sidebar.empty()

    # Slider de seleção do ano
    st.sidebar.subheader("Ano")
    filtro = st.sidebar.selectbox("Qual filtro deseja:", ("Ano fixo", "Período"))
    if filtro == "Ano fixo":
        year_to_filter = st.sidebar.slider('Escolha o ano desejado', 2008, 2018, 2015)
        df = df[(df.data.dt.year == year_to_filter)]
        year_text = str(year_to_filter)

    elif filtro == "Período":
        year_1 = st.sidebar.slider('Início', 2008, 2018, 2008)
        year_2 = st.sidebar.slider('Fim', 2008, 2018, 2018)
        df = df[(df.data.dt.year >= year_1) & (df.data.dt.year <= year_2)]
        year_text = str(year_1) + ' - ' + str(year_2)

    # Multiselect com os lables únicos dos tipos de classificação
    label_to_filter = st.sidebar.multiselect(
        label="Escolha a classificação da ocorrência",
        options=labels,
        default=["INCIDENTE", 'ACIDENTE']
    )

    # Multiselect com os lables únicos do tipo de categoira
    tipo_to_filter = st.sidebar.multiselect(
        label="Escolha o tipo de ocorrência",
        options=tipo,
        default=tipo
    )

    filtered_df = df[(df.classificacao.isin(label_to_filter)) & (df.tipo_categoria.isin(tipo_to_filter))]

    st.sidebar.header("Data Analysis")
    # Checkbox da Tabela
    st.sidebar.subheader("Tabela")
    tabela = st.sidebar.empty()  # placeholder que só vai ser carregado com o df_filtered

    st.sidebar.subheader("Distribuição")
    dist1 = st.sidebar.empty()
    dist2 = st.sidebar.empty()
    dist3 = st.sidebar.empty()
    dist4 = st.sidebar.empty()
    count1 = st.sidebar.empty()
    count2 = st.sidebar.empty()
    count3 = st.sidebar.empty()

    # Aqui o placehoder vazio finalmente é atualizado com dados do filtered_df
    info_sidebar.info("{} ocorrências selecionadas de um total de {}.".format(filtered_df.shape[0],df.shape[0]))
    porcentagem = round(filtered_df.shape[0] / df.shape[0],2)
    porcent.markdown("Estão sendo analisados {}% dos casos neste período".format(porcentagem*100))
    progress.progress(porcentagem)

    # Mapa principal
    st.title("CENIPA - Acidentes Aeronáuticos")
    st.markdown(f"""
                Estão sendo exibidas as ocorrências classificadas como **{", ".join(label_to_filter)}**
                para o ano de **{"{}".format(year_text)}**.
                """)

    st.subheader("Mapa de ocorrências")
    st.map(filtered_df)

    # raw data (tabela) dependente do checkbox
    if tabela.checkbox("Mostrar tabela de dados"):
        st.write(filtered_df)
    if dist1.checkbox("Latitude e Longitude"):
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        fig = sns.distplot(filtered_df.longitude,color='#ff2b2b')
        plt.title("Distribuição de ocorrências por longitude")
        plt.ylabel("%")
        plt.subplot(1, 2, 2)
        fig = sns.distplot(filtered_df.latitude,color='#ff2b2b')
        plt.title("Distribuição de ocorrências por Latitude")
        plt.tight_layout()
        st.pyplot();

    if dist2.checkbox("Mês do ano"):
        month = filtered_df.data.dt.month.sort_values().map(dict_month)
        plt.figure(figsize=(10, 4))
        fig = sns.countplot(month,color="#ff2b2b")
        plt.ylabel("Nº de ocorrências")
        plt.xlabel("")
        plt.title("Número de ocorrências/ mês")
        plt.tight_layout()
        st.pyplot();

    if dist3.checkbox("Dia da semana"):
        week = filtered_df.data.dt.dayofweek.sort_values().map(dict_day)
        plt.figure(figsize=(10, 4))
        fig = sns.countplot(week,color="#ff2b2b")
        plt.xlabel("")
        plt.ylabel("Nº de ocorrências")
        plt.title("Número de ocorrências/ dia da semana")
        plt.tight_layout()
        st.pyplot();

    if dist4.checkbox("Horário"):
        hora = filtered_df.data.dt.hour
        fig = sns.countplot(hora,color="#ff2b2b")
        plt.ylabel("Nº de ocorrências")
        plt.title("Número de ocorrências/ horário")
        plt.tight_layout()
        st.pyplot();

    if count1.checkbox("Classificação"):
        fig = sns.countplot(x='classificacao',data=filtered_df,color="#ff2b2b")
        plt.title("Número de ocorrências/ classificação")
        plt.ylabel("Nº de ocorrências")
        plt.tight_layout()
        st.pyplot();

    if count2.checkbox("Tipo de ocorrência"):
        plt.figure(figsize=(10,6.5))
        fig = sns.countplot(y='tipo_categoria',data=filtered_df,color="#ff2b2b")
        plt.ylabel("")
        plt.xlabel("Nº de ocorrências")
        plt.title("Número de ocorrências/ tipo")
        plt.tight_layout()
        st.pyplot();

    if count3.checkbox("Cidades mais comuns"):
        plt.figure(figsize=(10,6.5))
        nome = filtered_df.cidade.value_counts().sort_values(ascending=False).index[:10]
        valor = filtered_df.cidade.value_counts().sort_values(ascending=False)[:10]
        fig = plt.barh(y=nome,width=valor,color="#ff2b2b")
        plt.ylabel("")
        plt.xlabel("Nº de ocorrências")
        plt.title("Top 10 - Número de ocorrências/ cidade")
        plt.tight_layout()
        st.pyplot();