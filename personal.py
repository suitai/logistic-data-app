# -*- coding: utf-8 -*-

import os
import json
import requests
import dateutil.parser
import numpy

URL = "https://api.frameworxopendata.jp/"

def get_requests(payload, path="api/v3/datapoints"):
    payload['acl:consumerKey'] = os.environ['FRAMEWORX_KEY']
    data =  requests.get(URL+path, params=payload)
    print "get:", payload
    with open("requests.json", 'w') as f:
        json.dump(data.json(), f)
    return data


def get_time(date_org, interval):
    date = dateutil.parser.parse(date_org)
    return str(date.hour).zfill(2) + ":" + str((date.minute//interval)*interval).zfill(2)


def get_vital_data(workerId, interval=10):
    times = [""]
    calorie = {'log': [], 'title': u"合計", 'result': 0, 'unit': u"kcal"}
    step = {'log': [], 'title': u"合計", 'result': 0, 'unit': u"歩"}
    heartrate = {'log': [], 'title': u"平均", 'result': 0, 'unit': "bpm"}
    tmp_heartrates = []

    payload = {'rdf:type': "frameworx:WarehouseVital",
               'frameworx:workerId': workerId}
    requests = get_requests(payload)

    for d in requests.json():
        if d['dc:date']:
            time = get_time(d['dc:date'], interval)
            tmp_heartrates.append(d["frameworx:heartrate"])
            calorie['result'] = int(d["frameworx:calorie"])
            step['result'] = int(d["frameworx:step"])
            if time != times[-1]:
                times.append(time)
                calorie['log'].append(calorie['result'])
                step['log'].append(step['result'])
                heartrate['log'].append(sum(tmp_heartrates)/len(tmp_heartrates))
                tmp_heartrates = []

    if len(heartrate['log']) > 0:
        heartrate['result'] = sum(heartrate['log'])/len(heartrate['log'])

    vital_data = {
            u'時間': times[1:],
            u'カロリー': calorie,
            u'歩数': step,
            u'脈拍': heartrate}

    return vital_data


def get_sensor_data(workerId, interval=10):
    times = [""]
    temperature = {'log': [], 'title': u"平均", 'result': 0, 'unit': u"℃"}
    humidity = {'log': [], 'title': u"平均", 'result': 0, 'unit': "%"}
    tmp_temperature = []
    tmp_humidity = []

    payload = {'rdf:type': "frameworx:WarehouseSensor",
               'frameworx:workerId': workerId}
    requests = get_requests(payload)

    for d in requests.json():
        if d['dc:date']:
            time = get_time(d['dc:date'], interval)
            tmp_temperature.append(d["frameworx:temperature"])
            tmp_humidity.append(d["frameworx:humidity"])
            if time != times[-1]:
                times.append(time)
                temperature['log'].append(sum(tmp_temperature)/len(tmp_temperature))
                humidity['log'].append(sum(tmp_humidity)/len(tmp_humidity))
                tmp_temperature = []
                tmp_humidity = []

    if len(temperature['log']) > 0:
        temperature['result'] = round(sum(temperature['log'])/len(temperature['log']), 1)
    if len(humidity['log']) > 0:
        humidity['result'] = round(sum(humidity['log'])/len(humidity['log']), 1)

    sensor_data = {
            u'時間': times[1:],
            u'気温': temperature,
            u'湿度': humidity}

    return sensor_data


def get_activity_data(workerId, interval=10):
    location = {}

    payload = {'rdf:type': "frameworx:WarehouseLocation"}
    requests = get_requests(payload)
    for d in requests.json():
        location[(d['frameworx:shelfId'])] = numpy.array([int(d['frameworx:x']), int(d['frameworx:y'])])

    times = [""]
    itemNum = {'log': [], 'title': u"合計", 'result': 0, 'unit': u"個"}
    distance = {'log': [], 'title': u"合計", 'result': 0, 'unit': "m"}
    locations = [numpy.array([2500, 2500])]
    shelfIds = [""]

    payload = {'rdf:type': "frameworx:WarehouseActivity",
               'frameworx:workerId': workerId}
    requests = get_requests(payload)

    for d in sorted(requests.json(), key=lambda x: x['dc:date']):
        if d['dc:date']:
            time = get_time(d['dc:date'], interval)
            if d["frameworx:itemNum"]:
                itemNum['result'] += int(d["frameworx:itemNum"])

            if d["frameworx:shelfId"]:
                if d["frameworx:shelfId"] != shelfIds[-1]:
                    if d["frameworx:shelfId"] in location:
                        distance['result'] += int(numpy.linalg.norm(location[(d['frameworx:shelfId'])] - locations[-1])/100)
                        shelfIds.append(d["frameworx:shelfId"])
                        locations.append(location[d["frameworx:shelfId"]])
                    else:
                        print "Can not find the shelfId ", d["frameworx:shelfId"]

            if time != times[-1]:
                times.append(time)
                itemNum['log'].append(itemNum['result'])
                distance['log'].append(distance['result'])

    activity_data = {
            u'時間': times[1:],
            u'商品数': itemNum,
            u'距離': distance,
            u'座標': locations[1:],
            u'シェルフ': shelfIds[1:]}

    return activity_data

def set_data(data, tmp_data, category, member):
    for c in category:
        if c in member:
            data.append({
                'label': c,
                'value_x': tmp_data[u'時間'],
                'value_y': tmp_data[c]['log'],
                'title': tmp_data[c]['title'],
                'result': tmp_data[c]['result'],
                'unit': tmp_data[c]['unit']})

def get_log_data(workerId, category):
    data = []
    print "workerId:", workerId
    print "category:", category

    if u"カロリー" in category or u"歩数" in category or u"脈拍" in category:
        tmp_data = get_vital_data(workerId)
        set_data(data, tmp_data, category, [u"カロリー", u"歩数", u"脈拍"])

    if u"商品数" in category or u"距離" in category:
        tmp_data = get_activity_data(workerId)
        set_data(data, tmp_data, category, [u"商品数", u"距離"])

    if u"気温" in category or u"湿度" in category:
        tmp_data = get_sensor_data(workerId)
        set_data(data, tmp_data, category, [u"気温", u"湿度"])

    return data


def get_summary_data(workerId):
    data = {}
    calorie = 2000.0
    step = 5000.0
    itemNum = 500.0
    distance = 1000.0

    print "workerId:", workerId

    tmp_data = get_vital_data(workerId)
    data[u'カロリー'] = int(((tmp_data[u'カロリー']['result']/calorie)*100))
    data[u'歩数'] = int(((tmp_data[u'歩数']['result']/step)*100))

    tmp_data = get_activity_data(workerId)
    data[u'商品数'] = int(((tmp_data[u'商品数']['result']/itemNum)*100))
    data[u'距離'] = int(((tmp_data[u'距離']['result']/distance)*100))

    return data

if __name__ == '__main__':
    pass
