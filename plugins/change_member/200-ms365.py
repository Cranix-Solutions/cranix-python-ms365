#!/usr/bin/python3
# Copyright (c) 2026 Peter Varkoly <pvarkoly@cephalix.eu> All rights reserved.

import cranix_ms365

import sys


action = {}

# Read data from standard input
for line in sys.stdin:
    p = line.rstrip().split(": ", 1)
    if len(p) == 2:
        action[p[0]] = p[1]

# Check if all needed parameters are given
for required in ('changetype', 'users', 'group'):
    if required not in action:
        print("Missing parameter " + required)
        sys.exit(1)

cranix_ids = action['userIds'].split(",")

group_msid = cranix_ms365.get_group_msid(action['id'])
if group_msid == "":
    print("Group not available in MS365!")
    sys.exit(0)
msteamid = cranix_ms365.get_msteamid(action['id'])

for cranix_id in cranix_ids:
    user_msid = cranix_ms365.get_user_msid(cranix_id)
    if action['changetype'] == 'addmembers':
        if cranix_ms365.cranix_user_role_by_id(cranix_id) == "teachers":
            cranix_ms365.add_owner_to_team(msteamid, user_msid, cranix_id)
        cranix_ms365.add_user_to_group(group_msid, user_msid, cranix_id)
        cranix_ms365.add_user_to_team(msteamid, user_msid, cranix_id)
    else:
        cranix_ms365.remove_user_from_group(group_msid, user_msid, cranix_id)
        cranix_ms365.remove_user_from_team(msteamid, user_msid, cranix_id)