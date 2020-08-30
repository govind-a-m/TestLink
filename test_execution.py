# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 10:26:01 2019

@author: MLG1KOR
"""
import xlrd
import json
from recurse_tl_v3 import gm_get_nodes
from requests import session
from bs4 import BeautifulSoup
import xlsxwriter

result_file_path = r'C:\Users\mlg1kor\Downloads\resultsTCFlat_DEP-IN_eScooter4KW_AR4.2_FunctionalSafety_Step2_Testing_Cycle7(5).xls'
testing_cycle_name = 'eScooter4KW_AR4.2_FunctionalSafety_Step2_Testing_Cycle7'
output_file = 'req_Remarks_testStatus.xlsx'

book = xlrd.open_workbook(result_file_path)
sheet = book.sheet_by_index(0)
with open('tl_login_info.json','r+') as fjson:
    lg_info = json.load(fjson)
nodeid = '19272'
nodename = 'hw_sw_adc'
payload={"tl_login":lg_info['username'],
         "tl_password":lg_info['password'],
         "CSRFName":"CSRFGuard_2113925045",
         "CSRFToken":"d661b4dfa16c21a9b594d95cce0d4e6d52ab254ec490afd357332093b6858d7c38f405c8803e263a23033fc2fa8519dbeb7b5838bfd9e05dffb5ab2c3dd1bacb",
         "action":"login.php?viewer=" }

class testcase():
  db = []
  skip_db = []
  def __init__(self,tc,result):
    self.name = tc.name
    self.node_id = tc.node_id
    self.result = result
    self.internal_id = tc.internal_id
    self.link = 'http://10.58.199.163:8025/testlink-1.9.16/lib/testcases/archiveData.php?edit=testcase&id='+self.node_id
    self.set_custom_fields()
  
  def set_custom_fields(self):
    try:
      tc = c.get(self.link)
      soup = BeautifulSoup(tc.content)
      cfields = soup.select('#cfields_design_time')
      c_rows = cfields[0].table.find_all('tr')
      self.external_id = c_rows[0].find_all('td')[1].text
      rid = str(c_rows[1].find_all('td')[1].text)
      self.rid = []
      if ',' in rid:
        rid = rid.split(',')
        for raw_id in rid:
          raw_id = raw_id.strip()
          if raw_id!='':
            self.rid.append(raw_id)
      elif '\n' in rid:
        rid = rid.split('\n')
        for raw_id in rid:
          raw_id = raw_id.strip()
          if raw_id!='':
            self.rid.append(raw_id)
      else:
        self.rid = [rid]
      testcase.db.append(self)
      print(self)
    except:
      testcase.skip_db.append(self)
      print(f'skipped {self.node_id}')
  
  def __repr__(self):
    return f'id:{self.internal_id},req:{self.rid},stat:{self.result}'
      
class req():
  db = {}
  def __init__(self,tc,rid):
    if rid not in req.db:
      self.id = rid
      if tc.result=='Failed':
        self.stat = False
        self.remarks = testing_cycle_name+'\n'+tc.link
      else:
        self.stat = True
        self.remarks = testing_cycle_name
      req.db.update({self.id:self})
    else:
      if tc.result=='Failed':
        req.db[rid].stat = not req.db[rid].stat
        req.db[rid].remarks = req.db[rid].remarks+'\n'+tc.link
  
  @classmethod
  def dxl_prepare(cls):
    with open('U:\\req.txt','w') as freq:
      with open('U:\\result.txt','w') as fres:
        with open('U:\\remarks.txt','w') as frem:
          for item in cls.db.values():
            freq.write(item.id+'\n')
            result = 'Passed' if item.stat else 'Failed'
            fres.write(result+'\n')
            frem.write(item.remarks+'\n')
            frem.write('-----')
  
  @classmethod
  def write_results_to_excel(cls):
    global output_file
    book = xlsxwriter.Workbook(output_file)
    sheet=book.add_worksheet()
    sheet.write(0,0,'requirementID')
    sheet.write(0,1,'Remarks')
    sheet.write(0,2,'Test Status')
    for rno,item in enumerate(cls.db.values(),start=1):
      sheet.write(rno,0,item.id)
      sheet.write(rno,1,item.remarks)
      result = 'Passed' if item.stat else 'Failed'
      sheet.write(rno,2,result)
    
  def __repr__(self):
    return f'id:{self.id},stat={self.stat}\n remarks:\n{self.remarks}'

if 'node_list' not in globals():
  nodes = gm_get_nodes(lg_info['username'],lg_info['password'],nodeid,nodename)
  node_list = [value for key,value in nodes.items()]
with session() as c:
  c.post("http://10.58.199.163:8025/testlink-1.9.16/login.php",data=payload)
  len_skip_db = len(testcase.db)
  if len_skip_db==0:
    for i in range(5,sheet.nrows):
      internal_id = sheet.cell(i,1).value
      internal_id = internal_id[:internal_id.find(':')]
      stat = sheet.cell(i,6).value
      for index,item in enumerate(node_list):
        if item.internal_id==internal_id:
          testcase(node_list.pop(index),stat)
          break
  else:
    skip_list = testcase.skip_db
    testcase.skip_db = []
    while len(skip_list)>0:
      testcase(skip_list[0],skip_list[0].result)
      del skip_list[0]
  if len(testcase.skip_db)==0:
    for tcase in testcase.db:
      for rq in tcase.rid:
        req(tcase,rq)
    req.write_results_to_excel()
    req.dxl_prepare()
  else:
    print('some testcases are skipped run again?')