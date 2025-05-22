from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        pass  # puedes agregar un encabezado si quieres

def generar_pdf_por_codigo(codigo, df_filtrado, output_dir):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)

    # Título con el nombre de la empresa
    empresa = df_filtrado["EMPRESA"].iloc[0]

    
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, f"{empresa}", ln=True, align="C")

    pdf.set_font("Arial", "", 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"NCODIGOPJ: {codigo}", ln=True, align="C")
    pdf.ln(5)

    # --- Configuración de tabla ---
    pdf.set_font("Arial", "B", 8)
    pdf.set_fill_color(200, 255, 200)  # verde claro
    pdf.set_text_color(0, 0, 0)

    columnas = ["APELLIDOS Y NOMBRES", "EMAIL", "PERFIL", "CARGOS", "FECHA INICIAL", "FECHA VENC CERTIFICADO"]
    anchos = [60, 60, 40, 60, 30, 40]

    # Encabezados con multi_cell
    x_start = pdf.get_x()
    y_start = pdf.get_y()
    max_header_height = 0

    for i, col in enumerate(columnas):
        pdf.set_xy(x_start + sum(anchos[:i]), y_start)
        pdf.multi_cell(anchos[i], 5, col, border=0.5, align="C", fill=True)
        max_header_height = max(max_header_height, pdf.get_y() - y_start)

    pdf.set_y(y_start + max_header_height)

    # --- Cuerpo ---
    pdf.set_font("Arial", "", 7)
    pdf.set_text_color(0, 0, 0)

    for _, fila in df_filtrado.iterrows():
        valores = [
            str(fila["APELLIDOS Y NOMBRES"]),
            str(fila["EMAIL"]),
            str(fila["PERFIL"]),
            str(fila["CARGOS"]).replace("<BR>", ", "),
            str(fila["FECHA INICIAL"])[:10],
            str(fila["FECHA VENC CERTIFICADO"])[:10],
        ]

        line_heights = []
        for i, val in enumerate(valores):
            texto = val.strip()
            ancho = anchos[i]
            num_lineas = max(1, len(pdf.multi_cell(ancho, 4.5, texto, border=0, align="J", split_only=True)))
            line_heights.append(num_lineas * 4.5)

        max_height = max(line_heights)
        x = pdf.get_x()
        y = pdf.get_y()

        for i, val in enumerate(valores):
            pdf.set_xy(x + sum(anchos[:i]), y)
            pdf.multi_cell(anchos[i], 4.5, val.strip(), border=0.5, align="J")

        pdf.set_y(y + max_height)

    # Guardar PDF
    nombre_pdf = f"{codigo}.pdf"
    ruta_pdf = os.path.join(output_dir, nombre_pdf)
    pdf.output(ruta_pdf)

    return ruta_pdf

