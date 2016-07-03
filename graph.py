# coding:utf-8
import requests
import numpy

# get calorie or step
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

def getMoveDistance(key):
    r = getRequest('frameworx:WarehousePosition', key)
    jsList = r.json()
    workerIdSet = set([])
    totalDistanceDict = {}
    beforePointDict = {}
    for js in jsList:
        workerId = js["frameworx:workerId"]
        pointx = js["frameworx:x"]
        pointy = js["frameworx:y"]
        if workerId not in beforePointDict :
            beforePointDict[workerId]  = [pointx,pointy]
        distance = int(numpy.sqrt((pointx - beforePointDict[workerId][0]) ** 2 + (pointy - beforePointDict[workerId][1]) ** 2))
        if workerId not in totalDistanceDict :
            totalDistanceDict[workerId] = distance
        else:
            totalDistanceDict[workerId] += distance
        beforePointDict[workerId]  = [pointx,pointy]
    return totalDistanceDict

def getRequest(type, key):
    payload = {'rdf:type': type, 'acl:consumerKey':key}
    return requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)