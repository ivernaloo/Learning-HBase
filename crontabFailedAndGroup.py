#coding=UTF-8
import schedule
import time
from __init__ import saveOrderData
#增杰约束

def jobOrder():
  while True:
    try:
      saveOrderData(1,50000,True,True,True,True,True)
    except NameError:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)  # Log it or whatever here:i
      continue
    break
schedule.every().day.at("8:20").do(jobOrder)

while 1:
  schedule.run_pending()
  time.sleep(1)
