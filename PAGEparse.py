#/usr/bin/python

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
  
def pagechapterBlank():
  return "<p>&nbsp;</p>"

def pageFormat(content,pageparse_keyword):
  keyword = re.compile(pageparse_keyword,re.IGNORECASE)
  try:
    result = keyword.search(content)
    page_head = result.group(1)
    page_body = result.group(2)
    page = page_head + pagechapterBlank() + page_body
  except:
    print "can not parse key content." 
    page = ""
  return page
  
def pageFormatNFpeople(content):
  keyword1 = re.compile(r'<span[\s\S]*?>',re.IGNORECASE)         # delete the begin span mark
  keyword2 = re.compile(r'</span>',re.IGNORECASE)                # delete the end span mark
  keyword3 = re.compile(r'<p\sstyle=[\s\S]*?>',re.IGNORECASE)    # sub to <p>
  keyword4 = re.compile(r'<p>(&nbsp;){2,}',re.IGNORECASE)        # delete the &nbsp; marks followed <p>
  keyword5 = re.compile(r'(<p>&nbsp;</p>\s*)+',re.IGNORECASE)
  keyword6 = re.compile(r'(<p><p>&nbsp;</p>)+',re.IGNORECASE)
  try:
    content = keyword1.sub('',content)
    content = keyword2.sub('',content)
    content = keyword3.sub('<p>',content)
    content = keyword4.sub('<p>',content)
    content = keyword5.sub('<p>&nbsp;</p>\n',content)
    content = keyword6.sub('',content)
  execpt:
    print "can not parse key content."
    content = ""
  return content

def downloadIMG(content,title):
  img_uri_prefix = randomString(6)
  img_tab = re.findall(r'<img[\s\S]*?src="(\S+)?"',content)
  for list in img_tab:
    if re.search(r"nbweekly",title):
      base_url = "http://www.nbweekly.com"
      img_url = base_url + list
    elif re.search(r"nfpeople",title):
      base_url = "http://www.nfpeople.com"
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
