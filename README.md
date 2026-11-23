# cranix-python-ms365

Microsoft 365 synchronization helpers for
[CRANIX](https://github.com/Cranix-Solutions).

This repository provides the `cranix_ms365` Python module together with the
Microsoft 365 add-on for CRANIX (user/group plugins, administration tools and
configuration). It was split out of
[cranix-python](https://github.com/Cranix-Solutions/cranix-python) so that the
Microsoft 365 synchronization code can be released independently.

CRANIX side calls are done through the native REST client from the `cranix`
package, Microsoft Graph calls through `requests`.

## Build status
[![build result](https://build.opensuse.org/projects/home:pvarkoly:CRANIX/packages/cranix-python-ms365/badge.svg?type=default)](https://build.opensuse.org/package/show/home:pvarkoly:CRANIX/cranix-python-ms365)

## Packages

The spec builds two RPMs:

* `cranix-python-ms365` — the `cranix_ms365` Python module (also available as a
  normal Python distribution via `pip`).
* `cranix-ms365` — the CRANIX add-on. It requires `cranix-python-ms365` and
  installs:
  * `/usr/share/cranix/plugins/{add_group,add_user,change_member,delete_user,modify_user}/200-ms365.py`
  * `/usr/share/cranix/tools/ms365/`
  * `/opt/cranix-ms365/config` (marked `%config(noreplace)`)
  * `/var/adm/cranix/ms365/{failed,userids,groupids}`

## Installation

For the RPM based installation:

```
make install DESTDIR=/ PYTHONSITEARCH=/usr/lib/python3.13/site-packages/
```

For local development of the Python module only:

```
pip install -e .
```

## Requirements

* Python >= 3.11
* `cranix`
* `requests`
* `bashconfigparser`

## Usage

```python
import cranix_ms365

cranix_ms365.read_token()
ms_id = cranix_ms365.get_user_msid(user_id)
```

The module reads its bash style configuration from `/opt/cranix-ms365/config`
and stores its state below `/var/adm/cranix/ms365`.

## CRANIX integration

The `cranix-ms365` add-on is invoked by the CRANIX plugin framework
(`/usr/share/cranix/plugins/plugin_handler.sh`), which pipes the object data
into the `200-ms365.py` scripts. The administration tools live in
`/usr/share/cranix/tools/ms365/`:

* `sync_all_user_to_ms.py` — create all configured CRANIX users in Microsoft 365
* `read_all_user_from_ms.py` — list Microsoft 365 users and optionally store the ids
* `move_ids_to_database.py` — migrate ids from the old files into the CRANIX database
* `check_office365_password.sh` — check a password against Office 365 policies

## Tests

```
python3 -m pytest -q
```

## License

See [LICENSE](LICENSE).