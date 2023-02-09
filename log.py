from openpyxl import Workbook
from openpyxl import load_workbook
import time

wb = load_workbook(filename="Log.xlsx")

ws = wb["Sheet1"]


def login(text):
    i = 0
    for row in ws.iter_rows(min_row=2, min_col=1, max_row=ws.max_row, max_col=1):
        for cell in row:
            if cell.value == text and ws.cell(row=cell.row, column=3).value is None:
                i = 1
            else:
                i = 0
    if i == 0:            
        ws.cell(row=ws.max_row+1, column=1).value = text
        ws.cell(row=ws.max_row, column=2).value = time.ctime(time.time())
        wb.save("Log.xlsx")

def logout(text):
    for row in ws.iter_rows(min_row=2, min_col=1, max_row=ws.max_row, max_col=1):
        for cell in row:
            if cell.value == text and ws.cell(row=cell.row, column=3).value is None:
                ws.cell(row=cell.row, column=3).value = time.ctime(time.time())
                wb.save("Log.xlsx")
