#!/usr/bin/env bash
NB_CONCURRENT_USERS=$1

locust --headless --locustfile ./benchmark_codalab.py \
    --users $NB_CONCURRENT_USERS --spawn-rate 5 --run-time 60s --reset-stats --loglevel ERROR \
    --stop-timeout 999
