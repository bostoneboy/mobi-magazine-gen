#!/usr/bin/env python

from pymongo import Connection

db = Connection().test

input = input("1/infzm, 2/nbweekly, 3/nfpeople: ")

if input == 1:
  collection = 'infzm'
elif input == 2:
  collection = 'nbweekly'
elif input ==3:
  collection = 'nfpeople'
collection = "rss_" + collection

post = db[collection]
list_yes = post.find({'is_operate':'yes'}).sort('insert_time')
list_no = post.find({'is_operate':'no'}).sort('insert_time')
for i in list_yes:
  print i['is_operate'],i['date'],i['insert_time'],i['exception'],i['link']
for j in list_no:
  print j['is_operate'],j['date'],j['insert_time'],j['exception'],j['link']
