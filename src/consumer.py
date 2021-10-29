"""
consumer module - creates a kafka consumer listening to a perticular topic and
consumes the messages. The web stats details like response code, response time,
any regexp etc. are extracted from the message and stored in the database.
"""
import psycopg2
import json
from kafka import KafkaConsumer
from settings import *

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    auto_offset_reset="latest",
    bootstrap_servers=KAFKA_SERVICE_URI,
    client_id="demo-consumer-1",
    key_deserializer=lambda k: json.loads(k.decode('utf-8')),
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    security_protocol="SSL",
    ssl_cafile="./keys/ca.pem",
    ssl_certfile="./keys/service.cert",
    ssl_keyfile="./keys/service.key",
)


def store_web_stats():
    print("consumer started")
    conn = psycopg2.connect(POSTGRESQL_URI)

    cursor = conn.cursor()

    for msg in consumer:
        print("in consumer messages : ")
        print(msg)
        website = msg.key['website']
        status_code = msg.value['status_code']
        response_time = msg.value['response_time']
        regexp = msg.value['regexp'] if msg.value['regexp'] else ''
        regexp_exists = msg.value['regexp_exists']
        create_datetime = msg.value['create_datetime']

        query_str = '''INSERT INTO website_stats(website, regexp, status_code, response_time,
                        regexp_exists, create_datetime) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (website, regexp) DO UPDATE
                        SET status_code = %s,
                            response_time = %s,
                            regexp_exists = %s,
                            create_datetime = %s'''

        cursor.execute(query_str, (website, regexp, status_code, response_time,
                                   regexp_exists, create_datetime, status_code,
                                   response_time, regexp_exists, create_datetime))

        conn.commit()

    conn.close()


store_web_stats()
