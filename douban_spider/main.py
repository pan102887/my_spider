# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt

class Data_item:
    link: str
    imgSrc: str
    ctitle: str
    otitle: str
    rating: str
    judgeNum: str
    inq: str
    bd: str

findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)
basePath = "./douban_spider/target"


def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    savepath = basePath + "/豆瓣电影Top250.xls"
    saveData(datalist, savepath)
    


def getData(baseUrl: str) -> list[Data_item]:
    data_item_list: list[Data_item] = []

    for i in range(0, 10):
        url = baseUrl + str(i * 25)
        html = askURL(url)
        save_temp(str(html), str(i * 25) + ".html")
        soup = BeautifulSoup(html, "html.parser")

        count: int = 0
        for item in soup.find_all('div', class_='item'):
            data_item: Data_item = Data_item()
            
            item = str(item)
            save_temp(item, str(i * 25) + "_" + str(count)+".html")
            count += 1

            link = re.findall(findLink, item)[0]    
            data_item.link = link

            imgSrc = re.findall(findImgSrc, item)[0]    
            data_item.imgSrc = imgSrc

            titles = re.findall(findTitle, item)
            if (len(titles) == 2):
                ctitle = titles[0]        
                data_item.ctitle = ctitle

                otitle = titles[1].replace("/", "")        
                data_item.otitle = otitle
            else:                
                data_item.ctitle = titles[0]
                data_item.otitle = ' '

            rating = re.findall(findRating, item)[0]    
            data_item.rating = rating

            judgeNum = re.findall(findJudge, item)[0]    
            data_item.judgeNum = judgeNum

            inq = re.findall(findInq, item)
            if (len(inq) != 0):
                inq = inq[0].replace("。", "")        
                data_item.inq = inq
            else:        
                data_item.inq = " "

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?', "", bd)
            rb = re.sub('/', "", bd)    
            data_item.bd = rb.strip()
            data_item_list.append(data_item)
    return data_item_list


def askURL(url: str):
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    req = urllib.request.Request(url, headers=head)
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


def saveData(datalist: list, savepath):
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True) #创建工作表
    col = ("电影详情链接","图片链接","影片中文名","影片外国名","评分","评价数","概况","相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])  #列名

    for i in range(0, len(datalist)):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data: Data_item = datalist[i]
        sheet.write(i+1, 0, data.link)
        sheet.write(i+1, 1, data.imgSrc)
        sheet.write(i+1, 2, data.ctitle)
        sheet.write(i+1, 3, data.otitle)
        sheet.write(i+1, 4, data.rating)
        sheet.write(i+1, 5, data.judgeNum)
        sheet.write(i+1, 6, data.inq)
        sheet.write(i+1, 7, data.bd)
    book.save(savepath)
    print("爬取完毕！")


def save_temp(temp: str, suffix: str):
    f = open(basePath + "/temp_" + suffix, "w", encoding="utf-8")
    f.write(temp)


if __name__ == "__main__":
    main()
    