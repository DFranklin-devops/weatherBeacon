#!/usr/bin/env python3

from time import time
from math import floor
import datetime
import requests


class Collector:
    def __init__(self):
        self.last_updated = 0
        self.data = None

    def get_data(self):
        if int(time()) - self.last_updated > 900:
            print("Data is stale; fetching...")
            payload = {
                'zip': '02108',
                'APPID': '91bdc35a82d8312a2549944ac06b0eb4',
                'mode': 'json',
                'units': 'imperial',
                'cnt': '1'
            }

            try:
                r = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                                 params=payload)
            except requests.exceptions.ConnectionError:
                print("Oh fuck")
                return False

            self.data = r.json()
            self.last_updated = int(time())

#        print("Data not stale - the time is ", int(time()),\
#            "and the last update is ",self.last_updated)
        return self.data

    def get_forecast_time(self):
        data = self.get_data()
        if "list" in data and len(data["list"]):
            day = data["list"][0]
        thedt = day["dt"]
        if "city" in data and len(data["city"]):
            loc = data["city"]
        offset = loc["timezone"]
        thedt += offset
        string_timestamp = datetime.datetime.fromtimestamp(thedt)
        str_now = datetime.datetime.fromtimestamp(time())
        print("Time now ", str_now.strftime("%H:%M:%S"))
        print("Forecast valid until", string_timestamp.strftime("%H:%M:%S"))

    def get_text(self):
        data = self.get_data()

        if "list" in data\
           and len(data["list"]):

            day = data["list"][0]

        desc = day["weather"][0]["description"]
        desc += " " * (16 - len(desc))

        temp = "%s/%s" % (int(day["temp"]["max"]),
                          int(day["temp"]["min"]))

        if len(desc) == 16:
            temp = (" " * (int(floor((15 - len(temp)) / 2)))) + temp
        else:
            temp = " (%s)" % temp

        return "%s%s" % (desc, temp)

    def get_id(self):
        data = self.get_data()

        if "list" in data \
           and len(data["list"]) \
           and "weather" in data["list"][0] \
           and len(data["list"][0]["weather"]) \
           and "id" in data["list"][0]["weather"][0]:

            return int(data["list"][0]["weather"][0]["id"])

        # Return "clear" by default
        return 800
