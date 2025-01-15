#!/usr/bin/env python3
import json, sys

records = list()

for line in sys.stdin.readlines():
    record = json.loads(line)
    records.append(record)

print(json.dumps(records))
