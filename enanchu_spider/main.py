# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import bs4
import urllib.request
import urllib.error
import re
import os.path
import http.cookiejar
import nanchu_data

class KeyValueItem:
    key: str
    value: str
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value


baseDir: str = "./enanchu_spider/target"
baseUrl: str = "http://www.enanchu.com/historyQuote.shtml"
# todo: cookie需要更新, 需要建立更新机制
Cookie: str = "JSESSIONID=node0tffg0w9xxtbi1valaexz4et3x100564.node0"
foshan_area_code: KeyValueItem = KeyValueItem("quote.area", "4")


def main():
    intiDir()
    getFoShanData()


def getFoShanData():
    params: dict[str, str] = {
        foshan_area_code.key : foshan_area_code.value,
        "quote.commodityName": "22_"
    }
    dataCollector: nanchu_data.NanchuDataCollector = nanchu_data.NanchuDataCollector()
    pageSize: int = 10
    currentPage: int = 1
    while currentPage <= 100:
        data_list: list[nanchu_data.NanChuDataItem] = getData(currentPage, pageSize, params)
        dataCollector.dataCollect(data_list)
        currentPage += 1
    dataCollector.save(baseDir, "南储佛山-重熔铝锭")


def intiDir():
    if not os.path.exists(baseDir):
        os.makedirs(baseDir)


def askURL(currentPage: int, pageSize: int, params: dict[str, str]) -> str:
    url: str = baseUrl + "?"
    url += url + "pageView.currentPage=" + str(currentPage) + "&" + "pageView.pageSize=" + str(pageSize) + "&"
    for key, value in params.items():
        url += key + "=" + value + "&"
    url = url[:-1]

    headers: dict = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.enanchu.com",
        "Upgrade-Insecure-Requests": 1,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        "Refer" : "http://www.enanchu.com/historyQuote.shtml?pageView.currentPage=2&pageView.pageSize=10&quote.area=4&quote.commodityName=22_&beginDate=&endDate=",
        "Cookie": Cookie
    }
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


def getData(currentPage: int, pageSize: int, params: dict[str, str]) -> list[nanchu_data.NanChuDataItem]:
    data_item_list: list[nanchu_data.NanChuDataItem] = []
    html = askURL(currentPage, pageSize, params)
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all("div", class_="scroll_table"):
        for tr in item.find_all("tr"):
            data_item_list.append(getDataItem(tr))

    return data_item_list


def getDataItem(tag: bs4.element.Tag) -> nanchu_data.NanChuDataItem:
    date_regexp = re.compile(r'<td width="14%">(.*)</td>', re.S)
    date_sub_regexp = re.compile(r'\n(.*)\r\n<!--', re.S)
    td_list = tag.find_all("td")
    if (len(td_list) == 0):
        return None
    else:
        # for t in td_list:
        #     print(str(t) + "\n")
        item: nanchu_data.NanChuDataItem = nanchu_data.NanChuDataItem()
        item.category = td_list[0].string
        item.tradeMark = td_list[1].string
        item.priceRange = td_list[2].string
        item.averagePrice = td_list[3].string
        item.change = td_list[4].string
        item.dateStr = re.findall(date_sub_regexp, re.findall(date_regexp, str(td_list[5]))[0])[0]
        return item


def saveTempFile(savePath: str, fileName: str, suffix: str, content: str):
    filePath = savePath + "/" + fileName + suffix
    f = open(filePath, "w", encoding="utf-8")
    f.write(content)
    f.flush()
    f.close()


if __name__ == "__main__":
    main()
