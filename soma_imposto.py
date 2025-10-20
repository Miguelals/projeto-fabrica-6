import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# =====================
# Função pura com validação
# =====================
def somaImposto(taxaImposto: float, custo: float) -> float:
    if taxaImposto < 0:
        raise ValueError("A taxa de imposto não pode ser negativa.")
    if custo < 0:
        raise ValueError("O custo não pode ser negativo.")
    return custo * (1 + taxaImposto / 100.0)

# =====================
# Configuração da página
# =====================
st.set_page_config(
    page_title="🛒 Preço com Imposto Animado",
    page_icon="💰",
    layout="centered"
)

st.title("🛒 Calculadora de Preço com Imposto Animado")
st.markdown("""
Digite o **custo do item** e a **taxa de imposto** e veja o preço final crescer animadamente!
""")
st.markdown("---")

# =====================
# Entradas de dados
# =====================
taxa_input = st.text_input("Taxa de imposto (%)", value="17.5")
custo_input = st.text_input("Custo do item (antes do imposto)", value="200")

# =====================
# Botão de cálculo animado
# =====================
if st.button("✅ Calcular e Animar"):
    try:
        # Conversão e validação
        taxa = float(taxa_input.replace(',', '.'))
        custo = float(custo_input.replace(',', '.'))
        preco_final = somaImposto(taxa, custo)
        valor_imposto = preco_final - custo

        # =====================
        # Cria DataFrame para animação
        # =====================
        passos = 50  # número de frames
        precos = np.linspace(custo, preco_final, passos)
        df_anim = pd.DataFrame({
            "Etapa": range(1, passos+1),
            "Preço com Imposto": precos
        })

        # =====================
        # Gráfico de linha animado
        # =====================
        fig = px.line(df_anim, x="Etapa", y="Preço com Imposto",
                      markers=True,
                      labels={"Preço com Imposto": "Preço com Imposto (R$)", "Etapa": ""},
                      title="Evolução do Preço com Imposto")
        
        # Mostra o valor em cada ponto
        fig.update_traces(text=df_anim["Preço com Imposto"].map("R$ {:,.2f}".format),
                          textposition="top right",
                          line=dict(color="#FF5733", width=4),
                          marker=dict(size=8, color="#FF5733"))

        # Ajuste dos eixos
        fig.update_layout(
            yaxis=dict(range=[custo*0.95, preco_final*1.05]),
            xaxis=dict(showticklabels=False),
            hovermode="x unified",
            title=dict(x=0.5, xanchor="center")
        )

        st.plotly_chart(fig, use_container_width=True)

        # =====================
        # Exibe resultado final
        # =====================
        st.success(f"💵 Preço final com imposto: R$ {preco_final:.2f}")
        st.info(f"📌 Valor do imposto aplicado: R$ {valor_imposto:.2f}")

    except ValueError as e:
        st.error(f"❌ Erro: {e}")
    except Exception:
        st.error("❌ Entrada inválida! Digite números válidos para taxa e custo.")
