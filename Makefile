#
# Copyright (C) 2026 Peter Varkoly <pvarkoly@cephalix.eu> Nürnberg, Germany.  All rights reserved.
#
DESTDIR        ?= /
PYTHONSITEARCH ?= /usr/lib/python3.13/site-packages/
PACKAGE         = cranix_ms365
VERSION         = $(shell cat VERSION)
HERE            = $(shell pwd)

SHARE           = $(DESTDIR)/usr/share/cranix
PLUGINS         = $(SHARE)/plugins
TOOLS           = $(SHARE)/tools/ms365
OPTDIR          = $(DESTDIR)/opt/cranix-ms365
VARDIR          = $(DESTDIR)/var/adm/cranix/ms365
PLUGIN_GROUPS   = add_group add_user change_member delete_user modify_user

.PHONY: all install test sdist wheel dist clean

all: test

install:
	mkdir -p $(DESTDIR)$(PYTHONSITEARCH)
	cp -r cranix_ms365 $(DESTDIR)$(PYTHONSITEARCH)/
	find $(DESTDIR)$(PYTHONSITEARCH)/cranix_ms365 -name '__pycache__' -type d -exec rm -rf {} +
	find $(DESTDIR)$(PYTHONSITEARCH)/cranix_ms365 -name '*.pyc' -delete
	mkdir -p $(TOOLS) $(OPTDIR) $(VARDIR)/{failed,userids,groupids}
	for dir in $(PLUGIN_GROUPS); do \
	    mkdir -p $(PLUGINS)/$$dir; \
	    install -m 755 plugins/$$dir/* $(PLUGINS)/$$dir/; \
	done
	install -m 755 tools/* $(TOOLS)/
	install -m 644 opt/config $(OPTDIR)/config

test:
	python3 -m pytest -q

sdist wheel dist:
	python3 -m build

clean:
	rm -rf build dist *.egg-info .pytest_cache
	find . -name '__pycache__' -type d -exec rm -rf {} +