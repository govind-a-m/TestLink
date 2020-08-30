# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 12:19:07 2019

@author: mlg1kor
"""

import xlrd
import json
book = xlrd.open_workbook(r"C:\Users\mlg1kor\Desktop\portvalues.xlsx")
sheet= book.sheet_by_index(0)
data={'PM':'0x4051','P':'0x00A0','PMC':'0x06F4','PFCE':'0x04C0','PFC':'0x0400','PMM':'0x4051','PIPC':'0x0000','PBDC':'0x0000','PIS':'0x0000','PD':'0x0000','PU':'0x0400'}
for p in range(10):
    js_file='port'+str(p)+'.json'
    data['PM']=sheet.cell((p*21)+2,1).value
    data['P']=sheet.cell((p*21)+9,1).value
    data['PMC']=sheet.cell((p*21)+0,1).value
    data['PFCE']=sheet.cell((p*21)+5,1).value
    data['PFC']=sheet.cell((p*21)+4,1).value
    data['PMM']=sheet.cell((p*21)+2,1).value
    data['PIPC']=sheet.cell((p*21)+8,1).value
    data['PBDC']=sheet.cell((p*21)+12,1).value
    data['PIS']=sheet.cell((p*21)+20,1).value
    data['PD']=sheet.cell((p*21)+14,1).value
    data['PU']=sheet.cell((p*21)+13,1).value    
    with open(js_file,'w') as fjson:
        json.dump(data,fjson)