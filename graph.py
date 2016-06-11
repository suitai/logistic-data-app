# coding:utf-8
import requests
from pylab import *
import pandas
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys

param = sys.argv
key = param[1]

def getVitalData():
    r = getReuqest('frameworx:WarehouseVital', key)
    jsList = r.json()
    workerIdSet = set([])
    totalCalDict = {}
    totalStepDict = {}
    for js in jsList:
        workerIdSet.add(js["frameworx:workerId"])

    for workerId in workerIdSet:
        totalCalDict[workerId] = 0
        totalStepDict[workerId] = 0

    for js in jsList:
        cal = js["frameworx:calorie"]
        step = js["frameworx:step"]
        workerId = js["frameworx:workerId"]
        if totalCalDict[workerId] < cal:
            totalCalDict[workerId] = cal
        if totalStepDict[workerId] < step:
            totalStepDict[workerId] = step

    print totalCalDict, totalStepDict
    return [totalCalDict, totalStepDict]

def getLogData():
    r = getReuqest('frameworx:WarehouseActivity', key)
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

def getReuqest(type, key):
    payload = {'rdf:type': type, 'acl:consumerKey':key}
    return requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)

itemNum = getLogData()
itemNumX = itemNum.keys()
itemNumY = itemNum.values()
plt.bar(itemNumX, itemNumY,)
plt.title("title", fontsize=22)
plt.xlabel("worker Id", fontsize=22)
plt.ylabel("total item num", fontsize=22)
plt.show()

vitalData = getVitalData()

totalCal = vitalData[0]
totalCalX  = totalCal.keys()
totalCalY = totalCal.values()
plt.bar(totalCalX , totalCalY)
plt.title("title", fontsize=22)
plt.xlabel("worker Id", fontsize=22)
plt.ylabel("total calories", fontsize=22)
plt.show()

totalStep = vitalData[1]
totalStepX  = totalStep.keys()
totalStepY = totalStep.values()
plt.bar(totalStepX , totalStepY)
plt.title("title", fontsize=22)
plt.xlabel("worker Id", fontsize=22)
plt.ylabel("total step", fontsize=22)
plt.show()
