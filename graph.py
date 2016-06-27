# coding:utf-8
import requests

#get calorie or step
def getVitalData(key, targetData):
    r = getRequest('frameworx:WarehouseVital', key)
    jsList = r.json()
    totalVitalDict = {}
    for js in jsList:
        workerId = js["frameworx:workerId"]
        data = js["frameworx:" + targetData]
        if (workerId != None) and (data != None) :
            totalVitalDict[workerId] = data
    return totalVitalDict

def getTotalItemNumData(key):
    r = getRequest('frameworx:WarehouseActivity', key)
    jsList = r.json()
    totalItemNumDict = {}
    for js in jsList:
        workerId = js["frameworx:workerId"]
        data = js["frameworx:itemNum"]
        if (workerId != None) and (data != None) :
            if workerId not in totalItemNumDict :
                totalItemNumDict[workerId] = 0
            totalItemNumDict[workerId] += data
    return totalItemNumDict

def getRequest(type, key):
    payload = {'rdf:type': type, 'acl:consumerKey':key}
    return requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)
