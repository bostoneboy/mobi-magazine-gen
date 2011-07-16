#!/usr/bin/python

import re
import time
import random
import urllib
from xml.etree import ElementTree
from pymongo import Connection 

def fetchHtml(url):
  try:
    action = urllib.urlopen(url)
    content = action.read()
  except:
    print "can not open url:",url
    content = ""
  #content = action.read()
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
    title = SubCR(title)
    doc = {'date':date,'link':link,'title':title}
    list_today.append(doc)
  return list_today
  
def fetchListNFpeople(content):
  item_origin = re.findall(r'<h3><a\starget="_blank"\shref=[\s\S]+?</h3>',content)
  number = int(time.time())
  list_today = []
  link_prefix = "http://www.nfpeople.com"
  keyword = re.compile(r'<h3><a\starget="_blank"\shref="(\S+\d+\.html)?">(.*)</a></h3>',re.IGNORECASE)
  for i in item_origin:
    result = keyword.search(i)
    if result:
      link = link_prefix + result.group(1)
      title = keyword.search(i).group(2)
      number += 1
      date = str(number)
      insert_time = time.time()
      doc = {'date':date,'link':link,'title':title}
      list_today.append(doc)
  return list_today

def insertDB(collection,doc,errorno = 0):
  db = Connection().test
  post = db[collection]
  is_operate = 'no'
  insert_time = time.time()
  b = {'exception':errorno,'is_operate':is_operate,'insert_time':insert_time}
  doc.update(b)
  post.insert(doc)
 
def updateDB(collection,url):
  db = Connection().test
  post = db[collection]
  post.update({'link':url},{'$set':{'is_operate':'yes'}})

def queryDB(collection):
  db = Connection().test
  post = db[collection]
  return list(post.find({'is_operate':'no' , 'exception' : 0}).sort('date'))

def isqueryDB(collection,url):
  db = Connection().test
  post = db[collection]
  return post.find({'link' : url}).count()
