# -*- coding: utf-8 -*-
"""
Created on Tue May 21 14:03:13 2019

@author: mlg1kor
"""

from   selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from recurse_tl_v3 import node,gm_get_nodes,gm_recurse_node
import json
import xlrd
#%%
node_id = '19272'
with open('tl_login_info.json','r+') as fjson:
    lg_info = json.load(fjson)
book = xlrd.open_workbook(r'map_signalname.xlsx')
sheet= book.sheet_by_index(0)
#%%
def get_tcvid(nid):
    browser.get("http://10.58.199.163:8025/testlink-1.9.16/lib/testcases/archiveData.php?edit=testcase&id={}".format(nid))
    return browser.find_element_by_xpath('/html/body/div/div[2]/form[1]/input[4]').get_attribute('value')

def login():
    browser.get("http://10.58.199.163:8025/testlink-1.9.16/login.php")
    username = browser.find_element_by_id("tl_login")
    pwd = browser.find_element_by_id("tl_password")
    username.send_keys(lg_info['username'])
    pwd.send_keys(lg_info['password'])
    s = browser.find_element_by_xpath("/html/body/div/div[2]/form/div[3]/input")
    s.click()

def create_new_version(tcid,tcvid):
    browser.get('http://10.58.199.163:8025/testlink-1.9.16/lib/testcases/tcEdit.php?testcase_id={}&tcversion_id={}&has_been_executed=0&doAction=&show_mode=&do_create_new_version=New+version'.format(tcid,tcvid))

def edit_cfield(nid,tcvid,pid,new_req,asil):
    browser.get('http://10.58.199.163:8025/testlink-1.9.16/lib/testcases/tcEdit.php?testcase_id={}&tcversion_id={}&has_been_executed=0&doAction=edit&show_mode=&edit_tc=Edit&containerID={}'.format(nid,tcvid,pid))
    req = browser.find_element_by_id("custom_field_0_2")
    if(req.get_attribute('value').find(new_req)==-1):
        req.send_keys(','+new_req)
    alevel =  browser.find_element_by_id("custom_field_0_3")
    if (alevel.get_attribute('value') =="") :
        alevel.send_keys(asil)
    browser.find_element_by_xpath('//*[@id="do_update_bottom"]').click()
    wait.until_not(EC.visibility_of_element_located((By.ID, "do_update_bottom")))

#%%
tl_nodes = gm_get_nodes(lg_info['username'],lg_info['password'],node_id,'HW-SW')
node_list = list(filter(lambda x: x.tcase,tl_nodes))
#%%
browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)
login()
for index,tc in enumerate(node_list):
    if(sheet.cell(index,1).value!=""):
        tc_vid = get_tcvid(tc.node_id)
        create_new_version(tc.node_id,tc_vid)
        tc_vid = get_tcvid(tc.node_id)
        edit_cfield(tc.node_id,tc_vid,tc.parent,sheet.cell(index,1).value,'B(B)')
        
#%%
#browser = webdriver.Firefox()
#wait = WebDriverWait(browser, 10)
#login()
#parent = node_id
#for row in range(sheet.nrows):
#    if(sheet.cell(row,1).value!=""):
#        tid = str(int(sheet.cell(row,2).value))
#        tc_vid = get_tcvid(tid)
#        create_new_version(tid,tc_vid)
#        tc_vid = get_tcvid(tid)
#        edit_cfield(tid,tc_vid,parent,sheet.cell(row,1).value,'B(B)')
   
        
        

