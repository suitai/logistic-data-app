# coding:utf-8
# from pylab import *
# import pandas
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
import requests
import sys
import json

def getVitalData(key, targetData):
    r = getRequest('frameworx:WarehouseVital', key)
    jsList = r.json()
    workerIdSet = set([])
    totalVitalData = {}
    for js in jsList:
        workerIdSet.add(js["frameworx:workerId"])

    for workerId in workerIdSet:
        totalVitalData[workerId] = [0]

    for js in jsList:
        cal = js["frameworx:" + targetData]
        workerId = js["frameworx:workerId"]
        if totalVitalData[workerId][0] < cal:
            totalVitalData[workerId][0] = cal

    return totalVitalData

def getLogData(key):
    r = getRequest('frameworx:WarehouseActivity', key)
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


def getRequest(type, key):
    payload = {'rdf:type': type, 'acl:consumerKey':key}
    return requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)
