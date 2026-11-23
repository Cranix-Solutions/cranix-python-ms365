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

# Some checks
if 'uid' not in user:
    print("Missing parameter uid")
    sys.exit(1)

# Get the role of the user
role = user.get('role', '') or cranix_ms365.cranix_user_role(user['uid'])

# Check if the user has to be synchronized
if role not in cranix_ms365.config.get('ROLES_TO_SYNCHRONIZE', '').split(","):
    sys.exit(0)

# Convert CRANIX user to a MS365 user
msuser = {}
if 'givenname' in user and 'surname' in user:
    msuser['givenName'] = user['givenname']
    msuser['surName'] = user['surname']
    msuser['displayName'] = '{0} {1}'.format(user['givenname'], user['surname'])
if 'password' in user:
    msuser['passwordProfile'] = {}
    msuser['passwordProfile']['password'] = user['password']
    if user.get('mpassword') == 'yes':
        msuser['passwordProfile']['forceChangePasswordNextSignIn'] = True
        msuser['passwordProfile']['forceChangePasswordNextSignInWithMfa'] = True
    else:
        msuser['passwordProfile']['forceChangePasswordNextSignIn'] = False
        msuser['passwordProfile']['forceChangePasswordNextSignInWithMfa'] = False

# Get the ms365_id
ms365_id = cranix_ms365.get_user_msid(cranix_ms365.cranix_user_id(user['uid']))
if ms365_id == "":
    sys.exit(1)

cranix_ms365.update_ms_user(ms365_id, msuser)