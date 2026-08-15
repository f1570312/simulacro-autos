import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AutoAndes Import")
st.title("Análisis de eficiencia de autos")

@st.cache_data
def cargar_datos():
    return pd.read_csv("data/autos_limpio.csv")

df = cargar_datos()

origenes = ["(todos)"] + sorted(df["origin"].unique().tolist())
origen = st.sidebar.selectbox("Origen", origenes)

peso_maximo = st.sidebar.slider(
    "Peso máximo",
    int(df["weight"].min()),
    int(df["weight"].max()),
    int(df["weight"].max())
)

df_filtrado = df[df["weight"] <= peso_maximo]

if origen != "(todos)":
    df_filtrado = df_filtrado[df_filtrado["origin"] == origen]

if len(df_filtrado) == 0:
    st.warning("No hay autos para los filtros seleccionados.")
    st.stop()

st.metric("Número de autos", len(df_filtrado))
st.metric("MPG promedio", round(df_filtrado["mpg"].mean(), 2))
st.metric("Peso promedio", round(df_filtrado["weight"].mean(), 2))

fig, ax = plt.subplots()
ax.scatter(df_filtrado["weight"], df_filtrado["mpg"])
ax.set_xlabel("Weight")
ax.set_ylabel("MPG")
ax.set_title("Weight vs MPG")

st.pyplot(fig)