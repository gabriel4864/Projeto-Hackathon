import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configuração da página
st.set_page_config(page_title="Logística", page_icon="🤡🚦", layout="wide")

# Carregar dados só uma vez
df = pd.read_excel("Frete_por_regiao.xlsx")

# FILTROS
st.sidebar.header("Selecione os Filtros")

transportadora = st.sidebar.multiselect(
    "Filial Responsável",
    options=df["Filial_responsavel"].unique(),
    default=df["Filial_responsavel"].unique(),
    key="transportadora"
)

# Filtrar dataframe
df_selecao = df.query("Filial_responsavel in @transportadora")

def Home():
    st.title("Desempenho das Entregas")

    atrasado = (df_selecao["Atraso_medio"] > 0).sum()
    pontual = (df_selecao["Atraso_medio"] <= 0).sum()
    
    frete_por_tipo = df.groupby("Origem")["Custo_medio"].agg(["mean", "std"]).reset_index().round(2)
    frete_por_tipo.rename(columns={
        "mean": "Custo Médio",
        "std": "Desvio Padrão"
    }, inplace=True)
    
    frete_medio_total = df_selecao["Custo_medio"].mean().round(2)

    status1, status2, status3 = st.columns(3)
    with status1:
        st.metric("Entregas Atrasadas", value=atrasado)
    with status2:
        st.metric("Entregas Pontuais", value=pontual)
    with status3:
        st.metric("Custo Médio de Frete", value=f"R$ {frete_medio_total}")

    st.markdown("---")
    st.subheader("Custos de Frete por Região de Origem")
    st.dataframe(frete_por_tipo)

def Graficos():
    st.title("Análise Gráfica das Entregas")

    # Gráfico de custo médio de frete por origem
    fig_frete_origem = px.bar(
        df_selecao,
        x="Origem",
        y="Custo_medio",
        color="Filial_responsavel",
        title="Custo Médio de Frete por Região de Origem",
        labels={"Custo_medio": "Custo Médio (R$)", "Origem": "Região de Origem"},
        height=600
    )

    fig_frete_origem.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor="#f9f9f9",
        title_font_size=20
    )

    # Gráfico de custo médio de frete por destino
    fig_frete_destino = px.bar(
        df_selecao,
        x="Destino",
        y="Custo_medio",
        color="Filial_responsavel",
        title="Custo Médio de Frete por Região de Destino",
        labels={"Custo_medio": "Custo Médio (R$)", "Destino": "Região de Destino"},
        height=600
    )

    fig_frete_destino.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor="#f9f9f9",
        title_font_size=20
    )

    # Exibir gráficos
    st.plotly_chart(fig_frete_origem, use_container_width=True)
    st.plotly_chart(fig_frete_destino, use_container_width=True)

def sideBar():
    with st.sidebar:
        selecionado = option_menu(
            menu_title="Menu",
            options=["Home", "Gráficos"],
            icons=["🏠", "📉"],
            default_index=0
        )

    if selecionado == "Home":
        Home()
    elif selecionado == "Gráficos":
        Graficos()

sideBar()
