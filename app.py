
import streamlit as st
import pandas as pd
from utils.generar_pdf import generar_pdf
import os

st.set_page_config(page_title="Generador de Certificados SMV", layout="centered")

st.image("logo_smv.png", width=120)  # Logo SMV

st.markdown("## Generador de Certificados por NCODIGOPJ")
st.markdown('<p style="color:gray; font-size:10px;">Hecho por Juan S.</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    codigos_unicos = df['NCODIGOPJ'].unique()

    st.success(f"Se encontraron {len(codigos_unicos)} códigos únicos.")

    for codigo in codigos_unicos:
        datos = df[df['NCODIGOPJ'] == codigo]
        nombre_pdf = f"certificado_{codigo}.pdf"
        generar_pdf(datos, nombre_pdf, codigo)
        with open(nombre_pdf, "rb") as f:
            st.download_button(
                label=f"📄 Descargar PDF para NCODIGOPJ {codigo}",
                data=f,
                file_name=nombre_pdf,
                mime='application/pdf'
            )
        os.remove(nombre_pdf)  # Limpieza del archivo local
