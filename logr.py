from openpyxl import Workbook
from openpyxl import load_workbook
import time

wb = load_workbook(filename="Log.xlsx")

ws = wb["Sheet1"]

def check(id):
    r = 0
    rows = list(ws.iter_rows(min_row=2, max_row=ws.max_row))
    rows = reversed(rows)
    for row in rows:
        if row[0].value == id and row[2].value is None:
            r = row[0].row
            break
    return r

def log(id, img_path, r):
    i = 0
    if r == 0:            
        ws.cell(row=ws.max_row+1, column=1).value = id
        ws.cell(row=ws.max_row, column=2).value = time.ctime(time.time())
        ws.cell(row=ws.max_row, column=4).value = img_path
    else:
        ws.cell(row=r, column=3).value = time.ctime(time.time())
        ws.cell(row=r, column=5).value = img_path
        i = 1

    wb.save("Log.xlsx")

    return i