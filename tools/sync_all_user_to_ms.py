#!/usr/bin/python3
# Copyright (c) 2026 Peter Varkoly <pvarkoly@cephalix.eu> All rights reserved.

from cranix import api
import cranix_ms365

import os


client = api.client()
roles_to_sync = cranix_ms365.config.get('ROLES_TO_SYNCHRONIZE', '').split(",")

for user in client.get("users/all") or []:
    if user['role'] not in roles_to_sync:
        continue
    ms_id = cranix_ms365.get_user_msid(user['id'])
    if ms_id != "":
        print("{0} does already exists in ms365.".format(user['uid']))
        continue
    user['givenname'] = user['givenName']
    user['surname'] = user['surName']
    user['password'] = cranix_ms365.generate_office365_password(
        length=16, require_upper=True, require_lower=True,
        require_digit=True, require_symbol=True, allow_repeats=False)
    msuser = cranix_ms365.cranix_user_to_ms(user)
    cranix_id = user['id']
    ms365_id = cranix_ms365.create_ms_user(msuser)
    if not ms365_id:
        continue
    cranix_ms365.set_user_msid(cranix_id, ms365_id)
    home = client.get("users/byUid/{0}/home".format(user['uid']), text=True)
    home = (home or "").strip()
    if home:
        os.system("mkdir -m 750 -p {0}".format(home))
        os.system("chown {0} {1}".format(user['uid'], home))
        with open("{0}/ms365-password.txt".format(home), 'w') as pwfile:
            pwfile.write(user['password'])
        os.system("chown {0} {1}/ms365-password.txt".format(user['uid'], home))
    msgroup_id = cranix_ms365.get_group_msid_byname(user['role'].upper())
    if msgroup_id != "":
        cranix_ms365.add_user_to_group(msgroup_id, ms365_id, cranix_id)
    print("{0} successfully synced.".format(user['uid']))