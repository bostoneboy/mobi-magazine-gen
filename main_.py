#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import time
import random
from shutil import move
from ConfigParser import ConfigParser

import RSSparse
import PAGEparse
import OPFgen

def writeFile(filename,open_type,write_content):
  action = open(filename,open_type)
  action.write(write_content)
  action.close()
  
def randomString(count):
  basestring = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
  return "".join(random.sample(basestring,count))
  
def makeDir(directory):
  if not os.path.isdir(directory):
    os.mkdir(directory)
  else:
    pass
    
def kindleGen(opf_file,mobi_file):
  param = " -c1 -verbose -o "
  command = "kindlegen " + opf_file + param + mobi_file
  os.system(command)
  
def main():
  # read the config file.
  config_file = "config.cfg"
  config = ConfigParser()
  config.read(config_file)
  
  base_dir     = config.get("SYSTEM","base directory")
  mobi_dir     = config.get("SYSTEM","mobi directory")
  run_weekday  = config.get("SYSTEM","run weekday")
  database_dir = config.get("SYSTEM","temp directory")
  config_file  = os.path.join(base_dir,"config.cfg")
  
  makeDir(database_dir)
  makeDir(mobi_dir)
  
  config_list = config.sections()
  rss_list    = [i for i in config_list if re.search(r"RSS",i)]
  for item in rss_list:
    title        = config.get(item,"title")
    creator      = config.get(item,"creator")
    publisher    = config.get(item,"publisher")
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

    date      = time.strftime("%Y-%m-%d", time.localtime())
    date_week = time.strftime("%Y%W", time.localtime())
    find_key  = find_key.split(",")
    bookid    = randomString(12)
    
    title2   = title + "-" + date_week
    database = title2 + ".db"
    database = os.path.join(database_dir,database)

    # RSS parse and compare for today and yestoday
    content = RSSparse.fetchHtml(url)
    if re.search(r'nfpeople',url):
      list_today = RSSparse.fetchListNFpeople(content)
    else:
      list_today = RSSparse.fetchList(content,findall_key,find_key)
    if os.path.isfile(database):
      list_yesterday = RSSparse.resolvetoList(database)
      list_today = RSSparse.compareListday(list_today,list_yesterday)
    RSSparse.writeDatabase(database,list_today)
    
    weekday = time.strftime("%w", time.localtime())
    if weekday != run_weekday:
      continue
    else:
      pass
    
    # RSS compare and compare for this week and last week.
    unixtime_lastweek = time.time() - (3600 * 24 * 7)
    date_lastweek = time.strftime("%Y%W", time.localtime(unixtime_lastweek))
    database_lastweek = title + "-" + date_lastweek + ".db"
    database_lastweek = os.path.join(database_dir,database_lastweek)
    if os.path.isfile(database_lastweek):
      list_lastweek = RSSparse.resolvetoList(database_lastweek)
      list_thisweek = RSSparse.resolvetoList(database)
      list_now = RSSparse.compareListweek(list_thisweek,list_lastweek)
      RSSparse.writeDatabase(database,list_now)
    else:
      pass
      
    temp_dir = os.path.join(config.get("SYSTEM","temp directory"),str(int(time.time())))
    makeDir(temp_dir)
    os.chdir(temp_dir)
    
    # PAGE parse
    list_index = RSSparse.resolvetoList(database)
    index = 1
    for i in list_index:
      # if re.search(r"nbweekly",title):
      #   temp_head = "<h1>%s</h1>\n" % i[2]
      #   page = temp_head + i[3]
      # else:
      html_content = RSSparse.fetchHtml(i[1])
      page = PAGEparse.pageFormat(html_content,pageparse_keyword)
      page_downloadimg = PAGEparse.downloadIMG(page,title)
      page_addbodytag = PAGEparse.addBodytag(page_downloadimg)
      page_entire = PAGEparse.htmlHeader() + page_addbodytag
      out_filename = str(index) + ".html"
      #out_filename = temp_dir + out_filename
      PAGEparse.writeHtml(out_filename,page_entire)
      index += 1

    # OPF generation
    opf_metadata = OPFgen.opfMetadata(item,config_file)
    opf_entire = OPFgen.opfHeader(bookid) + opf_metadata + OPFgen.opfMainfest(list_index) + OPFgen.opfSpine(list_index) + OPFgen.opfGuide() + OPFgen.opfFooter()
    opf_filename = "index.opf"
    writeFile(opf_filename,"w",opf_entire)

    # INDEX html file generation
    html_header = OPFgen.htmlHeader()
    html_body = OPFgen.htmlBody(list_index)
    html_body = OPFgen.addBodytag(html_body)
    index_entire = html_header + html_body
    html_filename = "0.html"
    writeFile(html_filename,"w",index_entire)

    # KUG.ncx generation
    ncx_header = OPFgen.ncxHeader()
    ncx_head = OPFgen.ncxHead(bookid)
    ncx_doctitle = OPFgen.ncxDocTitle(title2)
    ncx_docauthor = OPFgen.ncxDocAuthor(creator)
    ncx_entirenavpoint = OPFgen.ncxEntireNavPoint(list_index)
    ncx_navmap = OPFgen.ncxNavMap(ncx_entirenavpoint)
    ncx_body = ncx_head + ncx_doctitle + ncx_docauthor + ncx_navmap
    ncx_body = OPFgen.ncxBody(ncx_body)
    ncx_entire = ncx_header + ncx_body
    ncx_filename = "KUG.ncx"
    writeFile(ncx_filename,"w",ncx_entire)
    
    # genaration the .mobi file use system tool kindlegen
    opf_file = "index.opf"
    mobi_file = title2 + ".mobi"
    if os.path.isfile(os.path.join(mobi_dir,mobi_file)):
      mobi_file = title2 + "-" + randomString(6) + ".mobi"
    kindleGen(opf_file,mobi_file)
    move(mobi_file,mobi_dir)

if __name__ == "__main__":
  main()
