# coding=UTF-8
import datetime,itertools,operator
from statisticMap import provinceMap,vendorMap

#按省份聚合
def groupProvince(listData):
    resList=[]
    for areaCode,group in itertools.groupby(sorted(listData, key=lambda k: k['areaCode']) ,operator.itemgetter('areaCode')):
        item = {
            "province":areaCode,
            "cProvince":provinceMap[areaCode],
            "time":listData[0]["day"],
	    "day":listData[0]["day"],
            "z":len(list(group))
        }
        resList.append(item)
    return resList
def groupServiceData(listData):
    resList=[]
    for serviceProvider,group in itertools.groupby(sorted(listData,key=lambda k: k['serviceProvider']),operator.itemgetter('serviceProvider')):
        item = {
            "serviceProvider":serviceProvider,
            "time":listData[0]["day"],
            "day":listData[0]["day"],
            "count":len(list(group))
        }
        resList.append(item)
    return resList
def generateSrcMap():
  data={}
  for i in range(0,40):
    data[str(100000+i)]={
        "total_num":0,
        "succ_num":0
    }
  return data
def groupSrcData(singleData,map,value):
  if singleData["O:src"]=="":
    map["100000"][value]+=1
  elif len(singleData["O:src"])==6:
    map[singleData["O:src"]][value]+=1
  else:
    map[singleData["O:src"][0:6]][value]+=1
