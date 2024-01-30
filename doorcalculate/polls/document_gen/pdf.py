from fpdf import FPDF, XPos, YPos
import io
import math

class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation='L')
        self.add_font('Roboto', '', 'polls/document_gen/fonts/Roboto-Light.ttf')
        self.add_font('Roboto', 'B', 'polls/document_gen/fonts/Roboto-Bold.ttf')
        self.set_font('Roboto', '', 8)
    
    def header(self):
        self.set_font('Roboto', '', 8)
        self.cell(0, 10, 'Table Example', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')


def create(data: dict):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Roboto', '', 6)

    with pdf.table(col_widths=(15, 15, 10, 10, 10, 10, 10, 8, 15, 10, 10, 10, 5, 5, 5, 7, 7), text_align='CENTER', first_row_as_headings=True) as table:
        header_row = table.row()
        for key in data.keys():
            header_row.cell(key)
            
        for row_d in zip(*data.values()):
            row = table.row()
            for cell_d in row_d:
                row.cell(str(cell_d))

    full_sum = sum(map(int, list(data.values())[-1]))
    text = f'Всего за дверные блоки: {full_sum} грн'
    pdf.set_xy(pdf.w-72, pdf.get_y()+3)
    pdf.set_font('Roboto', 'B', 10)    
    pdf.cell(txt=text, new_y=YPos.NEXT)
    text = 'Скидка 30%'
    pdf.set_x(pdf.w-30)
    pdf.cell(txt=text, new_y=YPos.NEXT)
    text = f'Всего, с учётом скидки: {math.ceil(full_sum*0.7)} грн'
    pdf.set_x(pdf.w-70)
    pdf.cell(txt=text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    x = pdf.get_x()
    y = pdf.get_y()
    pdf.image(w=100, name='polls/static/media/External opening.PNG')
    pdf.image(w=100, name='polls/static/media/Internal opening.PNG', x=x+110, y=y)

    with io.BytesIO() as buffer:
        pdf.output(buffer)
        return buffer.getvalue()




