# -*- coding: utf-8 -*-
from lxml import etree
import requests
import time
import math

content = requests.get("https://xyq.netease.com/thread-1302818-1-1.html?refer_site=chatbot")
content.encoding = 'gb2312'

html = etree.HTML(content.text)
trs = html.xpath("//table[@class='t_table']/tr")
#print(trs)
num = 0
server = {}
for li in trs:
    num += 1
    if num > 1:
        td_num = len(li.xpath("./td/text()"))
        #print(td_num)
        td_text = li.xpath("./td/text()")
        #print(td_text)


        if td_num==3:
            #print(td_text[2].find('-')==-1)
            if (td_text[2].find('-') == -1):
                break
            server[td_text[0]] = math.floor((int(time.time()) - int(time.mktime(time.strptime(td_text[2], "%Y-%m-%d"))))/(3600*24*365))
            if len(server)==0:
                break
        if td_num==2:
            print(td_text)
        #server_list.append(server)

print(server)

