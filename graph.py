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
    for js in jsList:
        workerIdSet.add(js["frameworx:workerId"])
    for workerId in workerIdSet:
        rPerson = getPersonRequest('frameworx:WarehousePosition', key, workerId)
        jsPersonList = rPerson.json()
        pointxBefore = None
        pointyBefore = None
        totalDistance = 0
        for jsPerson in jsPersonList:
            pointx = jsPerson["frameworx:x"]
            pointy = jsPerson["frameworx:y"]
            if (pointxBefore is None) or (pointyBefore is None):
                pointxBefore = pointx
                pointyBefore = pointy
            distance = numpy.sqrt((pointx - pointxBefore) ** 2 + (pointy - pointyBefore) ** 2)
            totalDistance += distance
        totalDistanceDict[workerId] = int(totalDistance)
    return totalDistanceDict


def getRequest(type, key):
    payload = {'rdf:type': type, 'acl:consumerKey':key}
    return requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)

def getPersonRequest(type, key , id):
    payload = {'rdf:type': type, 'acl:consumerKey':key, 'frameworx:workerId':id}
    return requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)
