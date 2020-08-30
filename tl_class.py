# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 09:34:48 2019

@author: MLG1KOR
"""

import xlsxwriter

class testSuite():
  def __init__(self,name,tcs):
    self.name = name
    self.testcases = tcs
    print(f'testsuite {self.name} is created')
    
  @classmethod
  def fromXML(cls,root):
    name = root.attrib['name']
    testsuite = cls(name,[])
    testcases = root.findall('testcase')
    for i in range(len(testcases)):
      testcases[i] = testcase.fromXML(testcases[i])
    testsuite.testcases = testcases
    return testsuite

  def write(self):
    book=xlsxwriter.Workbook(self.name.replace('/',' ')+'.xlsx')
    sheet=book.add_worksheet()
    wrap=book.add_format({'text_wrap':True})
    rno = 0
    sheet.write(rno,0,'Name')
    sheet.write(rno,1,'Summary')
    sheet.write(rno,2,'Precondition')
    sheet.write(rno,3,'Actions')
    sheet.write(rno,4,'Expected Results')
    sheet.write(rno,5,'TestCase ID')
    sheet.write(rno,6,'Requirements')
    sheet.write(rno,7,'Test Classification')
    sheet.write(rno,8,'ASIL')
    sheet.write(rno,9,'TS-ExternalID')
    for tc in self.testcases:
      rno+=1
      sheet.write(rno,0,tc.name)
      sheet.write(rno,1,tc.summary.text,wrap)
      sheet.write(rno,2,tc.precondition.text,wrap)
      try:
        sheet.write(rno,3,tc.action_ptr[0][0].text,wrap)
      except:
        pass
      try:
        sheet.write(rno,4,tc.action_ptr[0][1].text,wrap)
      except:
        pass
      sheet.write(rno,5,tc.cfield_data['TestCaseID'])
      sheet.write(rno,6,tc.cfield_data['Requirement_ID'])
      sheet.write(rno,7,tc.cfield_data['Test Classification'])
      sheet.write(rno,8,tc.cfield_data['ASIL Level'])
      sheet.write(rno,9,tc.externalID.replace('TS-',''))
      if len(tc.action_ptr)>1:
        for i in range(1,len(tc.action_ptr)):
          rno+=1
          sheet.write(rno,3,tc.action_ptr[i][0].text,wrap)
          sheet.write(rno,4,tc.action_ptr[i][1].text,wrap)
    book.close()
  
class testcase():
  def __init__(self,externalID,name,summary,precondition,ptr,cdata):
    self.externalID = externalID
    self.name = name
    self.summary = summary
    self.precondition = precondition
    self.action_ptr = ptr
    self.cfield_data = cdata
    print(f'       testCase {self.name} is created',end = ' ')
    
  @classmethod
  def fromXML(cls,tc):
    externalID = 'TS-'+tc.find('externalid').text
    name = tc.attrib['name']
    summary = tc.find('summary')
    precondition = tc.find('preconditions')
    cdata = {}
    for cfield in tc.find('custom_fields').getchildren():
      key,value = cfield.getchildren()
      cdata.update({key.text:value.text})
    ptr = []
    try:
      for step in tc.find('steps').getchildren():
        _,action,expected,_ = step.getchildren()
        ptr.append([action,expected])
    except:
      pass
    return cls(externalID,name,summary,precondition,ptr,cdata)
  
  @classmethod
  def fromHTML(cls,spec,src,externalid,name):
    noftc = 1
    ptr = []
    while True:
      step_row = src.select('#step_row_'+str(noftc))
      if len(step_row)>0:
        _,action,expected,*_ = step_row[0].find_all('td')
        ptr.append([action,expected])
        noftc+=1
      else:
        break
    anc = src.find('table').find_all('td')
    summary,precondition = anc[5],anc[6]
    cfields=src.select('#cfields_design_time')
    c_rows=cfields[0].table.find_all('tr')
    tid=c_rows[0].find_all('td')[1].text
    rid=c_rows[1].find_all('td')[1].text
    tcls  = c_rows[2].find_all('td')[1].text
    asil = c_rows[3].find_all('td')[1].text
    cdata = {'TestCaseID':tid,'Requirement_ID':rid,'Test Classification':tcls,'ASIL Level':asil}
    return_tc = cls(externalid,name,summary,precondition,ptr,cdata)
    print(f'under {spec.name}')
    spec.testcases.append(return_tc)
    return return_tc