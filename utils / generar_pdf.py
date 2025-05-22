
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 102, 204)  # Azul claro
        self.cell(0, 10, "Superintendencia del Mercado de Valores", ln=True, align='C')
        self.ln(5)

def generar_pdf(data, filename, codigo):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(0, 0, 0)

    pdf.cell(0, 10, f"Certificado para NCODIGOPJ: {codigo}", ln=True)

    for index, row in data.iterrows():
        pdf.ln(5)
        nombres = row['APELLIDOS Y NOMBRES']
        cargo = row['CARGOS']
        vencimiento = row['FECHA VENC CERTIFICADO']
        pdf.multi_cell(0, 10, f"Nombre: {nombres}\nCargo: {cargo}\nVence: {vencimiento}", border=0)

    pdf.output(filename)
