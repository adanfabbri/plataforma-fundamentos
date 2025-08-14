import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
from scipy.signal import argrelextrema
import numpy as np
import io

# Configura layout amplo
st.set_page_config(layout="wide")

# Cabeçalho com imagem centralizada
col1, col2, col3 = st.columns([2.5, 3, 0.1])



# Carregar CSV
df = pd.read_csv("analise_acoes_porcentagem.csv")


df['próxima entrada'] = pd.to_datetime(df['próxima entrada'], errors='coerce')
df = df.sort_values('próxima entrada')

with col1:
    st.image('take2.png', width=150)
    st.subheader("Resumo: Ativo, Empresa e Score Total")

    # Adiciona coluna para seleção
    df['Selecionar'] = False
    df_exibido = st.data_editor(
        df[["Selecionar", "Ativo Meta", "Empresa", "Total", "próxima entrada","proximo Balanco"]],
        use_container_width=True,
        num_rows="dynamic"
    )

    # Filtra as linhas marcadas
    linhas_selecionadas = df_exibido[df_exibido['Selecionar'] == True]

    # Botão para salvar
    if st.button("💾 Gerar seleção para download"):
        if not linhas_selecionadas.empty:
            csv = linhas_selecionadas.drop(columns='Selecionar').to_csv(index=False)
            st.download_button(
                label="📥 Baixar seleção em CSV",
                data=csv,
                file_name="selecao_salva.csv",
                mime="text/csv"
            )
            st.success("✅ Clique no botão acima para baixar o arquivo.")
        else:
            st.warning("⚠️ Nenhuma linha foi selecionada.")

with col2:
 
    st.subheader("🔍 Selecione um ativo para análise detalhada")
    ativos = df['Ativo'].unique()
    ativo_selecionado = st.selectbox("Escolha um ativo", ativos)

    dados_ativo = df[df['Ativo'] == ativo_selecionado]
    if not dados_ativo.empty:
        # Gráfico radar com plotly
        colunas_radar = dados_ativo.drop(columns=["Ativo","Ativo Meta", "Empresa", "Total", "próxima entrada","proximo Balanco"]).select_dtypes(include='number').columns
        valores = dados_ativo[colunas_radar].iloc[0]
        st.subheader("📈 Gráfico Radar dos Indicadores")
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=valores.values,
            theta=colunas_radar,
            fill='toself'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            showlegend=False
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Gráfico de tendência com MM200 + Topos e Fundos
        st.subheader("📉 Tendência de Preço (Fechamento x MM200)")
        try:
            ticker = ativo_selecionado.lower()
            start = dt.datetime.now() - dt.timedelta(days=730)
            end = dt.datetime.now()

            # Baixar e preparar dados do Yahoo
            df_trend = yf.download(ticker, start=start, end=end, interval="1d", auto_adjust=True)
            df_trend = df_trend.drop(columns=['Volume','Open','High','Low'], errors='ignore')
            df_trend['MM200'] = df_trend['Close'].rolling(window=200).mean()
            df_trend = df_trend[df_trend['MM200'].notna()].tail(100).sort_index()

            # Detectar topos e fundos
            n = 5
            close_vals = df_trend['Close'].values
            idx_topos  = argrelextrema(close_vals, np.greater_equal, order=n)[0]
            idx_fundos = argrelextrema(close_vals, np.less_equal,    order=n)[0]
            df_trend['topos']  = np.nan
            df_trend['fundos'] = np.nan
            df_trend.iloc[idx_topos, df_trend.columns.get_loc('topos')]   = df_trend['Close'].iloc[idx_topos].values
            df_trend.iloc[idx_fundos, df_trend.columns.get_loc('fundos')] = df_trend['Close'].iloc[idx_fundos].values

            topos  = df_trend['topos'].dropna()
            fundos = df_trend['fundos'].dropna()

            # Plotagem
            fig2, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df_trend.index, df_trend['Close'], label='Fechamento')
            ax.plot(df_trend.index, df_trend['MM200'],  label='MM200 (200d)', linestyle='--')
            ax.scatter(topos.index,  topos.values,  color='red',   marker='^', s=100, label='Topos')
            ax.scatter(fundos.index, fundos.values, color='green', marker='v', s=100, label='Fundos')
            ax.set_title(f"{ticker.upper()} — Fechamento x MM200 com Topos e Fundos")
            ax.set_xlabel("Data")
            ax.set_ylabel("Preço")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig2, use_container_width=True)
        except Exception as e:
            st.warning(f"⚠️ Erro ao carregar dados do Yahoo Finance: {e}")
    else:
        st.warning("⚠️ Ativo não encontrado na base de dados.")

