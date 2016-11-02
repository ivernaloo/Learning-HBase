#coding=UTF-8
#import sys
#sys.path.append('../gen-py')
import pymongo
import happybase
from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.transport import THttpClient
from thrift.protocol import TBinaryProtocol
from hbase import THBaseService
from hbase.ttypes import *
import redis,datetime
from datetime import date, timedelta
from apscheduler import *
import sys
import traceback
from groupFunction import groupProvince,groupServiceData,generateSrcMap,groupSrcData
from statisticMap import provinceMap,vendorMap
import schedule,time
#import BlockingScheduler
#BlockingScheduler=apscheduler.schedulers.blocking

#connect hbase
tablesCon=happybase.Connection(host='localhost',timeout=600000,port=9092)
tablesCon.open()
print "HBase successfully connected，table list：  "+str(tablesCon.tables())
#create connection of table miui_sec:flow_order_order
orderOrder=tablesCon.table('miui_sec:flow_order_order')

#connect MongoDB
client=pymongo.MongoClient("localhost",27017)
db=client.orderStatistic;
print "MongoDB mongoDB successfully connected:    "+str(db.authenticate('qilianshan', 'qilianshan', source='orderStatistic'))


#根据日期查询数据函
def getDataByDate(date,size):
  try:
    #统计失败订单
    failedOrderData=[]
    srcMap=generateSrcMap()
    #所有数据
    orderResultSet=orderOrder.scan(filter="RowFilter(=,'substring:"+str(date)+"')",batch_size=size,limit=size)
    #一共渠道的数据
    count=0
    totalFlow=0
    for key,data in orderResultSet:
    #  print key,data['O:orderStatus']
      count+=1
      groupSrcData(data,srcMap,"total_num")
      if int(data['O:orderStatus'])%11!=0:
        #print key,data
        failedOrderData.append(data)
      else:
        totalFlow+=int(data['O:flowTotal'])
        groupSrcData(data,srcMap,"succ_num")
    print "get "+str(count)+" total data from hbase"
  except NameError:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    print ''.join('!! ' + line for line in lines)  # Log it or whatever here
  returnJSON={
    "failedOrderData":failedOrderData,
    "srcMapData":srcMap,
    "totalDataMap":{
      "totalCount":count,
      "succeed":count-len(failedOrderData),
      "totalFlow":totalFlow
    }
  }
  print returnJSON['totalDataMap']
  return returnJSON
#存储json
def saveJsonToDB(list):
  for data in list:
    for i in data:
      data[i.translate(None,"O:")]=data.pop(i) 
    data['day']=data['payTime'].split(' ')[0] 
  return db.orderFailed.insert_many(list)
#存储前一天数据
def saveOrderData(deltaDay,size,ifSaveFailedDataToDB,ifHandleData,ifGroupData,ifSaveSrcMap,ifSaveTotalDataMap):
  try:
    deltaDay # does a exist in the current namespac
  except NameError:
    deltaDay = 1 # nope
  targetDate=(datetime.datetime.now() - datetime.timedelta(days=deltaDay));
  targetDateFormatted=targetDate.strftime("%Y-%m-%d")
  print "Scaning data of "+str(deltaDay)+" days ago,Date："+targetDateFormatted
  resultDict=getDataByDate(targetDate.strftime("%Y%m%d"),size)
  print "get "+str(len(resultDict["failedOrderData"]))+" failed data from hbase"
  print resultDict["srcMapData"]
  #如果开关打开，而且数据库内没数据，则进行存储
  if ifSaveFailedDataToDB and db.orderFailed.count({"day":targetDateFormatted})==0:
    saveJsonToDB(resultDict["failedOrderData"])
    print "Failed order count in mongoDB:"+str(db.orderFailed.count({"day":targetDateFormatted}))
  if ifHandleData:
    handleData(targetDateFormatted,targetDateFormatted)
  #如果没有聚合过，则聚合存储
  if ifGroupData and db.groupProvinceData.count({"day":targetDateFormatted})==0 and db.groupServiceData.count({"day":targetDateFormatted})==0:
    groupData(targetDateFormatted,targetDateFormatted,1,1)
  #
  if ifSaveSrcMap and db.orderSrc.count({"day":targetDateFormatted})==0:
    db.orderSrc.insert_one({
      "day":targetDateFormatted,
      "data":resultDict["srcMapData"]
    })
  #
  if ifSaveTotalDataMap and db.totalDataMap.count({"day":targetDateFormatted})==0:
    db.totalDataMap.insert_one({
      "data":resultDict["totalDataMap"],
      "day":targetDateFormatted
    })
#获取数据
def getList(queryJson):
  resultlist=list(db.orderFailed.find(queryJson))
  return resultlist

#%Y-%m-%d
def getDateList(startDate,endDate):
  dateList=[]
  listStartDate=startDate.split('-')
  listEndDate=endDate.split('-')
  d1=date(int(listStartDate[0]),int(listStartDate[1]),int(listStartDate[2]))
  d2=date(int(listEndDate[0]),int(listEndDate[1]),int(listEndDate[2]))
  delta=d2-d1
  for i in range(delta.days+1):
    print d1+timedelta(days=i)
    dateList.append(str(d1+timedelta(days=i)))
  return dateList
#处理运营商和运营商
def handleData(startDate,endDate):
  for date in getDateList(startDate,endDate):
    print date+":data processed,add province and serviceProvider"
    #update province
    for key in provinceMap:
      db.orderFailed.update_many({"day":date,"areaCode":key},{"$set":{"province":provinceMap[key]}});
    for key in vendorMap:
      db.orderFailed.update_many({"day":date,"serviceProvider":key},{"$set":{"serviceProvider":vendorMap[key],"serviceProviderCode":key}})

def groupData(startDate,endDate,getProvince,getService):
  dates=getDateList(startDate,endDate)
  for date in dates:
    listData=getList({"day":date})
    if getProvince==1:
      db.groupProvinceData.insert_many(groupProvince(listData))
    if getService==1:
      db.groupServiceData.insert_many(groupServiceData(listData))
    print date+":data grouped,by province and serviceProvider"
#入口函数集

#添加province and provider
#handleData("2016-07-27","2016-07-27") 

#聚合数据group by province and provider
#groupData("2016-07-27","2016-07-27",1,1)

#存储前一天的数据(
#前i天,
#扫描数量,
#是否存储，
#是否添加province和serviceprovider字段，
#是否分省分运营商
#是否进行分渠道统计
#)
for i in range(1,3):
  saveOrderData(i,50000,True,True,True,True,True)
#saveOrderData(1,50000,True,True,True,True,True)
