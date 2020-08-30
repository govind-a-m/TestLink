# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 13:47:11 2019

@author: MLG1KOR
"""
from tl_class import testSuite,testcase
from recurse_tl_v3 import gm_get_nodes
import json
from requests import session
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import os
import sys

nodeid = '23580'
nodename = 'voltage_monitor'
with open('database.json','r+') as fjson:
    data = json.load(fjson)
payload =  data['payload']
exp_payload = data['exp_payload']
exp_url = data['exp_url']


if 'node_list' not in globals():
  nodes = gm_get_nodes(payload['tl_login'],payload['tl_password'],nodeid,nodename)
  node_list = [value for key,value in nodes.items()]
idx = 0
skip_list = []

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
        for nth_try in range(3):      
          tc=c.get(tc_url)
          if tc.text!='':
            break
          print(f'trying {nth_try+1} time')
        soup=BeautifulSoup(tc.content)
        testcase.fromHTML(testSpec,soup,node_list[index].internal_id,node_list[index].name)
        testSpec.write()
        return index+1
      tc_url='http://10.58.199.163:8025/testlink-1.9.16/lib/testcases/archiveData.php?edit=testcase&id='+node_list[index].node_id
      for nth_try in range(3):      
        tc=c.get(tc_url)
        if tc.text!='':
          break
        print(f'trying {nth_try+1} time')
      soup=BeautifulSoup(tc.content)
      testcase.fromHTML(testSpec,soup,node_list[index].internal_id,node_list[index].name)

os.chdir(r'C:\Users\mlg1kor\testspecs')
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
          except Exception as e:
            lastchild = gm_lastChild(suite)
            idx = indexof(lastchild,idx)+1
            skip_list.append(suite)
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        else:
          root = ET.fromstring(rsp.text)
          testSpec = testSuite.fromXML(root)
          testSpec.write()
          lastchild = gm_lastChild(suite)
          idx = indexof(lastchild,idx)+1
      else:
        try:
          idx = buildTestSpec()
        except Exception as e:
          lastchild = gm_lastChild(suite)
          idx = indexof(lastchild,idx)+1
          skip_list.append(suite)
          print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)        
    else:
      idx+=1
# =============================================================================
# with session() as c:
#   c.post("http://10.58.199.163:8025/testlink-1.9.16/login.php",data=payload)
#   while idx<len(node_list):
#     if node_list[idx].tcase:
#       suite = nodes[node_list[idx].parent]
#       idx = buildTestSpec()
#     else:
#       idx+=1
# =============================================================================
  
  