%global         package_version 0.9.6-0
%global         package_name redhat-support-lib-python

Name:           %{package_name}
Version:        0.9.6
Release:        0%{?release_suffix}%{?dist}
Summary:        Red Hat Support Software Development Library
Vendor:         Red Hat, Inc.
Group:          Development/Libraries
License:        ASL 2.0
URL:            https://api.access.redhat.com
Source0:        http://people.redhat.com/kroberts/projects/redhat-support-lib/%{package_name}-%{package_version}.tar.gz

BuildRequires: python-setuptools
BuildArch: noarch
%{!?dist:BuildRequires: buildsys-macros}


Requires: python-lxml
Requires: rpm-python
Requires: python-dateutil
%if %{?rhel:0}%{!?rhel:1} || 0%{?rhel} > 5
Requires: ca-certificates
%endif
Requires: m2crypto

%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
BuildRoot: %{_topdir}/BUILDROOT/%{name}-%{version}-%{release}.%{_arch}
%endif

%description
This package contains the Red Hat Support Software Development Library.
Red Hat customers can use the library to easily integrate their help desk
solutions, IT infrastructure, etc. with the services provided by the
Red Hat Customer Portal.

The library provided by this package is an abstraction layer that simplifies
interactions with the Red Hat Customer Portal. Simply create an instance of
the API by providing the necessary authorization credentials, then use the
API object to interact with the Red Hat Customer Portal.

Some of the interactions supported by this API include, but are not limited to,
automatic diagnostic services on log files, knowledge base searching,
support case creation, attach files to support cases, view the status of
support cases, entitlement viewing, etc.

%prep
%setup -q -n %{package_name}-%{package_version}

%build
%configure \
        --docdir="%{_docdir}/%{package_name}-%{version}" \
        --disable-python-syntax-check

make %{?_smp_mflags}

%install
rm -rf "%{buildroot}"
make %{?_smp_mflags} install DESTDIR="%{buildroot}"

%files
%doc AUTHORS README
%{python_sitelib}/redhat_support_lib/

%changelog
* Wed Feb 26 2014 Keith Robertson <kroberts@redhat.com> - 0.9.6-0
- Resolves: bz1036697

* Sun Aug 11 2013 Keith Robertson <kroberts@redhat.com> - 0.9.5-9
- Resolves: bz967498

* Mon Jul 22 2013 Keith Robertson <kroberts@redhat.com> - 0.9.5-4
- Resolves: bz880750

* Tue Jun 11 2013 Keith Robertson <kroberts@redhat.com> - 0.9.5-3
- Resolves: bz869406

* Tue Jun 11 2013 Keith Robertson <kroberts@redhat.com> - 0.9.5-2
- Various updates including;
  - CA certificate fix for EL5
  - Support for case filters
  
* Thu May 23 2013 Nigel Jones <nigjones@redhat.com> - 0.9.4-1
- Downloads:
  - Fixes to download handling to avoid excessive memory use
- Localization/Internationalization:
  - Changes to support non-ASCII character input from character sets used in
    Red Hat GSS supported languages.

* Fri Apr 26 2013 Nigel Jones <nigjones@redhat.com> - 0.9.2-1
- API update to bring in line with current version of Strata.
  Changes include:
   - Update to Recommendations API
   - Pagination of Cases
- Additional fixes for proxy handling, and traceability of exceptions

* Tue Feb 19 2013 Nigel Jones <nigjones@redhat.com> - 0.9.0-2
- Import into Red Hat packaging system

* Fri Aug 17 2012 Keith Robertson <kroberts@redhat.com> - 0.9.0-1
- Initial release
