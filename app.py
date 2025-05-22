import pandas as pd
import streamlit as st
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="Generador de PDFs por Empresa", layout="wide")

st.title("📄 Generador de PDFs por NCODIGOPJ")
st.markdown("Sube un archivo Excel con datos y genera un PDF por empresa (`NCODIGOPJ`).")

uploaded_file = st.file_uploader("📁 Sube tu archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    if "NCODIGOPJ" not in df.columns:
        st.error("❌ El archivo debe contener una columna 'NCODIGOPJ'.")
    else:
        codigos = df["NCODIGOPJ"].unique()
        st.success(f"✅ Archivo cargado correctamente. Se encontraron {len(codigos)} empresas diferentes.")

        for codpj in codigos:
            grupo = df[df['NCODIGOPJ'] == codpj]

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.set_auto_page_break(auto=True, margin=15)

            # Cabecera
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, f"NCODIGOPJ: {codpj}", ln=True, align='C')
            pdf.set_font("Arial", size=12)

            # Cuerpo del PDF
            for index, row in grupo.iterrows():
                pdf.ln(5)
                pdf.multi_cell(0, 10,
                    f"Empresa: {row['EMPRESA']}\n"
                    f"Nombre: {row['APELLIDOS Y NOMBRES']}\n"
                    f"Tipo Doc: {row['TIPO_DOC']} - {row['NUMDOC']}\n"
                    f"Email: {row['EMAIL']}\n"
                    f"Teléfono: {row['TELEFONO']}\n"
                    f"Perfil: {row['PERFIL']}\n"
                    f"Fecha Inicial: {row['FECHA INICIAL']}\n"
                    f"Cargos: {row['CARGOS']}\n"
                    f"Vence Certificado: {row.get('FECHA VENC CERTIFICADO', 'No definido')}\n",
                    border=1
                )

            # Guardar PDF en memoria
            pdf_buffer = BytesIO()
            pdf.output(pdf_buffer)
            pdf_buffer.seek(0)

            st.download_button(
                label=f"📥 Descargar PDF - NCODIGOPJ {codpj}",
                data=pdf_buffer,
                file_name=f"NCODIGOPJ_{codpj}.pdf",
                mime="application/pdf"
            )
