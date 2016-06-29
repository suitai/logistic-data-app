# -*- coding: utf-8 -*-

import os
import json
import requests
import dateutil.parser

URL = "https://api.frameworxopendata.jp/"

def get_requests(payload, path="api/v3/datapoints"):
    payload['acl:consumerKey'] = os.environ['FRAMEWORX_KEY']
    data =  requests.get(URL+path, params=payload)
    print "get:", payload
    with open("requests.json", 'w') as f:
        json.dump(data.json(), f)
    return data

def get_first_in_interval(requests, category, interval=10):
    times = [""]    # ダミー
    values = []

    for d in requests.json():
        if d['dc:date'] and d["frameworx:" + category]:
            date = dateutil.parser.parse(d['dc:date'])
            time = str(date.hour).zfill(2) + ":" + str((date.minute//interval)*interval).zfill(2)
            if time != times[-1]:
                times.append(time)
                values.append(int(d["frameworx:" + category]))

    return times[1:], values


def get_average_in_interval(requests, category, interval=10):
    times = [""]    # ダミー
    values = []
    tmp_values = []

    for d in requests.json():
        if d['dc:date'] and d["frameworx:" + category]:
            date = dateutil.parser.parse(d['dc:date'])
            time = str(date.hour).zfill(2) + ":" + str((date.minute//interval)*interval).zfill(2)
            tmp_values.append(d["frameworx:" + category])
            if time != times[-1]:
                times.append(time)
                values.append(sum(tmp_values)/len(tmp_values))
                tmp_values = []

    return times[1:], values


def get_sum_at_interval(requests, category, interval=10):
    times = [""]    # ダミー
    values = []
    tmp_value = 0

    for d in requests.json():
        if d['dc:date'] and d["frameworx:" + category]:
            date = dateutil.parser.parse(d['dc:date'])
            time = str(date.hour).zfill(2) + ":" + str((date.minute//interval)*interval).zfill(2)
            tmp_value += int(d["frameworx:" + category])
            if time != times[-1]:
                times.append(time)
                values.append(tmp_value)

    return times[1:], values


def get_chart_data(workerId, category):
    category_dict = {'step':
                        {'payload':
                            {'rdf:type': "frameworx:WarehouseVital"},
                        'get_values': get_first_in_interval},
                     'calorie':
                        {'payload':
                            {'rdf:type': "frameworx:WarehouseVital"},
                        'get_values': get_first_in_interval},
                     'heartrate':
                        {'payload':
                            {'rdf:type': "frameworx:WarehouseVital"},
                        'get_values': get_average_in_interval},
                     'temperature':
                        {'payload':
                            {'rdf:type': "frameworx:WarehouseSensor"},
                        'get_values': get_average_in_interval},
                     'humidity':
                        {'payload':
                            {'rdf:type': "frameworx:WarehouseSensor"},
                        'get_values': get_average_in_interval},
                     'itemNum':
                        {'payload':
                            {'rdf:type': "frameworx:WarehouseActivity"},
                        'get_values': get_sum_at_interval}
                    }

    payload = category_dict[category]['payload']
    payload['frameworx:workerId'] = workerId
    requests = get_requests(payload)

    value_x, value_y = category_dict[category]['get_values'](requests, category)

    data = {'label': category,
            'value_x': value_x,
            'value_y': value_y}

    return data


def get_time(date_org, interval):
    date = dateutil.parser.parse(date_org)
    return str(date.hour).zfill(2) + ":" + str((date.minute//interval)*interval).zfill(2)


def get_vital_data(workerId, interval=10):
    times = [""]
    calories = []
    steps = []
    heartrates = []
    tmp_heartrates = []

    payload = {'rdf:type': "frameworx:WarehouseVital",
               'frameworx:workerId': workerId}
    requests = get_requests(payload)

    for d in requests.json():
        if d['dc:date']:
            time = get_time(d['dc:date'], interval)
            tmp_heartrates.append(d["frameworx:heartrate"])
            if time != times[-1]:
                times.append(time)
                calories.append(int(d["frameworx:calorie"]))
                steps.append(int(d["frameworx:step"]))
                heartrates.append(sum(tmp_heartrates)/len(tmp_heartrates))
                tmp_heartrates = []

    vital_data = {u'時間': times[1:],
                  u'カロリー': calories,
                  u'歩数': steps,
                  u'脈拍': heartrates}

    return vital_data

def get_sensor_data(workerId, interval=10):
    times = [""]
    temperature = []
    humidity = []
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
                temperature.append(sum(tmp_temperature)/len(tmp_temperature))
                humidity.append(sum(tmp_humidity)/len(tmp_humidity))
                tmp_temperature = []
                tmp_humidity = []

    sensor_data = {u'時間': times[1:],
                   u'気温': temperature,
                   u'湿度': humidity}

    return sensor_data


def get_activity_data(workerId, interval=10):
    times = [""]
    itemNums = []
    tmp_itemNums = 0

    payload = {'rdf:type': "frameworx:WarehouseActivity",
               'frameworx:workerId': workerId}
    requests = get_requests(payload)

    for d in sorted(requests.json(), key=lambda x: x['dc:date']):
        if d['dc:date']:
            time = get_time(d['dc:date'], interval)
            if d["frameworx:itemNum"]:
                tmp_itemNums += int(d["frameworx:itemNum"])
            if time != times[-1]:
                times.append(time)
                itemNums.append(tmp_itemNums)

    activity_data = {u'時間': times[1:],

    return activity_data


def get_data(workerId, category):
    data = []
    print "workerId:", workerId
    print "category:", category

    if u"カロリー" in category or u"歩数" in category or u"脈拍" in category:
        vital_data = get_vital_data(workerId)
        for c in category:
            if c in [u"カロリー", u"歩数", u"脈拍"]:
                data.append({'label': c,
                             'value_x': vital_data[u'時間'],
                             'value_y': vital_data[c]})

    if u"気温" in category or u"湿度" in category:
        sensor_data = get_sensor_data(workerId)
        for c in category:
            if c in [u"気温", u"湿度"]:
                data.append({'label': c,
                             'value_x': sensor_data[u'時間'],
                             'value_y': sensor_data[c]})

    if u"商品数" in category:
        activity_data = get_activity_data(workerId)
        for c in category:
            if c in [u"商品数"]:
                data.append({'label': c,
                             'value_x': activity_data[u'時間'],
                             'value_y': activity_data[c]})

    return data

if __name__ == '__main__':
    pass
