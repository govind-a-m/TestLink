# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 08:49:29 2019

@author: mlg1kor
"""

import json
from requests import *
from bs4 import BeautifulSoup
payload={"tl_login":"Govind","tl_password":"depin","CSRFName":"CSRFGuard_2113925045","CSRFToken":"d661b4dfa16c21a9b594d95cce0d4e6d52ab254ec490afd357332093b6858d7c38f405c8803e263a23033fc2fa8519dbeb7b5838bfd9e05dffb5ab2c3dd1bacb","action":"login.php?viewer=" }
url="http://10.58.199.163:8025/testlink-1.9.16/login.php"
nodeid = '16522'
node_dict={nodeid:'eScooter_SystemTesting'}
pc_dict={}
cp_dict={}
tc_node_list=[]

def gm_recurse_node(nid):
    global parent, nth_child, rsp, nid_url
    nid_url='http://10.58.199.163:8025/testlink-1.9.16/lib/ajax/gettprojectnodes.php?root_node=1&tcprefix=TS-&node='+nid
    rsp=c.get(nid_url)
    print(nid_url)
    with open(nid+'.json','w') as f:
        f.write(rsp.text)
    with open(nid+'.json','r+') as fjson:
        tsp_data = json.load(fjson)
    for node in tsp_data:
        node_dict.update(dict([(node['id'],node['text'])]))
        cp_dict.update(dict([(node['id'],nid)]))
    pc_dict.update(dict([(nid,list(tsp['id'] for tsp in tsp_data))]))
    parent=nid
    nth_child=0
    while(node_dict[pc_dict[parent][nth_child]].find('TS-')!=-1):
        tc_node_list.append(pc_dict[parent][nth_child])
        nth_child=nth_child+1
        while(len(pc_dict[parent])==nth_child):
            old_parent=parent
            try:
                parent=cp_dict[parent]
            except:
                return
            nth_child=pc_dict[parent].index(old_parent)+1
    gm_recurse_node(pc_dict[parent][nth_child])
            
with session() as c:
    c.post("http://10.58.199.163:8025/testlink-1.9.16/login.php",data=payload)
    gm_recurse_node(nodeid)


