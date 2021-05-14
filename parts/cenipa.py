'''
    2º Projeto da Masterclass de visão computacional do mestre Carlos Melo
    #FamíliaSigmoidal
'''

# Importação das bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

# Link original do dataset: https://raw.githubusercontent.com/carlosfab/curso_data_science_na_pratica/master/modulo_02/ocorrencias_aviacao.csv
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

    # Comon graphical params
    axes_size = 20

    # raw data (tabela) dependente do checkbox
    if tabela.checkbox("Mostrar tabela de dados"):
        st.markdown(''' ------ ''')
        st.write(filtered_df)

    if dist1.checkbox("Latitude e Longitude"):
        st.markdown(''' ------ ''')
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Latitude",
                                                           "Longitude"))

        # Printing information number

        fig.add_histogram(x=filtered_df.latitude,
                          nbinsx=8,
                          legendgroup="latitude",
                          name="Latitude", showlegend=True,
                          xaxis="x",
                          histfunc='sum',  # ['count', 'sum', 'avg', 'min', 'max']
                          histnorm='percent',  # ['', 'percent', 'probability', 'density', 'probability density']
                          hoverinfo='x + y',
                          text=["skip"],  # ['all', 'none', 'skip']
                          marker=dict(color="#00002B"),row=1, col=1)
        fig.add_histogram(x=filtered_df.longitude,
                          nbinsx=8,
                          legendgroup="longitude",
                          name="Longitude", showlegend=True,
                          xaxis="x",
                          histfunc='sum',  # ['count', 'sum', 'avg', 'min', 'max']
                          histnorm='percent',  # ['', 'percent', 'probability', 'density', 'probability density']
                          hoverinfo='x + y',
                          text=["skip"],  # ['all', 'none', 'skip']
                          marker=dict(color="#FF2B2B"), row=1, col=2)
        # Layout formating


        #X-AXES
        fig.update_xaxes(title_text="Graus", showgrid=False,  row=1, col=1)
        fig.update_xaxes(title_text="Graus", showgrid=False, row=1, col=2)

        #Y-AXES
        fig.update_yaxes(title_text="Porcentagem do dataset",
                         ticktext=["0%", "10%", "20%", "30%", "40%"],
                         tickvals=[0, 10, 20, 30, 40],
                         tickmode="array",
                         titlefont=dict(family='Arial',
                                        size=axes_size,
                                        color='#000000'),
                         range=[0, 50],
                         row=1, col=1)
        fig.update_yaxes(ticktext=["0%", "10%", "20%", "30%", "40%"],
                         tickvals=[0, 10, 20, 30, 40],
                         tickmode="array",
                         titlefont=dict(family='Arial',
                                        size=axes_size,
                                        color='#FFFFFF'),
                         range=[0, 50],
                         row=1,col=2)


        #  GENERAL UPDATE
        fig.update_layout(title=dict(text="Distribuição dos dados por Latitude e Longitude",
                                     yref='container',  # ['paper', 'container']
                                     xref='container',  # ['paper', 'container']
                                     x=0.5, y=0.92,
                                     yanchor="auto",  # ['auto', 'top', 'middle', 'bottom']
                                     xanchor="auto",  # ['auto', 'left', 'center', 'right']
                                     font=dict(family='Arial', # "Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", "Droid Sans Mono", "Gravitas One", "Old Standard TT", "Open Sans", "Overpass", "PT Sans Narrow", "Raleway", "Times New Roman"
                                               size=25,
                                               color='#000000')),
                          height=500, width=815,
                          showlegend=True)
        st.plotly_chart(fig, use_container_width=False)

    if dist2.checkbox("Mês do ano"):
        st.markdown(''' ------ ''')
        month = filtered_df.data.dt.month.sort_values().map(dict_month)


        fig = px.histogram(month,x="data",color_discrete_sequence=['#ff2b2b'],histnorm="",
                           hover_data=[month])
                           #hover_data="data")

        fig.update_xaxes(title_text="Mês do ano", showgrid=False,
                         titlefont=dict(family='Arial',
                                        size=axes_size,
                                        color='#000000'),
                         )
        fig.update_yaxes(title_text="Número de ocorrências", showgrid=False,
                         titlefont=dict(family='Arial',
                                        size=axes_size,
                                        color='#000000'),
                         )
        fig.update_layout(title=dict(text="Distribuição das ocorrências por Mês",
                                     yref='container',  # ['paper', 'container']
                                     xref='container',  # ['paper', 'container']
                                     x=0.5, y=0.93,
                                     yanchor="auto",  # ['auto', 'top', 'middle', 'bottom']
                                     xanchor="auto",  # ['auto', 'left', 'center', 'right']
                                     font=dict(family='Arial', # "Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", "Droid Sans Mono", "Gravitas One", "Old Standard TT", "Open Sans", "Overpass", "PT Sans Narrow", "Raleway", "Times New Roman"
                                               size=25,
                                               color='#000000')),
                          height=500, width=800,
                          showlegend=False, hovermode=False)


        st.plotly_chart(fig)

    if dist3.checkbox("Dia da semana"):
        st.markdown(''' ------ ''')
        week = filtered_df.data.dt.dayofweek.sort_values().map(dict_day)
        fig = px.histogram(week, x="data", color_discrete_sequence=['#ff2b2b'], histnorm="",
                           hover_data=[week])

        fig.update_xaxes(title_text="Dia da semana", showgrid=False,
                         titlefont=dict(family='Arial',
                                        size=axes_size,
                                        color='#000000'),
                         )
        fig.update_yaxes(title_text="Número de ocorrências", showgrid=False,
                         titlefont=dict(family='Arial',
                                        size=axes_size,
                                        color='#000000'),
                         )
        fig.update_layout(title=dict(text="Distribuição das ocorrências por dia da semana",
                                     yref='container',  # ['paper', 'container']
                                     xref='container',  # ['paper', 'container']
                                     x=0.5, y=0.93,
                                     yanchor="auto",  # ['auto', 'top', 'middle', 'bottom']
                                     xanchor="auto",  # ['auto', 'left', 'center', 'right']
                                     font=dict(family='Arial',
                                               # "Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", "Droid Sans Mono", "Gravitas One", "Old Standard TT", "Open Sans", "Overpass", "PT Sans Narrow", "Raleway", "Times New Roman"
                                               size=25,
                                               color='#000000')),
                          height=500, width=800,
                          showlegend=False, hovermode="closest")
        st.plotly_chart(fig)

    if dist4.checkbox("Horário"):
        st.markdown(''' ------ ''')
        hora = filtered_df.data.dt.hour
        fig = px.histogram(x= hora,nbins=24, color_discrete_sequence=['#ff2b2b'], histnorm="",
                           hover_data=[hora])

        fig.update_xaxes(title_text="Horário", showgrid=False,
                         titlefont=dict(family='Arial',
                                        size=axes_size,
                                        color='#000000'),
                         )
        fig.update_yaxes(title_text="Número de ocorrências", showgrid=False,
                         titlefont=dict(family='Arial',
                                        size=axes_size,
                                        color='#000000'),
                         )
        fig.update_layout(title=dict(text="Distribuição das ocorrências por horário",
                                     yref='container',  # ['paper', 'container']
                                     xref='container',  # ['paper', 'container']
                                     x=0.5, y=0.93,
                                     yanchor="auto",  # ['auto', 'top', 'middle', 'bottom']
                                     xanchor="auto",  # ['auto', 'left', 'center', 'right']
                                     font=dict(family='Arial',
                                               # "Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", "Droid Sans Mono", "Gravitas One", "Old Standard TT", "Open Sans", "Overpass", "PT Sans Narrow", "Raleway", "Times New Roman"
                                               size=25,
                                               color='#000000')),
                          height=500, width=800,
                          showlegend=False, hovermode="closest")
        st.plotly_chart(fig)

    if count1.checkbox("Classificação"):
        st.markdown(''' ------ ''')

        fig = px.histogram(filtered_df, x="classificacao",
                           opacity=0.95,
                           color_discrete_sequence=['#ff2b2b'],
                           hover_data=[hora])
        fig.update_xaxes(title_text="Classificação", showgrid=False,
                         titlefont=dict(family='Arial',
                                        size=axes_size,
                                        color='#000000'),
                         )
        fig.update_yaxes(title_text="Número de ocorrências", showgrid=False,
                         titlefont=dict(family='Arial',
                                        size=axes_size,
                                        color='#000000'),
                         )
        fig.update_layout(title=dict(text="Distribuição das ocorrências por classificação",
                                     yref='container',  # ['paper', 'container']
                                     xref='container',  # ['paper', 'container']
                                     x=0.5, y=0.93,
                                     yanchor="auto",  # ['auto', 'top', 'middle', 'bottom']
                                     xanchor="auto",  # ['auto', 'left', 'center', 'right']
                                     font=dict(family='Arial',
                                               # "Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", "Droid Sans Mono", "Gravitas One", "Old Standard TT", "Open Sans", "Overpass", "PT Sans Narrow", "Raleway", "Times New Roman"
                                               size=25,
                                               color='#000000')),
                          height=500, width=800,
                          showlegend=False, hovermode="closest")
        st.plotly_chart(fig)

    if count2.checkbox("Tipo de ocorrência"):
        fig = px.histogram(filtered_df, y="tipo", opacity=0.95,
                           color_discrete_sequence=['#ff2b2b'],
                           hover_data=[hora])

        fig.update_xaxes(title_text="Tipo de ocorrência", showgrid=False,
                         titlefont=dict(family='Arial',
                                        size=axes_size,
                                        color='#000000'),
                         )
        fig.update_yaxes(title_text="Número de ocorrências", showgrid=False,
                         titlefont=dict(family='Arial',
                                        size=axes_size,
                                        color='#000000'),
                         )
        fig.update_layout(title=dict(text="Distribuição das ocorrências por tipo",
                                     yref='container',  # ['paper', 'container']
                                     xref='container',  # ['paper', 'container']
                                     x=0.5, y=0.93,
                                     yanchor="auto",  # ['auto', 'top', 'middle', 'bottom']
                                     xanchor="auto",  # ['auto', 'left', 'center', 'right']
                                     font=dict(family='Arial',
                                               # "Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", "Droid Sans Mono", "Gravitas One", "Old Standard TT", "Open Sans", "Overpass", "PT Sans Narrow", "Raleway", "Times New Roman"
                                               size=25,
                                               color='#000000')),
                          height=500, width=800,
                          showlegend=False, hovermode="closest",
                          barmode='stack', yaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig)