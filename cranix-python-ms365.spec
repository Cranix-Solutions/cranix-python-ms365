#
# spec file for package cranix-python-ms365
#
# Copyright (c) 2026 Peter Varkoly, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for that file, and modifications and additions to the
# file, is the same license as for the pristine package itself.
#

Name:           cranix-python-ms365
Version:        1.0.0
Release:        0
Summary:        Microsoft 365 synchronization helpers for CRANIX
License:        CC-BY-NC-ND-4.0
URL:            https://github.com/Cranix-Solutions/cranix-python-ms365
Source:         cranix-python-ms365-%{version}.tar.xz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-pip
BuildRequires:  python3-build
BuildArch:      noarch

%description
Microsoft 365 synchronization helpers for CRANIX.

This package provides the ``cranix_ms365`` Python module.

%package -n cranix-ms365
Summary:        CRANIX plugin to synchronize users and groups with MS365
Requires:       cranix-python-ms365 = %{version}-%{release}
Requires:       python3-cranix
Requires:       python3-requests
Requires:       python3-bashconfigparser
Requires:       bash
Requires:       coreutils

%description -n cranix-ms365
CRANIX plugin to synchronize users and groups with MS365.

This package provides the CRANIX user and group plugins, the administration
tools, the configuration file and the runtime directories used by the
``cranix_ms365`` module.

%prep
%autosetup -p1 -n cranix-python-ms365-%{version}

%build
python3 -m build

%install
mkdir -p %{buildroot}%{python3_sitelib}
python3 -m pip install --no-deps --root=%{buildroot} --prefix=/usr dist/*.whl

mkdir -p %{buildroot}/usr/share/cranix/tools/ms365
mkdir -p %{buildroot}/usr/share/cranix/plugins/{add_group,add_user,change_member,delete_user,modify_user}
mkdir -p %{buildroot}/opt/cranix-ms365
mkdir -p %{buildroot}/var/adm/cranix/ms365/{failed,userids,groupids}
install -m 755 tools/* %{buildroot}/usr/share/cranix/tools/ms365/
install -m 755 plugins/add_group/200-ms365.py     %{buildroot}/usr/share/cranix/plugins/add_group/
install -m 755 plugins/add_user/200-ms365.py      %{buildroot}/usr/share/cranix/plugins/add_user/
install -m 755 plugins/change_member/200-ms365.py %{buildroot}/usr/share/cranix/plugins/change_member/
install -m 755 plugins/delete_user/200-ms365.py   %{buildroot}/usr/share/cranix/plugins/delete_user/
install -m 755 plugins/modify_user/200-ms365.py   %{buildroot}/usr/share/cranix/plugins/modify_user/
install -m 644 opt/config %{buildroot}/opt/cranix-ms365/config

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/cranix_ms365
%{python3_sitelib}/cranix_ms365-%{version}.dist-info

%files -n cranix-ms365
%doc README.md
%dir /opt/cranix-ms365/
%config(noreplace) /opt/cranix-ms365/config
/usr/share/cranix/plugins/*/*
/usr/share/cranix/tools/ms365
%dir /var/adm/cranix/ms365
%dir /var/adm/cranix/ms365/failed
%dir /var/adm/cranix/ms365/userids
%dir /var/adm/cranix/ms365/groupids

%changelog