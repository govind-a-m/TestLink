# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 12:17:14 2019

@author: MLG1KOR
"""

import openpyxl
import json
from recurse_tl_v3 import gm_get_nodes
import test_execution 

result_file_path = r'C:\Users\mlg1kor\Downloads\resultsTCFlat_DEP-IN_eScooter4KW_AR4.2_FunctionalSafety_Step2_Testing_Cycle7(2).xls'
output_file = 'req_Remarks_testStatus.xlsx'

wb=openpyxl.load_workbook(''