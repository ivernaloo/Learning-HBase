#coding=UTF-8
import time
import requests
import ast
import pymongo
from datetime import datetime,date,timedelta
import calendar
import schedule
client=pymongo.MongoClient("localhost",27017)
db=client.orderStatistic
print "成功连接MongoDB:    "+str(db.authenticate('qilianshan', 'qilianshan', source='orderStatistic'))
def cacheData(startDay,endDay):
  requestData={
    "endTime":startDay+" 00:00:00",
    "startTime":endDay+" 23:59:59",
    "page":1,
    "start":0,
    "limit":30,
    "spType":"",
    "serviceProvider":""
  }
  reque=requests.get('http://admin.sec.miui.com/floworderunity/flowOrderBillStatistics.do',params=requestData)
  print reque.text.encode('utf-8')
  return reque.text
def getNubmersOfDaysOfLastMonth():
  lastDayOfLastMonth=datetime.today().replace(day=1)-timedelta(days=1)
  return calendar.monthrange(lastDayOfLastMonth.year,lastDayOfLastMonth.month)[1]
def saveSummary(lastDate):
  #存储最近七天
  startDay=(datetime.now()-timedelta(days=lastDate)).strftime("%Y-%m-%d")
  print startDay
  endDay=(datetime.now()-timedelta(days=lastDate+6)).strftime("%Y-%m-%d")
  print endDay

  dayDelta=getNubmersOfDaysOfLastMonth()  
  startDayLastMonth=(datetime.now()-timedelta(days=dayDelta+lastDate)).strftime("%Y-%m-%d")
  print startDayLastMonth
  endDayLastMonth=(datetime.now()-timedelta(days=dayDelta+lastDate+6)).strftime("%Y-%m-%d")
  print endDayLastMonth
  text=cacheData(startDay,endDay)
  textLastMonth=cacheData(startDayLastMonth,endDayLastMonth)
  db.orderStatisticCom.insert_one({
    "day":datetime.now().strftime("%Y-%m-%d"),
    "data":text,
    "dataLastMonth":textLastMonth
  })
  #存储上个月同期
for i in range(1,7):
  saveSummary(i)
#cacheData("2016-07-04","2016-06-28")

