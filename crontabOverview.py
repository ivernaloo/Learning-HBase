#coding=UTF-8
import schedule
import time
from cacheOverViewData import saveSummary
#增杰约束
def jobCache():
  saveSummary(1)
schedule.every().day.at("4:38").do(jobCache)

while 1:
  schedule.run_pending()
  time.sleep(1)
