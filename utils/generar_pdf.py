from fpdf import FPDF

def generar_pdf(datos, nombre_archivo, codigo):
    from fpdf import FPDF

def generar_pdf(datos, nombre_archivo, codigo):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)

    # Título con el nombre de la empresa
    empresa = datos["EMPRESA"].iloc[0]
    pdf.set_text_color(0, 70, 127)  # Azul SMV
    pdf.cell(0, 10, f"EMPRESA: {empresa}", ln=True, align="C")

    # Encabezados de la tabla
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(0, 0, 0)
    columnas = ["APELLIDOS Y NOMBRES", "EMAIL", "PERFIL", "CARGOS", "FECHA INICIAL", "FECHA VENC CERTIFICADO"]
    anchos = [60, 60, 40, 60, 30, 40]

    for i, col in enumerate(columnas):
        pdf.cell(anchos[i], 10, col, border=1, align="C")
    pdf.ln()

    # Cuerpo de la tabla
    pdf.set_font("Arial", "", 9)
    for _, fila in datos.iterrows():
        valores = [
            str(fila["APELLIDOS Y NOMBRES"]),
            str(fila["EMAIL"]),
            str(fila["PERFIL"]),
            str(fila["CARGOS"]).replace("<BR>", ", "),
            str(fila["FECHA INICIAL"])[:10],
            str(fila["FECHA VENC CERTIFICADO"])[:10],
        ]
        for i, val in enumerate(valores):
            pdf.cell(anchos[i], 10, val, border=1)
        pdf.ln()

    # Guardar PDF
    pdf.output(nombre_archivo)

