from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Table Example', 0, 1, 'C')

    def chapter_title(self, num, label):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Row %d: %s' % (num, label), 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)

def create(data):
    pdf = PDF()
    pdf.add_page()

    # Create a table
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, text="Table Title", ln=True, align='C')
    pdf.ln(10)  # Add a line break


    pdf.output("table_example.pdf")
