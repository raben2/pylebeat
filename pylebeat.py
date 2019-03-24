#!/usr/bin/env python3
import json
import yaml
import urllib
import redis
import boto3
import random
import gzip
import base64

sec_random = random.SystemRandom()
# read config
cfg = open('pylebeat.yml', 'r')
config = yaml.load(cfg)
# get extra fields
extra_fields = config['pylebeat']['aws']['fields'].items()
# connect to redis
redis_hosts = config['output']['redis']['hosts']
redis_port = config['output']['redis']['port']
redis_pass = config['output']['redis']['password']
redis_key = config['output']['redis']['key']
# Select random host for connection
redis_host = sec_random.choice(redis_hosts)

try:
    res = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_pass)
except ConnectionError as e:
    print(e)

def merge_dicts(a, b, path=None):
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dicts(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception(
                        'Conflict while merging metadatas and the log entry at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a
 
def lamda_cloudwatch_log_handler(event, context):

    cw_data = event['awslogs']['data']
    structured_logs = []
    uncompressed_payload = gzip.decompress(base64.b64decode(cw_data))
    payload = json.loads(uncompressed_payload)

    log_events = payload['logEvents']
    for log_event in log_events:
            
            structured_line = merge_dicts(log_event, {
            "aws": {
                "awslogs": {
                    "logGroup": payload["logGroup"],
                    "logStream": payload["logStream"],
                    "owner": payload["owner"],
                }
            }
        })

            
            structured_line.update(extra_fields)
            structured_logs.append(structured_line)
    try:
        res.set(redis_key, json.dumps(structured_logs[0]))
    except:
        print("error")