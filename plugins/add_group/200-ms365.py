#!/usr/bin/python3

import cranix_ms365

import sys
from datetime import datetime
#import argparse


group = {}
#token = cranix_ms365.read_token()
# Read data from standard input
toDo = ""
border =  datetime(datetime.now().year,8,1)
now = datetime.now()
print(border)
print("Border is before date: " + str(border.date() < now.date()))
prefix=""
if border.date() < now.date():
    border_string=str(border.year)
    border_lenght = len(border_string)
    pr= border_string[border_lenght -2: border_lenght]
    tmp = str(int(pr) + 1)
    prefix = pr + tmp
    print("Prefix on " + str(now) + " is: " + prefix)
else:
    border_string=str(border.year)
    border_lenght = len(border_string)
    pr= border_string[border_lenght -2: border_lenght]
    tmp = str(int(pr) - 1)
    prefix = tmp + pr
    print("Prefix on " + str(now) + " is: " + prefix)

for line in sys.stdin:
    p = line.rstrip().split(": ", 1)
    if len(p) == 2:
        group[p[0]] = p[1]


#Check if all needed parameters are given
if 'name' not in group:
    print("Missing parameter name")
    sys.exit(1)
if 'description' not in group:
    print("Missing parameter description")
    sys.exit(1)
if 'grouptype' not in group:
    print("Missing parameter grouptype")
    sys.exit(1)

if group['grouptype']  not in cranix_ms365.config['GROUPS_TO_SYNCHRONIZE'].split(","):
    sys.exit(0)

ms_name = prefix + "_" + group['name']


cranix_ms365.create_msgroup(ms_name, group)
cranix_ms365.create_msteam(ms_name, group)