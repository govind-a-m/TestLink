# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 11:49:50 2019

@author: MLG1KOR
"""
from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from recurse_tl_v3 import gm_get_nodes
import json
import xlrd
from selenium.webdriver.support.ui import Select


browser = None
wait = None
def login(lg_info):
    browser.get("http://10.58.199.66:8050/testlink-1.9.16/login.php")
    username = browser.find_element_by_id("tl_login")
    pwd = browser.find_element_by_id("tl_password")
    username.send_keys(lg_info['username'])
    pwd.send_keys(lg_info['password'])
    s = browser.find_element_by_xpath("/html/body/div/div[2]/form/div[3]/input")
    s.click()

def save_data():
  browser.find_element_by_xpath('//*[@id="do_update_bottom"]').click()
  wait.until_not(EC.visibility_of_element_located((By.ID, "do_update_bottom")))
  
def srch_node(internal_id,node_list):
  for j in range(len(node_list)):
    if node_list[j].internal_id==internal_id:
      return node_list[j]
  return None
    
class testcase:
  def __init__(self,tc,tcls,asil,stat):
    self.nid = tc.node_id
    self.parent = tc.parent
    self.stat = stat
    self.tcls = tcls
    self.asil = asil
    
  
  def set_status(self):
    sel_stat = Select(browser.find_element_by_xpath('//*[@id="tc_status"]'))
    sel_stat.select_by_index(self.stat)
  
  def set_asil(self):
    sel_asil = Select(browser.find_element_by_xpath('//*[@id="custom_field_7_6"]'))
    sel_asil.deselect_all()
    if self.asil=='QM':
      sel_asil.select_by_index(0)
    else:
      sel_asil.select_by_index(1)
  
  def set_tcls(self):
    sel_tcls = Select(browser.find_element_by_xpath('//*[@id="custom_field_7_4"]'))
    sel_tcls.deselect_all()
    sel_tcls.select_by_index(self.tcls)
  
  def set_tcvid(self):
    for i in range(3):
      browser.get("http://10.58.199.66:8050/testlink-1.9.16/lib/testcases/archiveData.php?edit=testcase&id={}".format(self.nid))
      try:
        self.tcvid = browser.find_element_by_xpath('/html/body/div/div[2]/form[1]/input[4]').get_attribute('value')
      except:
        print(f'tryig {i+1} tiime')
        continue
      break
  def create_new_version(self):
    browser.get(f'http://10.58.199.66:8050/testlink-1.9.16/lib/testcases/tcEdit.php?testcase_id={self.nid}&tcversion_id={self.tcvid}&has_been_executed=0&doAction=&show_mode=&do_create_new_version=New+version')
    self.set_tcvid()
  
  def edit(self):
    browser.get(f'http://10.58.199.66:8050/testlink-1.9.16/lib/testcases/tcEdit.php?testcase_id={self.nid}&tcversion_id={self.tcvid}&has_been_executed=0&doAction=edit&show_mode=&edit_tc=Edit&containerID={self.parent}')
  
  def add_new_req(self,new_req):
    req = browser.find_element_by_id("custom_field_0_2")
    req.send_keys(','+new_req)

def ThreadUploader(data,node_list,lg_info):
  global browser,wait
  result = []
  opt = {"qm":0,
            "re":1,
            "fa":2,
            "in":3,
            "st":5,
            "fu":6,
            "el":7,
            "en":8,
            "eq":9,
            "bo":10,
            "an":11}
  browser = webdriver.Firefox()
  wait = WebDriverWait(browser, 15)
  login(lg_info)
  for tcdata in data:
    internal_id = tcdata[0]
    pb_node = srch_node(internal_id,node_list)
    asil = tcdata[2].upper()
    tcls = tcdata[1][:2].lower()
    if tcls in opt.keys():
      tcls = opt[tcls]   
      if pb_node is not None:
        cur_tc = testcase(pb_node,tcls,asil,6)
        cur_tc.set_tcvid()
        cur_tc.create_new_version()
        cur_tc.edit()
        cur_tc.set_status()
        cur_tc.set_asil()
        cur_tc.set_tcls()
        save_data()
        result.appennd(f'{internal_id}:{tcls},{asil}')
      else:
        result.append(f'wrong testcase {internal_id}')
    else:
      result.append(f'{internal_id} has wrong tcls {tcls}')
  return result
      
if __name__=='__main__':
  node_id = '20812'
  node_name = 'adc'
  with open('tl_login_info.json','r+') as fjson:
      lg_info = json.load(fjson)
  book = xlrd.open_workbook(r'D:\documents\Book1.xlsx')
  sheet= book.sheet_by_index(0)
  opt = {"qm":0,
            "re":1,
            "fa":2,
            "in":3,
            "st":5,
            "fu":6,
            "el":7,
            "en":8,
            "eq":9,
            "bo":10,
            "an":11}
  
  
  browser = webdriver.Firefox()
  wait = WebDriverWait(browser, 15)
  login(lg_info)
  nodes = gm_get_nodes(lg_info['username'],lg_info['password'],node_id,node_name)
  node_list = [value for key,value in nodes.items() if value.tcase]
  for nd in node_list:
    cur_tc = testcase(nd,3,'QM',6)
    cur_tc.set_tcvid()
    cur_tc.create_new_version()
    cur_tc.edit()
    cur_tc.set_status()
    cur_tc.set_asil()
    cur_tc.set_tcls()
    save_data()

#  for i in range(1,sheet.nrows):
#    nodes = gm_get_nodes(lg_info['username'],lg_info['password'],str(sheet.cell(i,0).value),node_name)
#    node_list = [value for key,value in nodes.items() if value.tcase]
#    for nd in node_list[1:]:
#      cur_tc = testcase(nd,opt[sheet.cell(i,1).value.lower()[:2]],sheet.cell(i,2).value.upper(),6)
#      cur_tc.set_tcvid()
#      cur_tc.create_new_version()
#      cur_tc.edit()
#      cur_tc.set_status()
#      cur_tc.set_asil()
#      cur_tc.set_tcls()
#      save_data()
#  nodes = gm_get_nodes(lg_info['username'],lg_info['password'],node_id,node_name)
#  node_list = [value for key,value in nodes.items() if value.tcase]
#  for i in range(1,sheet.nrows):
#    if isinstance(sheet.cell(i,0).value,float):
#      internal_id = 'TS-'+str(int(sheet.cell(i,0).value))
#    else:
#      internal_id = sheet.cell(i,0).value.strip()
#    pb_node = srch_node(internal_id,node_list)
#    asil = sheet.cell(i,2).value.upper()
#    tcls = sheet.cell(i,1).value.lower()[:2]
#    if tcls in opt.keys():
#      tcls = opt[tcls]   
#      if pb_node is not None:
#        print(f'{i}/{sheet.nrows-2}  {internal_id}:{tcls},{asil}')
#        cur_tc = testcase(pb_node,tcls,asil,6)
#        cur_tc.set_tcvid()
#        cur_tc.create_new_version()
#        cur_tc.edit()
#        cur_tc.set_status()
#        cur_tc.set_asil()
#        cur_tc.set_tcls()
#        save_data()
#      else:
#        print(f'wrong testcase {internal_id}')
#    else:
#      print(f'{internal_id} has wrong tcls {tcls}')