# -*- coding: utf-8 -*-

import os
import requests
import dateutil.parser

def get_requests(payload):
    payload['acl:consumerKey'] = os.environ['FRAMEWORX_KEY']
    print "get:", payload
    return requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)


def get_first_in_interval(requests, category, interval=10):
    times = [""]    # ダミー
    values = []

    for d in requests.json():
        date = dateutil.parser.parse(d['dc:date'])
        time = str(date.hour).zfill(2) + ":" + str((date.minute//interval)*interval).zfill(2)
        if time != times[-1]:
            times.append(time)
            values.append(d["frameworx:" + category])
    del times[0]    # ダミーを削除

    return times, values


def get_avarage_in_interval(requests, category, interval=10):
    times = [""]    # ダミー
    values = []
    tmp_values = []

    for d in requests.json():
        date = dateutil.parser.parse(d['dc:date'])
        time = str(date.hour).zfill(2) + ":" + str((date.minute//interval)*interval).zfill(2)
        tmp_values.append(d["frameworx:" + category])
        if time != times[-1]:
            times.append(time)
            values.append(sum(tmp_values)/len(tmp_values))
            tmp_values = []

    return times[1:], values


def get_chart_data(workerId, category):
    type_list = {'step': "frameworx:WarehouseVital",
                 'calorie': "frameworx:WarehouseVital",
                 'heartrate': "frameworx:WarehouseVital"}
    payload = {'rdf:type': type_list[category],
               'frameworx:workerId': workerId}
    requests = get_requests(payload)

    value_x, value_y = get_first_in_interval(requests, category)

    data = {'label': category,
            'value_x': value_x,
            'value_y': value_y}

    return data

if __name__ == '__main__':
    pass
