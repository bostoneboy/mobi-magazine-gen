#/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import time
import random
import urllib
import RSSparse

def randomString(count):
  basestring = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
  return "".join(random.sample(basestring,count))

def writeHtml(filename,page_content):
  action = open(filename,"w")
  action.write(page_content)
  action.close()

def pageFormat_nfzm(content,pageparse_keyword):
  keyword = re.compile(pageparse_keyword,re.IGNORECASE)
  result = keyword.search(content)
  page_head = result.group(1)
  page_body = result.group(2)
  page = page_head + page_body
  return page

def downloadIMG(content,title):
  img_uri_prefix = randomString(6)
  img_tab = re.findall(r'<img[\s\S]*?src="(\S+)?"',content)
  for list in img_tab:
    if re.search(r"nbweekly",title):
      base_url = "http://www.nbweekly.com"
      img_url = base_url + list
    else:
      img_url = list
    img_prefix = randomString(6)
    img_filename = img_prefix + re.search(r'(.[\w_-]+)$',img_url).group(1)
    try:
      urllib.urlretrieve(img_url,img_filename)
    except:
      print "cannot retrieve image on the server: %s" % img_url
      img_filename = ""
    content = re.sub(list,img_filename,content)
  return content

def htmlHeader():
  head = '''<html xmlns="http://www.w3.org/1999/xhtml"> 
            <head> 
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  
            </head> '''
  return head

def addBodytag(content):
  page = "<body>" + content + "</body>"
  return page