#!/bin/bash
# install amazon's offical kindlegen tool.
# KindleGen Download Page: http://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000234621
# make sure you can run this script in root privileges or sudo!!!

download_url="http://s3.amazonaws.com/kindlegen/kindlegen_linux_2.6_i386_v1.2.tar.gz"
wget $download_url
tar xvf kindlegen_linux_*.tar.gz
mv kindlegen /usr/bin
if [ $? -eq 0 ]
then
  echo "\n**********kindlegen installed successful."
else
  echo "\n**********Something error occured, be sure you are root user or in sudo mode!"
fi