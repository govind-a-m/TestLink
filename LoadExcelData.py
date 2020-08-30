# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 09:25:48 2019

@author: MLG1KOR
"""
from tree_class import step

step.result_filename = r'D:\documents\testspecs\eScooter_bridgeDrv_Monitor_FS_7.xlsx'
step.attatchments_directory = r'D:\documents\current' 
step.ID_col = 1
step.notes_col = 10
step.status_col = 11
step.png_col = 12

step.CreateFromExcel()
