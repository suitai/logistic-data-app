import requests
from pylab import *
import pandas
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def getVitalData():
    payload = {'rdf:type':'frameworx:WarehouseVital', 'acl:consumerKey':''}
    r = requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)
    jsList = r.json()
    workerIdSet = set([])
    maxcalDict = {}
    for js in jsList:
        workerIdSet.add(js["frameworx:workerId"])

    for workerId in workerIdSet:
        maxcalDict[workerId] = 0

    for js in jsList:
        cal = js["frameworx:calorie"]
        workerId = js["frameworx:workerId"]
        if maxcalDict[workerId] < cal:
            maxcalDict[workerId] = cal
    print maxcalDict
    return maxcalDict

def getLogData():
    payload = {'rdf:type':'frameworx:WarehouseActivity', 'acl:consumerKey':''}
    r = requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)
    jsList = r.json()
    workerIdSet = set([])
    totalItemNumDict = {}

    for js in jsList:
        workerIdSet.add(js["frameworx:workerId"])

    for workerId in workerIdSet:
        totalItemNumDict[workerId] = 0

    for js in jsList:
        workerId = js["frameworx:workerId"]
        if js["frameworx:itemNum"] != None :
            totalItemNumDict[workerId] += js["frameworx:itemNum"]
    print totalItemNumDict
    return totalItemNumDict


itemNum = getLogData()
itemNumX = itemNum.keys()
itemNumY = itemNum.values()
plt.bar(itemNumX, itemNumY,)
plt.xlabel("worker Id", fontsize=22)
plt.ylabel("total item num", fontsize=22)
plt.show()

maxCal = getVitalData()
maxCalX = maxCal.keys()
maxCalY = maxCal.values()
plt.bar(maxCalX, maxCalY)
plt.xlabel("worker Id", fontsize=22)
plt.ylabel("total calories", fontsize=22)
plt.show()
