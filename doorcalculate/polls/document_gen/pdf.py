from fpdf import FPDF, XPos, YPos, HTMLMixin
from xhtml2pdf import pisa
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

    # with pdf.table(col_widths=(15, 15, 10, 10, 10, 10, 10, 8, 15, 10, 10, 10, 5, 5, 5, 7, 7), text_align='CENTER', first_row_as_headings=True) as table:
    #     header_row = table.row()
    #     for key in data.keys():
    #         header_row.cell(key)
            
    #     for row_d in zip(*data.values()):
    #         row = table.row()
    #         for cell_d in row_d:
    #             row.cell(str(cell_d))

    # full_sum = sum(map(int, list(data.values())[-1]))
    # text = f'Всего за дверные блоки: {full_sum} грн'
    # pdf.set_xy(pdf.w-72, pdf.get_y()+3)
    # pdf.set_font('Roboto', 'B', 10)    
    # pdf.cell(txt=text, new_y=YPos.NEXT)
    # text = 'Скидка 30%'
    # pdf.set_x(pdf.w-30)
    # pdf.cell(txt=text, new_y=YPos.NEXT)
    # text = f'Всего, с учётом скидки: {math.ceil(full_sum*0.7)} грн'
    # pdf.set_x(pdf.w-70)
    # pdf.cell(txt=text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    # x = pdf.get_x()
    # y = pdf.get_y()
    # pdf.image(w=100, name='polls/static/media/External opening.PNG')
    # pdf.image(w=100, name='polls/static/media/Internal opening.PNG', x=x+110, y=y)
        
    html_code = """
    <table id="table"> <thead> <tr> <th class="cell" rowspan="3">Модель</th> <th class="cell td-opening" colspan="2" rowspan="3">Открывание</th> <th class="cell vertical" rowspan="3">Сторона</th> <th class="cell" colspan="2" rowspan="2">Габариты полотна</th> <th class="cell" colspan="2" rowspan="2">Габариты короба</th> <th class="cell" colspan="2" rowspan="2">Габариты проема</th> <th class="cell" rowspan="3">Отделки полотна и комплектации</th> <th class="cell" rowspan="3">Тип короба</th> <th class="cell" rowspan="3">Алюминиевый обвяз полотна</th> <th class="cell" rowspan="3">Цвет покраски профиля и короба</th> <th class="cell" rowspan="3">Цвет уплотнителя</th> <th class="cell vertical" rowspan="3">Сторона</th> <th class="cell" colspan="4" rowspan="1">Врезка</th> <th class="cell vertical" rowspan="3">Количество</th> <th class="cell" rowspan="2">Цена</th> <th class="cell" rowspan="2">Всего</th> <th class="cell remove" rowspan="3">Удалить</th></tr> <tr> <th class="cell" colspan="3">Отверствия</th> <th class="cell" rowspan="2">Петли</th> </tr> <tr> <th class="cell" rowspan="1">Ширина мм <br>лицо\тыл</th> <th class="cell">Высота мм <br>лицо\тыл</th> <th class="cell">Ширина мм</th> <th class="cell">Высота мм</th> <th class="cell">Ширина мм</th> <th class="cell">Высота мм</th> <th class="cell">ручка</th> <th class="cell">WC</th> <th class="cell">PZ</th> <th class="cell">грн</th> <th class="cell">грн</th> </tr> </thead> <tbody> <tr> <td class="cell" rowspan="2"> <span>Multistrato</span> </td> <td class="cell td-opening" rowspan="2"> <span>Левое</span> </td> <td class="cell" rowspan="2"> <span>Наружное</span> </td> <td class="cell"> <span>лицо</span> </td> <td class="cell"> <span>920</span> </td> <td class="cell"> <span>2100</span> </td> <td class="cell" rowspan="2"> <span>972</span> </td> <td class="cell" rowspan="2"> <span>2134</span> </td> <td class="cell" rowspan="2"> <span>952</span> </td> <td class="cell" rowspan="2"> <span>2124</span> </td> <td class="cell" rowspan="2"> <span>Ламинатин</span> </td> <td class="cell" rowspan="2"> <span>Slim Light</span> </td> <td class="cell" rowspan="2"> <span>-</span> </td> <td class="cell" rowspan="2"> <span>Аннодированый</span> </td> <td class="cell" rowspan="2"> <span>Серый</span> </td> <td class="cell"> <span>лицо</span> </td> <td class="cell"> <span>+</span> </td> <td class="cell"> <span>+</span> </td> <td class="cell"> <span>+</span> </td> <td class="cell" rowspan="2"> <span>2</span> </td> <td class="cell count" rowspan="2"> <span>1</span> </td> <td class="cell" rowspan="2"> <span>11490</span> </td> <td class="cell total-price" rowspan="2"> <span>11490</span> </td> <td rowspan="2"><button type="button" class="remove-button">Удалить дверь</button></td></tr><tr> <td class="cell"> <span>тыл</span> </td> <td class="cell"> <span>920</span> </td> <td class="cell"> <span>2100</span> </td> <td class="cell"> <span>тыл</span> </td> <td class="cell"> <span>+</span> </td> <td class="cell"> <span>+</span> </td> <td class="cell"> <span>+</span> </td> </tr></tbody> </table>
    """
    pdf.write_html(html_code)

    with io.BytesIO() as buffer:
        pdf.output(buffer)
        return buffer.getvalue()





