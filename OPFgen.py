#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import random
import RSSparse
from ConfigParser import ConfigParser

def randomString(count):
  basestring = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
  return "".join(random.sample(basestring,count))

##########################################
###### genenaration the opf file: index.opf
def opfHeader(bookid):
  bookid = randomString(12)
  head = '''<?xml version="1.0" encoding="utf-8"?>
            <package version="2.0" xmlns:opf="http://www.idpf.org/2007/opf" unique-identifier="%s">''' % bookid
  return head + "\n"

def metadataTag(tagname,value):
  if not value:
    line = "<dc:%s/>\n" % tagname
  else:
    line = '<dc:%s>%s</dc:%s>\n' % (tagname,value,tagname)
  return line

def opfMetadata(item,config_file):
  config = ConfigParser()
  config.read(config_file)
  title        = config.get(item,"title")
  creator      = config.get(item,"creator")
  publisher    = config.get(item,"publisher")
  date         = config.get(item,"date")
  source       = config.get(item,"source")
  rights       = config.get(item,"rights")
  subject      = config.get(item,"subject")
  description  = config.get(item,"description")
  contributor  = config.get(item,"contributor")
  type2        = config.get(item,"type2")
  format2      = config.get(item,"format2")
  identifier   = config.get(item,"identifier")
  language     = config.get(item,"language")
  relation     = config.get(item,"relation")
  coverage     = config.get(item,"coverage")

  url                = config.get(item,"rss_url")
  findall_key        = config.get(item,"findall key")
  find_key           = config.get(item,"find key")
  pageparse_keyword  = config.get(item,"pageparse keyword")

  date      = time.strftime("%Y-%m-%d", time.gmtime())
  date_week = time.strftime("%W", time.gmtime())
  title     = title + "-" + date_week
  find_key  = find_key.split(",")

  head = '''<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:opf="http://www.idpf.org/2007/opf">\n'''
  dcbody = ""
  dcbody += metadataTag("title",title)
  dcbody += metadataTag("creator",creator)
  dcbody += metadataTag("subject",subject)
  dcbody += metadataTag("description",description)
  dcbody += metadataTag("publisher",publisher)
  dcbody += metadataTag("contributor",contributor)
  dcbody += metadataTag("date",date)
  dcbody += metadataTag("type",type2)
  dcbody += metadataTag("format",format2)
  dcbody += metadataTag("identifier",identifier)
  dcbody += metadataTag("source",source)
  dcbody += metadataTag("language",language)
  dcbody += metadataTag("relation",relation)
  dcbody += metadataTag("coverage",coverage)
  dcbody += metadataTag("title",rights)
  dcbody += "</dc-metadata>\n"
  dcentire = head + dcbody
  dcentire += "<x-metadata/>\n"
  dcentire += "</metadata>\n"
  return dcentire

def mainfestLine(item_id,href,media_type="application/xhtml+xml"):
  line = '<item id="%s" href="%s" media-type="%s"/>\n' % (item_id,href,media_type)
  return line

def Indexlist(database):
  index_list = RSSparse.resolvetoList(database)
  return index_list

def opfMainfest(list_index):
  mfhead = "<manifest>\n"
  mfbody = ""
  for i in range(len(list_index) + 1):
    item_id = str(i)              
    href = item_id + ".html"
    mfbody += mainfestLine(item_id,href)
  # add index content KUG.ncx
  mfbody += mainfestLine("content_index","KUG.ncx","application/x-dtbncx+xml")
  mffoot = "</manifest>\n"
  mfentire = mfhead + mfbody + mffoot
  return mfentire
               
def spineLine(idref):
  line = '<itemref idref="%s"/>\n' % idref
  return line

def opfSpine(list_index):
  sphead = '<spine toc="content_index">\n'
  spbody = ""
  for i in range(len(list_index) + 1 ):
    idref = str(i)
    spbody += spineLine(idref)
  spfoot = "</spine>\n"
  spentire = sphead + spbody + spfoot
  return spentire

def opfGuide():
  guide_line1 = '<reference type="text" title="welcome" href="0.html"></reference>'
  guide_line2 = '<reference type="toc" title="content_index" href="0.html"></reference>'
  guide_line = "<guide>" + "\n" + guide_line1 + "\n" + guide_line2 + "\n" + "</guide>" + "\n"
  return guide_line
  
def opfFooter():
  foot = "</package>\n"
  return foot

######################################
###### gnenaration the index html file
def htmlHeader():
  head = '''<html xmlns="http://www.w3.org/1999/xhtml"> 
            <head> 
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  
            </head> '''
  return head

def addBodytag(content):
  page = "<body>" + content + "</body>"
  return page

def htmlBody(list_index):
  title = "<h1>INDEX</h1>" + "<br/>" + "\n"
  init_id = 1
  body = ""
  for item in list_index:
    line1 = "%d. " % init_id
    line2 = '<a href="%d.html">%s</a><br/>' % (init_id,item[2])
    line = line1 + line2
    body += line
    init_id += 1
  return body

######################################
###### genaration the ncx file for nav
def ncxHeader():
  header = '''<?xml version="1.0" encoding="UTF-8"?>
              <!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
	      "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">'''
  return header + "\n"

def ncxBody(body):
  ncx_mark = '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="zh-CN">'
  return ncx_mark + "\n" + body + "</ncx>" + "\n"

def ncxHead(bookid):
  head = '''<head>
            <meta name="dtb:uid" content="%s"/>
            <meta name="dtb:depth" content="-1"/>
            <meta name="dtb:totalPageCount" content="0"/>
            <meta name="dtb:maxPageNumber" content="0"/>
            </head>''' % bookid
  return head + "\n"

def ncxDocTitle(title):
  doc_title = "<docTitle><text>%s</text></docTitle>" % title
  return doc_title + "\n"

def ncxDocAuthor(creator):
  doc_author = "<docAuthor><text>%s</text></docAuthor>" % creator
  return doc_author + "\n"

def ncxNavPoint(page_id,page_title,page_src,play_order):
  nav_point = '''<navPoint id="%s" playOrder="%d">
                   <navLabel>
                     <text>%s</text>
                   </navLabel>
                 <content src="%s"/>
                 </navPoint>
              ''' % (page_id,play_order,page_title,page_src)
  return nav_point + "\n"

def ncxEntireNavPoint(list_index):
  # init the index page.
  entire_navpoint = ncxNavPoint("0","INDEX","0.html",1)
  init_id = 1
  for item in list_index:
    page_id = str(init_id)
    play_order = init_id + 1       
    page_src = page_id + ".html"
    page_title = item[2]
    nav_point = ncxNavPoint(page_id,page_title,page_src,play_order)
    entire_navpoint += nav_point
    init_id += 1
  return entire_navpoint

def ncxNavMap(nav_point):
  return "<navMap>" + "\n" + nav_point + "</navMap>" + "\n"

