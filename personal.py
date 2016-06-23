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

if __name__ == '__main__':
    pass
