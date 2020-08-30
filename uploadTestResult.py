# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:34:15 2019

@author: MLG1KOR
"""
from tree_class import *
from BruiteForce_TestReport import login,getScript,process_innerHTML
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import json
import os

suite_ID = '18976'
testplan = 'eScooter4KW_AR4.2_FuSi_Step3_Baseline2_RegressionCycle_Interface_2'
step.result_filename =r'C:\Users\mlg1kor\Documents\Copy of HW-SW (Port)_81.xlsx'
step.attatchments_directory = r'U:\clma_2' 
step.ID_col = 11
step.notes_col = 12
step.status_col = 13
step.png_col = 14
step.CreateFromExcel()
#%%
os.chdir(r'C:\Users\mlg1kor')
with open('tl_login_info.json','r+') as fjson:
  lg_info = json.load(fjson)
browser = webdriver.Firefox()
wait = WebDriverWait(browser, 50)
testcase.browser = browser
testcase.wait = wait
login(lg_info,browser)
script = getScript(browser,testplan)
tree,build = process_innerHTML(script)
gm_cut_the_tree(tree,'root','None')
suite = testsuite.db[suite_ID]
suite.CollectSteps(step.db)
for tc in suite.TestCases:
  if len(tc.steps)>0:
    tc.VisitTestCase(build)
    step_row = browser.find_elements_by_class_name('step_note_textarea')
    step_status = browser.find_elements_by_class_name('step_status')
    for index,row,status in zip(range(len(step_row)),step_row,step_status):
      if index<len(tc.steps):
        cur_step = tc.steps[index]
        row.send_keys(cur_step.notes)
        Select(status).select_by_index(cur_step.stat)
        cur_step.stepID = row.get_attribute('id').split('_')[2]
        cur_step.sendFileKey()
        tc.status = False if cur_step.stat==2 else tc.status
    tc.savedata()
