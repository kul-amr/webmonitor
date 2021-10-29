"""
producer module - this creates a kafka producer , tries to connect to a
given website and collects the connection stats like response code, response time,
checks if the given regexp exists and sends these details to kafka consumer.

"""
import requests
import re
import json
import datetime
from kafka import KafkaProducer
from .settings import *

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVICE_URI,
    client_id="demo-producer-1",
    key_serializer=lambda k: json.dumps(k).encode('utf-8'),
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    security_protocol="SSL",
    ssl_cafile="./keys/ca.pem",
    ssl_certfile="./keys/service.cert",
    ssl_keyfile="./keys/service.key",
)


def get_web_stats(url, timeout=3, regexp=None):
    try:
        key = {"website": url}
        val = {"status_code": 0,
               "response_time": 0,
               "regexp": regexp,
               "regexp_exists": False
               }

        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        response_time = response.elapsed.total_seconds()
        status_code = response.status_code
        regexp_exists = bool(re.search(regexp, response.text)) if regexp else False

        val = val | {"status_code": status_code,
                     "response_time": response_time,
                     "regexp_exists": regexp_exists,
                     "create_datetime": (datetime.datetime.now(datetime.timezone.utc)).strftime('%Y-%m-%d %H:%M:%S%z')}

    except requests.exceptions.HTTPError as err:
        print(f"http error occurred : {err}")
        val = val | {"status_code": err.response.status_code,
                     "create_datetime": (datetime.datetime.now(datetime.timezone.utc)).strftime('%Y-%m-%d %H:%M:%S%z')}
    except requests.exceptions.ConnectionError as err:
        print(f"connection error occurred : {err}")
        val = val | {"create_datetime": (datetime.datetime.now(datetime.timezone.utc)).strftime('%Y-%m-%d %H:%M:%S%z')}
    except requests.exceptions.Timeout as err:
        print(f"timeout error occurred : {err}")
        val = val | {"status_code": err.response.status_code,
                     "create_datetime": (datetime.datetime.now(datetime.timezone.utc)).strftime('%Y-%m-%d %H:%M:%S%z')}
    except Exception as err:
        print(f"error as : {err}")

    return key, val


def send_stats(key, val):
    producer.send(KAFKA_TOPIC, key=key, value=val)
