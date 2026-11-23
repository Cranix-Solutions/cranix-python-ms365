#
# spec file for package python-cranix-ms365
#
# Copyright (c) 2026 Peter Varkoly, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for that file, and modifications and additions to the
# file, is the same license as for the pristine package itself.
#

Name:           python-cranix-ms365
Version:        1.0.0
Release:        0
Summary:        Microsoft 365 synchronization helpers for CRANIX
License:        CC-BY-NC-ND-4.0
URL:            https://github.com/Cranix-Solutions/cranix-python-ms365
Source:         cranix-python-ms365-%{version}.tar.xz
BuildRequires:  python-rpm-macros
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module wheel}
BuildRequires:  fdupes
BuildArch:      noarch
%python_subpackages

%description
Microsoft 365 synchronization helpers for CRANIX.

This package provides the ``cranix_ms365`` Python module. It is used by the
cranix-ms365 plugin package to synchronize CRANIX users and groups with
Microsoft 365.

%prep
%autosetup -p1 -n cranix-python-ms365-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%python_expand %fdupes %{buildroot}%{$python_sitelib}

%files %{python_files}
%license LICENSE
%doc README.md
%{python_sitelib}/cranix_ms365
%{python_sitelib}/cranix_ms365-%{version}.dist-info

%changelog
