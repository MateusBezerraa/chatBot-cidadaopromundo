import streamlit as st
import pandas as pd
import json
import os
import time

# Configuração da Página
st.set_page_config(page_title="Dashboard ONG", layout="wide")

st.title("📊 Dashboard de Atendimento - ONG")

# Função para carregar dados
def carregar_dados():
    if not os.path.exists('historico.json'):
        return pd.DataFrame() # Retorna vazio se não tiver arquivo
    
    with open('historico.json', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return pd.DataFrame(data)
        except:
            return pd.DataFrame()

# Botão de atualizar
if st.button('🔄 Atualizar Dados'):
    st.rerun()

df = carregar_dados()

if not df.empty:
    # --- MÉTRICAS DO TOPO ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Atendimentos", len(df))
    
    # Calcula taxa de erro (Quantas vezes o bot não entendeu)
    erros = len(df[df['intencao'] == 'nao_entendeu'])
    taxa_erro = (erros / len(df)) * 100
    col2.metric("Taxa de 'Não Entendi'", f"{taxa_erro:.1f}%")
    
    # Última interação
    col3.metric("Última Interação", df.iloc[-1]['data'])

    st.markdown("---")

    # --- GRÁFICOS ---
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("Dúvidas Mais Frequentes")
        # Conta quantas vezes cada intencao apareceu
        contagem = df['intencao'].value_counts()
        st.bar_chart(contagem)

    with col_graf2:
        st.subheader("Histórico Recente")
        # Mostra apenas as colunas importantes
        st.dataframe(df[['data', 'pergunta_usuario', 'intencao']].iloc[::-1], hide_index=True)

else:
    st.info("Ainda não há dados de histórico. Converse com o bot para gerar dados!")