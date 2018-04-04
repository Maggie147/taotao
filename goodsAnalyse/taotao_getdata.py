# coding: utf-8
# python3.5
__author__ = 'green'

import re
import time
import requests
import pandas as pd
from retrying import retry
from concurrent.futures import ThreadPoolExecutor

# 计时开始
start = time.clock()

# plist 为1-100页的URL编号的num
plist = []
for i in range(1, 101):
    j = 44*(i-1)
    plist.append(j)

listno = plist
datatmsp= pd.DataFrame(columns=[])

while True:
    @retry(stop_max_attempt_number=8)
    def network_programming(num):
        url="https://s.taobao.com/search?q=%E6%B2%99%E5%8F%91&imgfile=&commend=all&\
ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&\
ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc&fs=1&filter_tianmao=tmall&\
filter=reserve_price%5B500%2C%5D&bcoffset=0&p4ppushleft=%2C44&s="+str(num)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'}

        # print(url)
        web = requests.get(url.strip(), headers= headers)
        web.encoding = 'utf-8'
        return web

    def multithreading():
        number = listno
        event = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            for result in executor.map(network_programming,
                                        number, chunksize=10):
                event.append(result)
        return event

    # 记录每次成功爬取页码
    listpg = []
    event = multithreading()
    for i in event:
        json = re.findall('"auctions":(.*?),"recommendAuctions"', i.text)

        if len(json):
            table = pd.read_json(json[0])
            datatmsp = pd.concat([datatmsp, table],
                                axis=0, ignore_index=True)
            pg = re.findall('"pageNum":(.*?),"p4pbottom_up"', i.text)[0]
            listpg.append(pg)

    # 架构爬取成功的页码转为url中的num值
    lists = []
    for a in listpg:
        b = 44*(int(a)-1)
        lists.append(b)

    # 将本次爬取失败的页记录列表中，用于循环爬取
    listn = listno
    listno =[]
    for p in listn:
        if p not in lists:
            listno.append(p)

    if len(listno) ==0:
        break

# 导出数据为Excel
datatmsp.to_excel('datatmsp.xls', index= False)

# 计时结束
end = time.clock()
print("爬去用时: ", end-start, 's')