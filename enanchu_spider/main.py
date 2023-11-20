# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import bs4
import urllib.request
import urllib.error
import xlwt
import re
import os.path


class Data_item:
    category: str
    tradeMark: str
    priceRange: str
    averagePrice: str
    change: str
    dateStr: str


baseDir: str = "./enanchu_spider/target"
demoUrl: str = "http://www.enanchu.com/historyQuote.shtml?pageView.currentPage=1&pageView.pageSize=10&quote.area=4&quote.commodityName=22_&beginDate=&endDate="
baseUrl: str = "http://www.enanchu.com/historyQuote.shtml"
Cookie: str = ""
currentPage: int = 1
pageSize: int = 10


def main():
    intiDir()
    data_list: list[Data_item] = getData(currentPage, pageSize)
    saveData(data_list, baseDir)


def intiDir():
    if not os.path.exists(baseDir):
        os.makedirs(baseDir)


def askURL(currentPage: int, pageSize: int) -> str:
    params: dict[str, str] = {
        "pageView.currentPage": str(currentPage),
        "pageView.pageSize=10": str(pageSize),
        "quote.area": "2",
        "quote.commodityName": "22_"
    }

    headers: dict[str, str] = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": Cookie,
        "Host": "www.enanchu.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    }

    url: str = baseUrl + "?"
    for key, value in params.items():
        url += key + "=" + value + "&"
    url = url[:-1]

    req = urllib.request.Request(url, headers=headers, method="GET")
    html = ""
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def getData(currentPage: int, pageSize: int) -> list[Data_item]:
    data_item_list: list[Data_item] = []
    html = askURL(currentPage, pageSize)
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all("div", class_="scroll_table"):
        for tr in item.find_all("tr"):
            data_item_list.append(getDataItem(tr))

    return data_item_list



def getDataItem(tag: bs4.element.Tag) -> Data_item:
    date_regexp = re.compile(r'<td width="14%">(.*)</td>', re.S)
    date_sub_regexp = re.compile(r'\n(.*)\r\n<!--', re.S)
    td_list = tag.find_all("td")
    if (len(td_list) == 0):
        return None
    else:
        # for t in td_list:
        #     print(str(t) + "\n")
        item: Data_item = Data_item()
        item.category = td_list[0].string
        item.tradeMark = td_list[1].string
        item.priceRange = td_list[2].string
        item.averagePrice = td_list[3].string
        item.change = td_list[4].string
        item.dateStr = re.findall(date_sub_regexp, re.findall(date_regexp, str(td_list[5]))[0])[0]
        return item



def saveData(datalist: list[Data_item], saveDirectory: str):
    date_list_length = len(datalist)

    if date_list_length == 0:
        return
    else:
        print("save.......")
        book = xlwt.Workbook(encoding="utf-8",style_compression=0)
        sheet = book.add_sheet('重熔用铝锭', cell_overwrite_ok=True)
        col = ("品名","牌号","价格区间","均价","涨跌","日期")
        for i in range(len(col)):
            sheet.write(0, i, col[i])

        for i in range(date_list_length):
            data: Data_item = datalist[i]
            sheet.write(i+1, 0, data.category)
            sheet.write(i+1, 1, data.tradeMark)
            sheet.write(i+1, 2, data.priceRange)
            sheet.write(i+1, 3, data.averagePrice)
            sheet.write(i+1, 4, data.change)
            sheet.write(i+1, 5, data.dateStr)
        book_path = saveDirectory + "/" + "重熔用铝锭" + ".xls"
        book.save(book_path)



def saveTempFile(savePath: str, fileName: str, suffix: str, content: str):
    filePath = savePath + "/" + fileName + suffix
    f = open(filePath, "w", encoding="utf-8")
    f.write(content)
    f.flush()
    f.close()

if __name__ == "__main__":
    main()
