"""
Created on Mon Apr 29 17:25:12 2019

@author: mlg1kor
"""

from requests import session
import json
from contextlib import contextmanager
import os
import random

class node:
    def __init__(self,name,parent,node_id,nth_child,node_type,text):
      self.name = name
      self.parent = parent
      self.node_id = node_id
      self.nth_child  = nth_child
      self.children= []
      if(node_type=='testcase'):
          self.tcase = True
          self.internal_id = text[:text.find(':')]
      else :
          self.tcase = False
          self.internal_id = None
            
    def set_children(self,data):
        self.children = list(item['id'] for item in data)
        self.nof_children = len(self.children)
    
    def __repr__(self):
      if isinstance(self.parent,node):
        return f'name:{self.name}\nparent:{self.parent.node_id}\nid:{self.node_id}internal_id:{self.internal_id}'
      else:
        return '\n'.join(f'{k} : {v}' for k,v in self.__dict__.items())
      

        
def gm_get_nodes(username,password,nodeid,nodename):
    global url,nodes,payload,c     
    payload = {"tl_login":username,
               "tl_password":password,
               "CSRFName":"CSRFGuard_2113925045",
               "CSRFToken":"d661b4dfa16c21a9b594d95cce0d4e6d52ab254ec490afd357332093b6858d7c38f405c8803e263a23033fc2fa8519dbeb7b5838bfd9e05dffb5ab2c3dd1bacb",
               "action":"login.php?viewer=" }
    url = "http://10.58.199.66:8050/testlink-1.9.16/login.php"
    nodes = {}
    nodes.update(dict([(nodeid,node(nodename,None,nodeid,None,'testsuite',''))]))
    with session() as c:
        c.post("http://10.58.199.66:8050/testlink-1.9.16/login.php",data=payload)
        gm_recurse_node(nodeid)
    return nodes

def gm_recurse_node(nid):
    global parent, nth_child, rsp, nid_url
    nid_url='http://10.58.199.66:8050/testlink-1.9.16/lib/ajax/gettprojectnodes.php?root_node=1&tcprefix=TS-&node='+nid
    rsp=c.get(nid_url)
    print(nid_url)
    tsp_data=rsp.json()
    try:
      for index,item in enumerate(tsp_data):
          nodes.update(dict([(item['id'],node(item['testlink_node_name'],nid,item['id'],index,item['testlink_node_type'],item['text']))]))
      nodes[nid].set_children(tsp_data)
      parent=nodes[nid]
      nth_child=0
    except:
      nth_child = nodes[nid].nth_child+1
      parent = nodes[nodes[nid].parent]
      while (parent.nof_children == nth_child) :
        try:
          nth_child = parent.nth_child+1
          parent = nodes[parent.parent]
        except:
            return
    while (nodes[parent.children[nth_child]].tcase):
        nth_child+=1
        while (parent.nof_children == nth_child) :
            try:
                nth_child = nodes[parent.parent].children.index(parent.node_id)+1
                nth_child = parent.nth_child+1
                parent = nodes[parent.parent]
            except:
                    return
    print(parent.name)
    gm_recurse_node(parent.children[nth_child])

@contextmanager
def walk_into(destination):
  try:
    cwd = os.getcwd()
    files = os.listdir()
    for file in files:
      if file.upper()==destination.upper():
        if file==destination:
          child_path = cwd+'//'+destination 
          os.chdir(child_path)
          break          
        else:
          destination = destination+'_'+str(random.randrange(1,10000,1)) 
          os.mkdir(destination)
          child_path = cwd+'//'+destination
          os.chdir(child_path)
          break
    else:
      os.mkdir(destination)
      child_path = cwd+'//'+destination 
      os.chdir(child_path)
    yield child_path
  finally:
    os.chdir(cwd)
    
def DeepCopy(parent):
  with walk_into(parent.name.replace('/',' ')) as child_path:
    for child in parent.children:
      setattr(child,'path',child_path)
      if child.tcase==False:
        DeepCopy(child)

def restructure_nodes(nodes):
  for nid,node in nodes.items():
    if node.parent:
      node.parent = nodes[node.parent]
    for i,child in enumerate(node.children):
      node.children[i] = nodes[child]
  
def gmDeepCopyTestlinkFolderStructure(nodeid,nodename,root_folder,payload):
  nodes = gm_get_nodes(payload['tl_login'],payload['tl_password'],nodeid,nodename)
  restructure_nodes(nodes)
  setattr(nodes[nodeid],'path',root_folder)
  wd = os.getcwd()
  os.chdir(root_folder)
  DeepCopy(nodes[nodeid])
  os.chdir(wd)
  return nodes
  
if __name__ == '__main__' :
    with open('tl_login_info.json','r+') as fjson:
        lg_info = json.load(fjson)
    testlink_nodes = gm_get_nodes(lg_info['username'],lg_info['password'],'19272','HW-SW')
    testcase = list(filter(lambda x: x.tcase,testlink_nodes))
    print(len(testcase))