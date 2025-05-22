import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO
import zipfile

st.set_page_config(page_title="Generador de PDFs en ZIP por Empresa", layout="centered")

st.title("📄 Generador de PDFs agrupados por NCODIGOPJ y descargables en ZIP")

uploaded_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    if "NCODIGOPJ" not in df.columns:
        st.error("El archivo no contiene la columna 'NCODIGOPJ'")
    else:
        grouped = df.groupby(['NCODIGOPJ', 'EMPRESA'])

        n_codigos = len(grouped)
        st.info(f"Se generarán PDFs para **{n_codigos}** códigos únicos NCODIGOPJ.")

        # Crear ZIP en memoria
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:

            for (ncodigopj, empresa), grupo in grouped:
                pdf = FPDF(orientation='L')
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()

                # Título empresa
                pdf.set_font("Arial", 'B', 16)
                pdf.set_text_color(70, 130, 180)
                pdf.cell(0, 10, f"{empresa}", ln=True, align="C")

                # Encabezado tabla
                headers = ["APELLIDOS Y NOMBRES", "EMAIL", "PERFIL", "CARGOS", "FECHA INICIAL", "FECHA VENC CERTIFICADO"]
                col_widths = [50, 40, 50, 60, 35, 35]

                pdf.set_fill_color(0, 100, 0)  # Verde oscuro
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("Arial", 'B', 8)

                for i, header in enumerate(headers):
                    pdf.cell(col_widths[i], 7, header, border=1, ln=0, align='C', fill=True)
                pdf.ln()

                # Filas con datos
                pdf.set_font("Arial", '', 8)
                for _, row in grupo.iterrows():
                    values = [
                        str(row["APELLIDOS Y NOMBRES"]),
                        str(row["EMAIL"]),
                        str(row["PERFIL"]),
                        str(row["CARGOS"]).replace("<BR>", " / "),
                        str(row["FECHA INICIAL"]),
                        str(row.get("FECHA VENC CERTIFICADO", ""))
                    ]
                    for i, value in enumerate(values):
                        pdf.cell(col_widths[i], 7, value[:40], border=1, ln=0)
                    pdf.ln()

                # Guardar PDF en bytes
                pdf_str = pdf.output(dest='S').encode('latin1')
                pdf_bytes = BytesIO(pdf_str)

                # Añadir PDF al ZIP
                safe_empresa = empresa.replace(" ", "_").replace("/", "-")
                filename = f"{ncodigopj}.pdf"
                zip_file.writestr(filename, pdf_bytes.read())

        zip_buffer.seek(0)

        st.download_button(
            label="📥 Descargar ZIP con todos los PDFs",
            data=zip_buffer,
            file_name="PDFs_empresas.zip",
            mime="application/zip"
        )
