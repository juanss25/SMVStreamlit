from fpdf import FPDF

def generar_pdf(datos, nombre_archivo, codigo):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)

    # Título con el nombre de la empresa
    empresa = datos["EMPRESA"].iloc[0]
    pdf.set_text_color(0, 70, 127)  # Azul SMV
    pdf.cell(0, 10, f"EMPRESA: {empresa}", ln=True, align="C")

    # Encabezados de la tabla
    pdf.set_font("Arial", "B", 10)  # fuente más pequeña
    pdf.set_fill_color(200, 255, 200)  # Verde claro
    pdf.set_text_color(0, 0, 0)  # Negro
    
    columnas = ["APELLIDOS Y NOMBRES", "EMAIL", "PERFIL", "CARGOS", "FECHA INICIAL", "FECHA VENC CERTIFICADO"]
    anchos = [60, 60, 40, 60, 30, 40]
    
    x_start = pdf.get_x()
    y_start = pdf.get_y()
    max_header_height = 0

# Calcular altura máxima del encabezado
for i, col in enumerate(columnas):
    pdf.set_xy(x_start + sum(anchos[:i]), y_start)
    pdf.multi_cell(anchos[i], 4, col, border=0.5, align="C", fill=True)
    max_header_height = max(max_header_height, pdf.get_y() - y_start)

# Ajustar posición después del encabezado
pdf.set_y(y_start + max_header_height)

    # Cuerpo de la tabla
pdf.set_font("Arial", "", 7)

for _, fila in datos.iterrows():
    valores = [
        str(fila["APELLIDOS Y NOMBRES"]),
        str(fila["EMAIL"]),
        str(fila["PERFIL"]),
        str(fila["CARGOS"]).replace("<BR>", ", "),
        str(fila["FECHA INICIAL"])[:10],
        str(fila["FECHA VENC CERTIFICADO"])[:10],
    ]

    # Calcular la altura máxima necesaria por fila
    line_heights = []
    for i, val in enumerate(valores):
        # MultiCell nos da control para obtener altura requerida
        pdf.set_xy(pdf.get_x(), pdf.get_y())
        line_heights.append(pdf.get_string_width(val) / (anchos[i] - 1) * 2.5)

    max_height = max(line_heights)

    x_start = pdf.get_x()
    y_start = pdf.get_y()

    for i, val in enumerate(valores):
        pdf.set_xy(x_start + sum(anchos[:i]), y_start)
        pdf.multi_cell(anchos[i], 4, val, border=0.5, align="J")

    pdf.set_y(y_start + max_height + 2)

    # Guardar PDF
    pdf.output(nombre_archivo)

