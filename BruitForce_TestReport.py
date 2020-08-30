# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 09:34:43 2019

@author: MLG1KOR
"""

from tree_class import gm_cut_the_tree,testsuite
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import time
import os
import pyautogui
import pdfkit


def login(lg_info):
  browser.get("http://10.58.199.163:8025/testlink-1.9.16/login.php")
  username = browser.find_element_by_id("tl_login")
  pwd = browser.find_element_by_id("tl_password")
  username.send_keys(lg_info['username'])
  pwd.send_keys(lg_info['password'])
  s = browser.find_element_by_xpath("/html/body/div/div[2]/form/div[3]/input")
  s.click()

def process_innerHTML(script):
  script = script.get_attribute('innerHTML')
  script = script[script.find('treeCfg.children=')+len('treeCfg.children='): ]
  script = script.split('\n')
  data = script[0][:-1]
  build = script[1]
  build = build[len("treeCfg.cookiePrefix='test_exec_build_id_'")-1:-len("_';")]
  with open('text.txt','w') as f:
    f.write(data)
  return (json.loads(data),build)

def set_report_id(testcase):
  global build
  browser.get(f'http://10.58.199.163:8025/testlink-1.9.16/lib/execute/execSetResults.php?version_id={testcase.tcversion_id}&level=testcase&id={testcase.node_id}&setting_build={build}')
  wait.until(EC.visibility_of_element_located((By.XPATH,'/html/body/div/form/div[9]/table/tbody/tr[2]/td[4]')))
  report_id = browser.find_element_by_xpath('/html/body/div/form/div[9]/table/tbody/tr[2]/td[4]').get_attribute('title')
  testcase.report_id = report_id[4:-1]
  print(testcase.report_id)

def downloadReport(link,name):
  if name in os.listdir():
    os.remove(name)
  browser.get(link)
  time.sleep(1)
  pyautogui.hotkey('ctrl', 's')
  time.sleep(1)
  pyautogui.typewrite(name)
  pyautogui.hotkey('enter')
  time.sleep(1)

def getScript(browser,testplan):
  browser.get('http://10.58.199.163:8025/testlink-1.9.16/lib/general/frmWorkArea.php?feature=executeTest')
  browser.switch_to.frame(browser.find_element_by_name('treeframe'))
  browser.find_element_by_xpath('/html/body/form/div[1]/div[2]/div/table/tbody/tr[1]/td[2]/div').click()
  inp = browser.find_element_by_xpath('/html/body/form/div[1]/div[2]/div/table/tbody/tr[1]/td[2]/div/div/div/input')
  inp.send_keys(testplan)
  inp.send_keys(Keys.ENTER)
  time.sleep(10)
  script = browser.find_element_by_xpath('/html/head/script[26]')
  return script

if __name__=="__main__":
  testplan = 'eScooter4KW_AR4.2_FunctionalSafety_Step2_Testing_Cycle7'
  testsuite_list = ['18976']
  with open('tl_login_info.json','r+') as fjson:
    lg_info = json.load(fjson)
  browser = webdriver.Firefox()
  wait = WebDriverWait(browser, 50)
  login(lg_info)
  script = getScript(browser,testplan)
  tree,build = process_innerHTML(script)
  gm_cut_the_tree(tree,'root','None')
  for i in range(len(testsuite_list)):
    if testsuite_list[i] in testsuite.db:
      testsuite_list[i] = testsuite.db[testsuite_list[i]]
      for testcase in testsuite_list[i].TestCases:
        set_report_id(testcase)
  config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
  os.chdir(r'C:\Users\mlg1kor\Downloads')
  for suite in testsuite_list:
    for testcase in suite.TestCases:
      url = f'http://10.58.199.163:8025/testlink-1.9.16/lib/execute/execPrint.php?id={testcase.report_id}'
      downloadReport(url,str(testcase.report_id)+'.html')
    pdfkit.from_file(suite.getFilenames('html'),suite.getSuiteFileName(),configuration=config)
     