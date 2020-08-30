# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 09:49:50 2019

@author: MLG1KOR
"""
from recurse_tl_v3 import gmDeepCopyTestlinkFolderStructure
from tl_req_export_multiprocessing import segregate
import json
from requests import session
import concurrent.futures as cf
from tl_class import testSuite,testcase
from bs4 import BeautifulSoup
import os

nodeid = '43878'
nodename = 'DEM'
testspec_folder = r'C:\Users\mlg1kor\testspec_317'
with open('database.json','r+') as fjson:
    data = json.load(fjson)
payload =  data['payload']

def simul_request(node_list):
  with session() as c:
    c.post("http://10.58.199.66:8050/testlink-1.9.16/login.php",data=payload)
    ret_data = []
    for tl_node in node_list:
      tc_url='http://10.58.199.66:8050/testlink-1.9.16/lib/testcases/archiveData.php?edit=testcase&id='+tl_node.node_id
      tc=c.get(tc_url)
      ret_data.append([tl_node,tc])
    return ret_data
  
nodes = gmDeepCopyTestlinkFolderStructure(nodeid,nodename,testspec_folder,payload)
leafs = []
specs = {}
for nid,node in nodes.items():
  if node.tcase:
    if node.parent.node_id not in specs:
      specs.update({node.parent.node_id:testSuite(node.parent.name,[])})
    leafs.append(node)
for i in range(3):
  skip_list = []
  if len(leafs)>0:
    print(f'{i+1} iteration')
    leaf_packets = segregate(leafs,8)
    with cf.ThreadPoolExecutor(max_workers=10) as executor:
      pool = [executor.submit(simul_request,packet) for packet in leaf_packets]
      for complete in cf.as_completed(pool):
        out = complete.result()
        for tc_node,tc_data in out:
          if tc_data.text!='':
            soup = BeautifulSoup(tc_data.content)
            try:
              testcase.fromHTML(specs[tc_node.parent.node_id],soup,tc_node.internal_id,tc_node.name)
            except:
              skip_list.append(tc_node)
          else:
            skip_list.append(tc_node)
    leafs = skip_list
  else:
    break
for nodeid,spec in specs.items():
  os.chdir(nodes[nodeid].path+'\\'+nodes[nodeid].name.replace('/',' '))
  spec.write()
  
            