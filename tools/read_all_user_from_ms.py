#!/usr/bin/python3
# Copyright (c) 2026 Peter Varkoly <pvarkoly@cephalix.eu> All rights reserved.

import cranix_ms365

import sys


write_db = len(sys.argv) > 1 and sys.argv[1] == '--writeDb'

for user in cranix_ms365.get_all_users():
    uid = user['userPrincipalName'].split('@')[0].lower()
    ms_id = user['id']
    print(uid, ms_id)
    if write_db:
        cranix_ms365.set_user_msid_byuid(uid, ms_id)