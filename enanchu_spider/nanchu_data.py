# -*- coding: utf-8 -*-

import xlwt

class NanChuDataItem:
    category: str
    tradeMark: str
    priceRange: str
    averagePrice: str
    change: str
    dateStr: str


class NanchuDataCollector:
    book: xlwt.Workbook
    sheet: xlwt.Worksheet
    currentRow: int

    def __init__(self):
        self.book = xlwt.Workbook(encoding="utf-8",style_compression=0)
        self.sheet = self.book.add_sheet('重熔用铝锭', cell_overwrite_ok=True)
        col = ("品名","牌号","价格区间","均价","涨跌","日期")
        self.currentRow = 0
        for i in range(len(col)):
            self.sheet.write(self.currentRow, i, col[i])
        self.currentRow += 1

    def dataCollect(self, datalist: list[NanChuDataItem]):
        for i in range(len(datalist)):
            data: NanChuDataItem = datalist[i]
            self.sheet.write(self.currentRow, 0, data.category)
            self.sheet.write(self.currentRow, 1, data.tradeMark)
            self.sheet.write(self.currentRow, 2, data.priceRange)
            self.sheet.write(self.currentRow, 3, data.averagePrice)
            self.sheet.write(self.currentRow, 4, data.change)
            self.sheet.write(self.currentRow, 5, data.dateStr)
            self.currentRow += 1

    def save(self, savePath: str):
        book_path = savePath + "/" + "重熔用铝锭" + ".xls"
        self.book.save(book_path)