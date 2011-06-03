Useage:
1. install kindlegen which is amazon's offical mobi generate tool from running the scrip : install_kindlegen.sh
2. add main_.py to you server's crontab, run it once a day. for example:
     00 14 * * * cd /home/user/mobi-magazine-gen; python main_.py
     run the program at 2:00 pm erveryday.
     
Config:
modify the config file: config.cfg
change the directory on SYSTEM section.
change the "run weekday" for your need.

待完成...