# coding:utf-8
import requests
import numpy
import json
import os
import urlparse
import redis

url = urlparse.urlparse(os.environ.get('REDISCLOUD_URL'))
red = redis.Redis(host=url.hostname, port=url.port, password=url.password)

# get calorie or step
def getVitalData(key, targetData):
    data = red.get(targetData)
    if data:
        return json.loads(data)

    r = getRequest('frameworx:WarehouseVital', key)
    jsList = r.json()
    totalVitalDict = {}

    for js in jsList:
        workerId = js["frameworx:workerId"]
        data = js["frameworx:" + targetData]
        if (workerId != None) and (data != None) :
            totalVitalDict[workerId] = data
    red.set(targetData, json.dumps(totalVitalDict), ex=600)
    return totalVitalDict


def getTotalItemNumData(key):
    data = red.get('itemNum')
    if data:
        return json.loads(data)

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

    red.set('itemNum', json.dumps(totalItemNumDict), ex=600)

    return totalItemNumDict


def getMoveDistance(key):
    data = red.get('distance')
    if data:
        return json.loads(data)

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

    for key in totalDistanceDict.keys():
        totalDistanceDict[key] /= 100

    red.set('distance', json.dumps(totalDistanceDict), ex=600)

    return totalDistanceDict

def getRequest(type, key):
    payload = {'rdf:type': type, 'acl:consumerKey':key}
    print "get:", payload
    return requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)
