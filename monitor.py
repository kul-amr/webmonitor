"""
This module reads the config json to get the websites to monitor and
collects the connection stats about those.
"""
import json
from time import sleep
from src import *


def monitor():
    while True:
        with open("./websites.json", "r") as webjson:
            websites = json.load(webjson)
            print("monitoring started for : ")
            print(websites)

            for web_dict in websites:
                key, val = get_web_stats(url=web_dict['website'], regexp=web_dict['regexp'])
                send_stats(key, val)
            producer.flush()

        print(f"sleeping for 5 mins")
        sleep(5*60)


monitor()