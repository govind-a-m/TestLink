# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 09:09:57 2019

@author: mlg1kor
"""
import json
from requests import *
from bs4 import BeautifulSoup
import xlsxwriter

book=xlsxwriter.Workbook('tc_req_bridgedrv.xlsx')
sheet=book.add_worksheet()
wrap=book.add_format({'text_wrap':True})
url="http://10.58.199.163:8025/testlink-1.9.16/login.php"
payload={"tl_login":"Govind","tl_password":"depin","CSRFName":"CSRFGuard_2113925045","CSRFToken":"d661b4dfa16c21a9b594d95cce0d4e6d52ab254ec490afd357332093b6858d7c38f405c8803e263a23033fc2fa8519dbeb7b5838bfd9e05dffb5ab2c3dd1bacb","action":"login.php?viewer=" }
rno=1
nodeid='17422'

with session() as c:
    c.post("http://10.58.199.163:8025/testlink-1.9.16/login.php",data=payload)
    q=c.get('http://10.58.199.163:8025/testlink-1.9.16/lib/ajax/gettprojectnodes.php?root_node=1&tcprefix=TS-&node='+nodeid)

with open('bridgedrv.json','w') as f:
   f.write(q.text)

with open('bridgedrv.json','r+') as fjson:
    data=json.load(fjson)
    with session() as c:
        c.post("http://10.58.199.163:8025/testlink-1.9.16/login.php",data=payload)
        for tcase in data:
            tc_url='http://10.58.199.163:8025/testlink-1.9.16/lib/testcases/archiveData.php?edit=testcase&id='+tcase['id']
            tc=c.get(tc_url)
            #print(tc_url)
            soup=BeautifulSoup(tc.content)
            cfields=soup.select('#cfields_design_time')
            c_rows=cfields[0].table.find_all('tr')
            tid=c_rows[0].find_all('td')[1].text
            rid=c_rows[1].find_all('td')[1].text
            sheet.write(rno,6,tid,wrap)
            sheet.write(rno,7,rid,wrap)
            print(tid,rid,rno)
            rno=rno+1
book.close()