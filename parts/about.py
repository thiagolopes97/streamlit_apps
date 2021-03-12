# Importação das bibliotecas
import streamlit as st

# Definição da página Sobre Mim
def about_func():
    st.title("Sobre o autor")
    st.markdown("Produzido por **Thiago Lopes**")
    st.markdown("""Atualmente atuo como Data Analyst na [Looqbox](https://www.looqbox.com/).Sou estudante de
                Mestrado em Engenharia Eletrônica e de Computação no Instituto Tecnológico da Aeronáutica (ITA),
                Bacharel em Engenharia Física pela Escola de Engenharia de Lorena da Universidade de São Paulo 
                (EEL - USP). Durante a graduação e meu TCC tive a oportunidade de aprender um pouco sobre Data 
                Science e Machine Learning. Realmente me envolver com dados e programação. Agora é hora de 
                aprimorar meus conhecimentos através da prática e compartilhá-los com vocês.""")
    st.header("Contatos:")
    st.markdown("Email: [thiagogglopes97@gmail.com]")
    st.markdown("[Linkedin](https://www.linkedin.com/in/thiago-lopes-666547164/)")
    st.markdown("[Medium](https://thiagogglopes97.medium.com/)")
    st.markdown("[GitHub](https://github.com/thiagolopes97)")