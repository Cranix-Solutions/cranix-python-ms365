# -*- coding: utf-8 -*-

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLUGIN_GROUPS = [
    "add_group",
    "add_user",
    "change_member",
    "delete_user",
    "modify_user",
]

TOOLS = [
    "check_office365_password.sh",
    "move_ids_to_database.py",
    "read_all_user_from_ms.py",
    "sync_all_user_to_ms.py",
]

PYTHON_TOOLS = [
    "move_ids_to_database.py",
    "read_all_user_from_ms.py",
    "sync_all_user_to_ms.py",
]


def _path(*parts):
    return os.path.join(ROOT, *parts)


def _assert_compiles(path):
    with open(path, encoding="utf-8") as handle:
        compile(handle.read(), path, "exec")


def test_plugin_files_present():
    for group in PLUGIN_GROUPS:
        assert os.path.isfile(_path("plugins", group, "200-ms365.py"))


def test_tool_files_present():
    for name in TOOLS:
        assert os.path.isfile(_path("tools", name))


def test_config_file_present():
    assert os.path.isfile(_path("opt", "config"))


def test_plugin_scripts_compile():
    for group in PLUGIN_GROUPS:
        _assert_compiles(_path("plugins", group, "200-ms365.py"))


def test_tool_scripts_compile():
    for name in PYTHON_TOOLS:
        _assert_compiles(_path("tools", name))