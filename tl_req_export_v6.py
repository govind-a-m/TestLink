# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 14:05:13 2019

@author: MLG1KOR
"""
from tl_class import testSuite,testcase
from recurse_tl_v3 import gm_get_nodes
from requests import session
from bs4 import BeautifulSoup
import xlsxwriter
import json
import xml.etree.ElementTree as ET
import sys


nodeid = '19272'
nodename = 'ADC'
start_req = 532
end_req = 537
export_filename = 'tc_req_ADC.xlsx'
req_filename = 'req3.2.xlsx'

idx = 0
rno=1
book=xlsxwriter.Workbook(export_filename)
sheet=book.add_worksheet()
wrap=book.add_format({'text_wrap':True})
with open('database.json','r+') as fjson:
    data = json.load(fjson)
payload =  data['payload']
exp_payload = data['exp_payload']
exp_url = data['exp_url']
book=xlsxwriter.Workbook(export_filename)
sheet=book.add_worksheet()
wrap=book.add_format({'text_wrap':True})

def gm_lastChild(suite):
  global nodes
  parent = suite
  nth_child = parent.nof_children-1
  while nth_child>-1:
    if nodes[parent.children[nth_child]].tcase:
      nth_child = nth_child-1
    else:
      parent = nodes[parent.children[nth_child]]
      nth_child = parent.nof_children-1
  return parent.children[-1]

def indexof(lc,index):
  global suite,lastchild
  for i in range(index,len(node_list)):
    if node_list[i].node_id==lc:
      return i
    
def buildTestSpec():
  global suite,node_list,nodes,c,idx,tc,testSpec
  testSpec = testSuite(suite.name,[])
  lastchild = gm_lastChild(suite)
  for index in range(idx,len(node_list)):
    if node_list[index].tcase:
      if node_list[index].node_id==lastchild:
        tc_url='http://10.58.199.163:8025/testlink-1.9.16/lib/testcases/archiveData.php?edit=testcase&id='+node_list[index].node_id
        tc=c.get(tc_url)
        soup=BeautifulSoup(tc.content)
        testcase.fromHTML(testSpec,soup,node_list[index].internal_id,node_list[index].name)
        return index+1
        break
      tc_url='http://10.58.199.163:8025/testlink-1.9.16/lib/testcases/archiveData.php?edit=testcase&id='+node_list[index].node_id
      tc=c.get(tc_url)
      soup=BeautifulSoup(tc.content)
      testcase.fromHTML(testSpec,soup,node_list[index].internal_id,node_list[index].name)

def write_data(spec):
  global rno,sheet
  for tcase in spec.testcases:
    sheet.write(rno,0,tcase.externalID)
    sheet.write(rno,1,tcase.cfield_data['TestCaseID'])
    sheet.write(rno,2,tcase.cfield_data['Requirement_ID'])
    sheet.write(rno,3,tcase.cfield_data['Test Classification'])
    sheet.write(rno,4,tcase.cfield_data['ASIL Level'])
    rno+=1

if 'nodes' not in globals():
  nodes = gm_get_nodes(payload['tl_login'],payload['tl_password'],nodeid,nodename)
  node_list = [value for key,value in nodes.items()]
skip_list = []
with session() as c:
  c.post("http://10.58.199.163:8025/testlink-1.9.16/login.php",data=payload)
  while idx<len(node_list):
    if node_list[idx].tcase:
      suite = nodes[node_list[idx].parent]
      if suite.nof_children<25:
        exp_payload["containerID"] = suite.node_id
        rsp=c.post(exp_url,params=exp_payload)
        if rsp.text=='':
          try:
            idx = buildTestSpec()
            write_data(testSpec)
          except Exception as e:
            lastchild = gm_lastChild(suite)
            idx = indexof(lastchild,idx)+1
            skip_list.append(suite)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        else:
          root = ET.fromstring(rsp.text)
          testSpec = testSuite.fromXML(root)
          write_data(testSpec)
          lastchild = gm_lastChild(suite)
          idx = indexof(lastchild,idx)+1
      else:
        try:
          idx = buildTestSpec()
          write_data(testSpec)
        except Exception as e:
          lastchild = gm_lastChild(suite)
          idx = indexof(lastchild,idx)+1
          skip_list.append(suite)
          print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)        
    else:
      idx+=1            
book.close()