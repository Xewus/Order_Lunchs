from json.tool import main
import pandas as pd
import openpyxl as oxl

book = oxl.open('/home/slava/Downloads/f_02461ee939a0c896.xlsx', read_only=True)
sheet = book.active
def main():
    for row in range(1, sheet.max_row):
        print(row, sheet[row][2].value)

if __name__ == '__main__':
    main()