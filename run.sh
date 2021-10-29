#!/bin/bash

echo Hello-docker

exec python src/consumer.py &
exec python monitor.py
