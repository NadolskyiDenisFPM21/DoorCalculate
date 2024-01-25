from datetime import datetime
import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo
import io

def create(data):
    # Создаем новую книгу и активный лист
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Записываем заголовки
    headers = list(data.keys())
    for col_num, header in enumerate(headers, 1):
        sheet.cell(row=1, column=col_num, value=header)

    # Записываем данные
    for row_num, row_data in enumerate(zip(*data.values()), 2):
        for col_num, cell_value in enumerate(row_data, 1):
            sheet.cell(row=row_num, column=col_num, value=cell_value)

    # Добавляем объект таблицы
    table = Table(displayName="MyTable", ref=sheet.dimensions)
    style = TableStyleInfo(
        name="TableStyleMedium9", showFirstColumn=False,
        showLastColumn=False, showRowStripes=False, showColumnStripes=False)
    table.tableStyleInfo = style
    sheet.add_table(table)


    with io.BytesIO() as buffer:
        workbook.save(buffer)
        return buffer.getvalue()
        
        
    