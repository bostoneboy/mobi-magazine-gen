#!/usr/bin/python

import urllib
import os
import sys

try:
	 urllib.urlretrieve("file:///c:/did.jpg","ksdiej.jpg")
except:
	 print "cannot not to retrieve image on the server"

	 
print "hello,wordl."