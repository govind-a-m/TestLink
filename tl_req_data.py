# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:40:42 2019

@author: MLG1KOR
"""

import sqlite3

conn = sqlite3.connect('tc_req.db')
c = conn.cursor()

create_module_table = """ CREATE TABLE IF NOT EXISTS module (
                                    nodeid integer PRIMARY KEY,
                                    testcaseID integer NOT NULL,
                                    name text NOT NULL,
                                    rid text,
                                    tcls text,
                                    asil text,
                                    
                                ); """

create_interface_table = """ CREATE TABLE IF NOT EXISTS interface (
                                    nodeid integer PRIMARY KEY,
                                    testcaseID integer NOT NULL,
                                    name text NOT NULL,
                                    rid text,
                                    tcls text,
                                    asil text,
                                    
                                ); """

