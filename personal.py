# -*- coding: utf-8 -*-

import os
import requests
import dateutil.parser

def get_requests(payload):
    payload['acl:consumerKey'] = os.environ['FRAMEWORX_KEY']
    print "get:", payload
    return requests.get("https://api.frameworxopendata.jp/api/v3/datapoints", params=payload)

def get_chart_data(workerId, category):
    type_list = {'step': "frameworx:WarehouseVital",
                 'calorie': "frameworx:WarehouseVital",
                 'heartrate': "frameworx:WarehouseVital"}
    payload = {'rdf:type': type_list[category],
               'frameworx:workerId': workerId}
    times = [""]    # ダミー
    values = []

    for d in get_requests(payload).json():
        date = dateutil.parser.parse(d['dc:date'])
        time = str(date.hour).zfill(2) + ":" + str((date.minute//10)*10).zfill(2)
        if time != times[-1]:
            times.append(time)
            values.append(d["frameworx:" + category])
    del times[0]    # ダミーを削除

    data = {'label': category,
            'value_x': times,
            'value_y': values}

    return data

if __name__ == '__main__':
    pass
