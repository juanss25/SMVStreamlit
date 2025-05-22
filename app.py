import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO
import zipfile
import os

st.set_page_config(page_title="Generador de PDFs en ZIP por Empresa", layout="centered")
st.title("📄 Generador de PDFs agrupados por NCODIGOPJ y descargables en ZIP")

uploaded_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

def print_row_with_wrap(pdf, col_widths, data, line_height=5):
    max_lines = 0
    cell_lines = []
    for i, text in enumerate(data):
        max_chars_per_line = int(col_widths[i] / 2.7)
        lines = (len(text) // max_chars_per_line) + 1
        cell_lines.append(lines)
        if lines > max_lines:
            max_lines = lines

    row_height = max_lines * line_height
    x_start = pdf.get_x()
    y_start = pdf.get_y()

    for i, text in enumerate(data):
        x = pdf.get_x()
        y = pdf.get_y()

        # Guardar posición inicial
        pdf.multi_cell(col_widths[i], line_height, text, border=1, align='L')
        
        # Restaurar posición a la derecha de la celda anterior
        pdf.set_xy(x + col_widths[i], y)

    # Bajar a la siguiente fila
    pdf.set_xy(x_start, y_start + row_height)

def draw_header(pdf, col_widths, headers, line_height=5):
    pdf.set_fill_color(0, 100, 0)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 10)

    # Forzar misma altura en todas las celdas de encabezado
    max_lines = 1
    row_height = max_lines * line_height
    x_start = pdf.get_x()
    y_start = pdf.get_y()

    for i, header in enumerate(headers):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.multi_cell(col_widths[i], line_height, header, border=1, align='C', fill=True)
        pdf.set_xy(x + col_widths[i], y)

    pdf.set_xy(x_start, y_start + row_height)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    if "NCODIGOPJ" not in df.columns:
        st.error("El archivo no contiene la columna 'NCODIGOPJ'")
    else:
        grouped = df.groupby(['NCODIGOPJ', 'EMPRESA'])
        n_codigos = len(grouped)
        st.info(f"Se generarán PDFs para **{n_codigos}** códigos únicos NCODIGOPJ.")

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for (ncodigopj, empresa), grupo in grouped:
                pdf = FPDF(orientation='L')
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()

                # Agregar logo si existe
                if os.path.exists("logo_smv.png"):
                    pdf.image("logo_smv.png", x=10, y=8, w=30)

                # Título
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, f"{empresa}", ln=True, align="C")

                pdf.ln(10)

                headers = ["APELLIDOS Y NOMBRES", "EMAIL", "PERFIL", "CARGOS", "FECHA INICIAL", "FECHA VENC CERTIFICADO"]
                col_widths = [60, 60, 50, 70, 35, 40]

                draw_header(pdf, col_widths, headers, line_height=5)
                pdf.set_font("Arial", '', 9)

                for _, row in grupo.iterrows():
                    values = [
                        str(row["APELLIDOS Y NOMBRES"]),
                        str(row["EMAIL"]),
                        str(row["PERFIL"]),
                        str(row["CARGOS"]).replace("<BR>", " / "),
                        str(row["FECHA INICIAL"]),
                        str(row.get("FECHA VENC CERTIFICADO", ""))
                    ]
                    print_row_with_wrap(pdf, col_widths, values, line_height=5)

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
