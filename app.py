import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO
import zipfile
import os

st.set_page_config(page_title="Generador de PDFs", layout="centered")
st.title("📄 Generador de PDFs agrupados por NCODIGOPJ")

uploaded_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

def add_fixed_row(pdf, col_widths, data, is_header=False, height=10):
    x_start = pdf.get_x()
    y_start = pdf.get_y()

    if is_header:
        pdf.set_fill_color(0, 100, 0)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", 'B', 10)
    else:
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 9)

    for i, text in enumerate(data):
        cell_text = str(text)
        if len(cell_text) > 100:
            cell_text = cell_text[:97] + "..."
        pdf.multi_cell(col_widths[i], height / 2, cell_text, border=1, align='L', max_line_height=height / 2)
        pdf.set_xy(x_start + sum(col_widths[:i+1]), y_start)

    pdf.set_xy(x_start, y_start + height)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    if "NCODIGOPJ" not in df.columns:
        st.error("El archivo no contiene la columna 'NCODIGOPJ'")
    else:
        grouped = df.groupby(['NCODIGOPJ', 'EMPRESA'])
        n_codigos = len(grouped)
        st.success(f"Se generarán PDFs para **{n_codigos}** códigos únicos.")

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for (ncodigopj, empresa), grupo in grouped:
                pdf = FPDF(orientation='L')
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()

                # Logo
                if os.path.exists("logo_smv.png"):
                    pdf.image("logo_smv.png", x=10, y=8, w=30)

                # Título
                pdf.set_font("Arial", 'B', 16)
                pdf.ln(5)
                pdf.cell(0, 10, f"{empresa}", ln=True, align="C")
                pdf.ln(5)

                # Encabezado y columnas
                headers = ["APELLIDOS Y NOMBRES", "EMAIL", "PERFIL", "CARGOS", "FECHA INICIAL", "FECHA VENC CERTIFICADO"]
                col_widths = [50, 40, 50, 70, 35, 40]
                add_fixed_row(pdf, col_widths, headers, is_header=True, height=10)

                # Datos
                for _, row in grupo.iterrows():
                    data = [
                        str(row["APELLIDOS Y NOMBRES"]),
                        str(row["EMAIL"]),
                        str(row["PERFIL"]),
                        str(row["CARGOS"]).replace("<BR>", " / "),
                        str(row["FECHA INICIAL"]),
                        str(row.get("FECHA VENC CERTIFICADO", ""))
                    ]
                    add_fixed_row(pdf, col_widths, data, is_header=False, height=10)

                pdf_bytes = BytesIO(pdf.output(dest='S').encode('latin1'))
                filename = f"{ncodigopj}.pdf"
                zip_file.writestr(filename, pdf_bytes.read())

        zip_buffer.seek(0)
        st.download_button(
            label="📥 Descargar ZIP con todos los PDFs",
            data=zip_buffer,
            file_name="PDFs_empresas.zip",
            mime="application/zip"
        )
