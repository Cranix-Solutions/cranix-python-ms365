#!/usr/bin/python3
# Copyright (c) 2026 Peter Varkoly <pvarkoly@cephalix.eu> All rights reserved.

import cranix_ms365

import sys


user = {}

# Read data from standard input
for line in sys.stdin:
    p = line.rstrip().split(": ", 1)
    if len(p) == 2:
        user[p[0]] = p[1]

# Check if all needed parameters are given
for required in ('role', 'uid'):
    if required not in user:
        print("Missing parameter " + required)
        sys.exit(1)

# Check if the user has to be synchronized
if user['role'] not in cranix_ms365.config.get('ROLES_TO_SYNCHRONIZE', '').split(","):
    sys.exit(0)

# Read the msid
ms365_id = cranix_ms365.get_user_msid(user['id'])
if ms365_id == "":
    print("No MS-ID found")
    sys.exit(1)

if not cranix_ms365.delete_ms_user(ms365_id):
    sys.exit(1)