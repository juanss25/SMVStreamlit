import streamlit as st
import pandas as pd
import os
import tempfile
import shutil
import zipfile
from utils.generar_pdf import generar_pdf_por_codigo

st.set_page_config(page_title="Generador de PDFs SMV", layout="wide")

# Estilo personalizado con firma sutil y colores
st.markdown("""
    <style>
        .main {
            background-color: #f4fcf7;
        }
        footer::after {
            content: "Hecho por Juan S.";
            font-size: 10px;
            color: #ccc;
            display: block;
            text-align: right;
            margin: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📄 Generador de Certificados PDF por Empresa")
st.markdown("Sube un archivo Excel con datos y genera PDFs por cada empresa (`NCODIGOPJ`).")

uploaded_file = st.file_uploader("📤 Sube tu archivo Excel", type=["xlsx", "xls"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # ✅ LIMPIEZA DE DATOS PARA EVITAR ERRORES
        df.columns = df.columns.str.strip()  # Quita espacios de los nombres de columnas
        df["NCODIGOPJ"] = df["NCODIGOPJ"].astype(str).str.strip()
        df["EMPRESA"] = df["EMPRESA"].astype(str).str.strip()
        df = df.dropna(subset=["NCODIGOPJ", "EMPRESA"])  # Elimina filas sin código ni empresa


        if "NCODIGOPJ" not in df.columns:
            st.error("❌ El archivo debe contener la columna 'NCODIGOPJ'")
        else:
            codigos = df["NCODIGOPJ"].dropna().astype(str).unique()
            st.success(f"✅ Se encontraron {len(codigos)} códigos únicos.")

            if st.button("📥 Generar PDFs"):
                with st.spinner("Generando PDFs..."):

                    temp_dir = tempfile.mkdtemp()
                    pdf_paths = []

                    for codigo in codigos:
                        datos_filtrados = df[df["NCODIGOPJ"] == codigo]
                    
                        if not datos_filtrados.empty:
                            pdf_path = generar_pdf_por_codigo(codigo, datos_filtrados, temp_dir)
                            pdf_paths.append(pdf_path)
                        else:
                            st.warning(f"⚠️ No se encontraron datos para el código {codigo}. Se omitió.")

                    # Crear ZIP
                    zip_path = os.path.join(temp_dir, "certificados.zip")
                    with zipfile.ZipFile(zip_path, "w") as zipf:
                        for path in pdf_paths:
                            zipf.write(path, os.path.basename(path))

                    with open(zip_path, "rb") as f:
                        st.download_button("📦 Descargar ZIP con todos los PDFs", f, file_name="certificados.zip")

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")

