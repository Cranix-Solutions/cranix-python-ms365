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
for required in ('role', 'givenname', 'surname', 'password'):
    if required not in user:
        print("Missing parameter " + required)
        sys.exit(1)

# Check if the user has to be synchronized
if user['role'] not in cranix_ms365.config.get('ROLES_TO_SYNCHRONIZE', '').split(","):
    sys.exit(0)

# Convert CRANIX user to a MS365 user
msuser = cranix_ms365.cranix_user_to_ms(user)

cranix_id = cranix_ms365.cranix_user_id(user['uid'])

# Create the user in MS365
ms365_id = cranix_ms365.create_ms_user(msuser)
if not ms365_id:
    sys.exit(1)

cranix_ms365.set_user_msid(cranix_id, ms365_id)

msgroup_id = cranix_ms365.get_group_msid_byname(user['role'].upper())

if msgroup_id != "":
    # Add user to the role specific group
    cranix_ms365.add_user_to_group(msgroup_id, ms365_id, cranix_id)
else:
    # Add license to the user
    license = 'LICENCE_' + user['role'].upper()
    if cranix_ms365.debug:
        print('selected license:' + license)

    if license in cranix_ms365.config:
        users_licenses = cranix_ms365.config[license].split(',')
    else:
        users_licenses = cranix_ms365.config.get('LICENCE_STUDENTS', '').split(',')

    add_licenses = [{"disabledPlans": [], "skuId": lic}
                    for lic in users_licenses if lic]
    if add_licenses:
        cranix_ms365.assign_license(ms365_id, add_licenses)