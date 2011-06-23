Useage:
1. install kindlegen which is amazon's offical mobi generate tool from running the scrip : install_kindlegen.sh
2. add main_.py to you server's crontab, run it once a day. for example:
     00 11 * * * cd /home/user/mobi-magazine-gen; python main_.py
     run the program at 11:00 am erveryday.
     
Config:
modify the config file: config.cfg
change the directory on SYSTEM section.
change the "run weekday" for your need.

项目页面： http://mobi.pagebrin.com/
目前每周按时提供南方周末、南都周刊，南方人物周刊的mobi格式版本。

待完成...