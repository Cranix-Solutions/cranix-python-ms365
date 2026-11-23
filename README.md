# cranix-python-ms365

Microsoft 365 synchronization helpers for
[CRANIX](https://github.com/Cranix-Solutions).

This package provides the `cranix_ms365` Python module. It was split out of
[cranix-python](https://github.com/Cranix-Solutions/cranix-python) so that the
Microsoft 365 synchronization code can be released independently.

CRANIX side calls are done through the native REST client from the `cranix`
package, Microsoft Graph calls through `requests`.

## Build status
[![build result](https://build.opensuse.org/projects/home:pvarkoly:CRANIX/packages/cranix-python-ms365/badge.svg?type=default)](https://build.opensuse.org/package/show/home:pvarkoly:CRANIX/cranix-python-ms365)

## Installation

The package is built as the RPM `python313-cranix-ms365` and depends on the
`cranix` package (RPM `python313-cranix`):

```
make install DESTDIR=/ PYTHONSITEARCH=/usr/lib/python3.13/site-packages/
```

For local development:

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

The module is configured through the bash style configuration file
`/opt/cranix-ms365/config` (installed by the `cranix-ms365` plugin package) and
stores its state below `/var/adm/cranix/ms365`.

The `cranix-ms365` plugin package uses this module from its user and group
plugins and its synchronization tools.

## Tests

```
python3 -m pytest -q
```

## License

See [LICENSE](LICENSE).
