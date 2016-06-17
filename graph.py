# coding:utf-8
import requests
from pylab import *
import pandas
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import json


def getVitalData(key):
    r = getRequest('frameworx:WarehouseVital', key)
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
