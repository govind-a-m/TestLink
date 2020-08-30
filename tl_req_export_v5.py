# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 14:50:12 2019

@author: mlg1kor
"""

from recurse_tl_v3 import gm_get_nodes
from map_req_v3 import map_req
from dxl_prepare import create_text_file
from requests import session
from bs4 import BeautifulSoup
import xlsxwriter
import time 
import json

with open('tl_login_info.json','r+') as fjson:
    lg_info = json.load(fjson)
nodeid = '26263'
nodename = 'escooter_hw'
start_req = 1172
end_req = 1182
export_filename = 'tc_req_hw.xlsx'
req_filename = r'U:\req3.1.xlsx'

rno=1
book=xlsxwriter.Workbook(export_filename)
sheet=book.add_worksheet()
wrap=book.add_format({'text_wrap':True})
payload={"tl_login":lg_info['username'],
         "tl_password":lg_info['password'],
         "CSRFName":"CSRFGuard_2113925045",
         "CSRFToken":"d661b4dfa16c21a9b594d95cce0d4e6d52ab254ec490afd357332093b6858d7c38f405c8803e263a23033fc2fa8519dbeb7b5838bfd9e05dffb5ab2c3dd1bacb",
         "action":"login.php?viewer=" }
#%%
if 'nodes' not in globals():
  nodes = gm_get_nodes(lg_info['username'],lg_info['password'],nodeid,nodename)
  node_list = [value for key,value in nodes.items()]
skip_list = ['None']
#%%
with session() as c:
    c.post("http://10.58.199.163:8025/testlink-1.9.16/login.php",data=payload)
    for testlink_node in node_list:
        if(testlink_node.tcase):
            tc_url='http://10.58.199.163:8025/testlink-1.9.16/lib/testcases/archiveData.php?edit=testcase&id='+testlink_node.node_id
            nth_try = 0
            while(True):
                try:
                    nth_try = nth_try+1
                    tc=c.get(tc_url)
                    soup=BeautifulSoup(tc.content)
                    cfields=soup.select('#cfields_design_time')
                    c_rows=cfields[0].table.find_all('tr')
                    tid=c_rows[0].find_all('td')[1].text
                    rid=c_rows[1].find_all('td')[1].text
                    tcls  = c_rows[2].find_all('td')[1].text
                    asil = c_rows[3].find_all('td')[1].text
                    break
                except:
                    if(nth_try<4):
                        print("trying {} time".format(nth_try))
                        time.sleep(15)
                    else :
                      print('skipped {}'.format(testlink_node.name))
                      skip_list.append(testlink_node)
                      break
            if skip_list[-1] is testlink_node:
              continue
            sheet.write(rno,0,testlink_node.internal_id,wrap)
            sheet.write(rno,1,tid,wrap)
            sheet.write(rno,2,rid,wrap)
            sheet.write(rno,3,tcls,wrap)
            sheet.write(rno,4,asil,wrap)
            print(tid,rid,tcls,asil,rno,len(node_list),testlink_node.node_id)
            rno=rno+1
            print('--------------------------')
book.close()
##%%
#map_req(export_filename,req_filename,start_req,end_req)
##%%
#create_text_file()