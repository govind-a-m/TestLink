# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 11:03:11 2019

@author: MLG1KOR
"""

from recurse_tl_v3 import gm_get_nodes
import concurrent.futures as cf
from asil_test_class import ThreadUploader
import json
import xlrd
from tl_req_export_multiprocessing import segregate


node_id = '16521'
node_name = 'DEP_escooter'
with open('tl_login_info.json','r+') as fjson:
    lg_info = json.load(fjson)
book = xlrd.open_workbook(r'C:\Users\mlg1kor\Documents\tcls.xlsx')
sheet= book.sheet_by_index(0)
if __name__=='__main__':
  __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
  nodes = gm_get_nodes(lg_info['username'],lg_info['password'],node_id,node_name)
  node_list = [value for key,value in nodes.items() if value.tcase]
  data = []
  packet = []
  for i in range(0,sheet.nrows):
    internal_id = sheet.cell(i,0).value.strip()
    asil = sheet.cell(i,2).value.upper()
    tcls = sheet.cell(i,1).value.lower()
    data.append([internal_id,tcls,asil])
  data = segregate(data,10)
  print(data)
  progress = 0
  with cf.ProcessPoolExecutor(max_workers=10) as executor:
    pool = [executor.submit(ThreadUploader,packet,node_list,lg_info) for packet in data]
    for complete in cf.as_completed(pool):
      result = complete.result()
      print(*result,sep='\n')
      progress = progress+8
      print(f'{progress}/{len(node_list)}')
