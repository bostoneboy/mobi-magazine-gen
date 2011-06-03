#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import random
import urllib
import os.path
from xml.etree import ElementTree

def fetchHtml(url):
  action = urllib.urlopen(url)
  content = action.read()
  return content

# substitute the CR where in the title to blank.
def SubCR(content):
  keyword = re.compile(r"</?br/?>",re.IGNORECASE)
  return keyword.sub(" ",content)

# find_key must be a tuple, ordry by date,link and title.
def fetchList(content,findall_key,find_key):
  root = ElementTree.fromstring(content)
  node1 = root.findall(findall_key)
  list_today = []
  for i in node1:
    date  = i.find(find_key[0]).text
    link  = i.find(find_key[1]).text
    title = i.find(find_key[2]).text.encode("utf-8")
    # description = i.find(find_key[3]).text.encode("utf-8")
    title = SubCR(title)
    line = [date,link,title]
    list_today.append(line)
  list_today.sort()
  return list_today

def writeDatabase(database,llist):
  action = open(database,"w")
  page = "EOFhc2fheEOF\n".join(["|||".join(n) for n in llist])
  action.write(page)
  action.close()

# resolve the database file to list.
def resolvetoList(database):
  action = open(database,"r")
  content = action.read()
  action.close()
  list_yesterday = [m.split("|||") for m in content.split("EOFhc2fheEOF\n")]
  return list_yesterday

def compareListday(list1,list2):
  lllist = list1[:]
  b = [ a[1] for a in list1 ]
  for c in list2:
    if not (c[1] in b):
      lllist.append(c)
  lllist.sort()
  return lllist
 
def compareListweek(list_thisweek,list_lastweek):
  url_lastweek = [i[1] for i in list_lastweek]
  list_new = [m for m in list_thisweek if not (m[1] in url_lastweek)]
  return list_new
