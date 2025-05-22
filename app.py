import streamlit as st
import pandas as pd
from fpdf import FPDF
from io import BytesIO
import zipfile

st.set_page_config(page_title="Generador de PDFs en ZIP por Empresa", layout="centered")
st.title("📄 Generador de PDFs agrupados por NCODIGOPJ y descargables en ZIP")

uploaded_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

def print_row_with_wrap(pdf, col_widths, data, line_height=5):
    # Calcular número de líneas por celda
    max_lines = 0
    lines_per_cell = []
    for i, text in enumerate(data):
        max_chars_per_line = int(col_widths[i] / 2.7)
        lines = (len(text) // max_chars_per_line) + 1
        lines_per_cell.append(lines)
        if lines > max_lines:
            max_lines = lines
    
    row_height = line_height * max_lines
    y_start = pdf.get_y()
    x_start = pdf.get_x()

    for i, text in enumerate(data):
        x_current = pdf.get_x()
        y_current = pdf.get_y()
        pdf.multi_cell(col_widths[i], line_height, text, border=1, align='L', fill=False)
        pdf.set_xy(x_current + col_widths[i], y_current)
    
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
                pdf = FPDF(orientation='L')  # Horizontal
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()

                # Título (nombre de la empresa)
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, f"{empresa}", ln=True, align="C")

                # Encabezado
                headers = ["APELLIDOS Y NOMBRES", "EMAIL", "PERFIL", "CARGOS", "FECHA INICIAL", "FECHA VENC CERTIFICADO"]
                col_widths = [60, 60, 50, 70, 35, 40]
                pdf.set_fill_color(0, 100, 0)  # Verde oscuro
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("Arial", 'B', 10)

                for i, header in enumerate(headers):
                    pdf.cell(col_widths[i], 10, header, border=1, ln=0, align='C', fill=True)
                pdf.ln()

                # Filas de datos
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

                # Exportar PDF a bytes y agregar al ZIP
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

