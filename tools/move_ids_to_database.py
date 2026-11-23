#!/usr/bin/python3
# Copyright (c) 2026 Peter Varkoly <pvarkoly@cephalix.eu> All rights reserved.

from cranix import api
import cranix_ms365

import os


client = api.client()

for name in os.listdir(cranix_ms365.USERIDS_DIR):
    user_id = client.user_id_by_uid(name)
    if user_id == "":
        continue
    try:
        with open(os.path.join(cranix_ms365.USERIDS_DIR, name)) as handle:
            ms365_id = handle.read().strip()
        print("Proceeding", name, user_id, ms365_id)
        print(client.set_object_config("user", user_id, "ms365id", ms365_id))
    except OSError:
        print("Can not open {0}".format(name))

for name in os.listdir(cranix_ms365.GROUPIDS_DIR):
    if name.endswith("_team"):
        continue
    group_id = client.group_id_by_name(name)
    if group_id == "":
        continue
    try:
        with open(os.path.join(cranix_ms365.GROUPIDS_DIR, name)) as handle:
            ms365_id = handle.read().strip()
        print("Proceeding", name, group_id, ms365_id)
        print(client.set_object_config("group", group_id, "ms365id", ms365_id))
    except OSError:
        print("Can not open {0}".format(name))

    try:
        with open(os.path.join(cranix_ms365.GROUPIDS_DIR, name + "_team")) as handle:
            ms365_id = handle.read().strip()
        print("Proceeding", name, group_id, ms365_id)
        print(client.set_object_config("group", group_id, "msteamid", ms365_id))
    except OSError:
        print("Can not open {0}_team".format(name))