import streamlit as st
import pandas as pd
import tempfile
import os
from zipfile import ZipFile
from utils.generar_pdf import generar_pdf_por_codigo
st.set_page_config(page_title="Generador SMV", layout="centered")

st.image("logo_smv.png", width=120)
st.markdown("## Generador de Certificados por NCODIGOPJ")
st.markdown('<p style="color:gray; font-size:10px;">Hecho por Juan S.</p>', unsafe_allow_html=True)


uploaded_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Validar que tenga las columnas necesarias
    required_columns = [
        "NCODIGOPJ", "EMPRESA", "APELLIDOS Y NOMBRES", "EMAIL",
        "PERFIL", "CARGOS", "FECHA INICIAL", "FECHA VENC CERTIFICADO"
    ]
    if not all(col in df.columns for col in required_columns):
        st.error("El archivo Excel no tiene las columnas requeridas.")
    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "certificados_smv.zip")
            pdf_folder = os.path.join(tmpdir, "pdfs")
            os.makedirs(pdf_folder, exist_ok=True)

            # Agrupar por NCODIGOPJ
            for codigo, grupo in df.groupby("NCODIGOPJ"):
                nombre_pdf = f"{codigo}.pdf"
                ruta_pdf = os.path.join(pdf_folder, nombre_pdf)
                generar_pdf(grupo, ruta_pdf, codigo)

            # Crear el zip
            with ZipFile(zip_path, "w") as zipf:
                for filename in os.listdir(pdf_folder):
                    full_path = os.path.join(pdf_folder, filename)
                    zipf.write(full_path, arcname=filename)

            # Descargar
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="📦 Descargar todos los PDFs en ZIP",
                    data=f,
                    file_name="certificados_smv.zip",
                    mime="application/zip"
                )

