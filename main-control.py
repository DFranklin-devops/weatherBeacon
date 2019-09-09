#!/usr/bin/env python3

from time import sleep
#from threading import Thread, Event
#from pprint import pprint
#import signal
#import datetime
#import Queue

import collector
import json

collector = collector.Collector()
myjson = collector.get_data()

print(json.dumps(myjson, indent=4, sort_keys=True))

collector.get_forecast_time()
print("goodbye")

for counter in range(30):
    myjson = collector.get_data()
    print(json.dumps(myjson, indent=4, sort_keys=True))
    collector.get_forecast_time()
    print("Sleeping", counter, "for 16 minutes")
    sleep(960)
