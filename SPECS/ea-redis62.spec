%global ns_dir /opt/cpanel

# OBS builds the 32-bit targets as arch 'i586', and more typical
# 32-bit architecture is 'i386', but 32-bit archive is named 'x86'.
# 64-bit archive is 'x86-64', rather than 'x86_64'.
%if "%{_arch}" == "i586" || "%{_arch}" == "i386"
%global archive_arch x86
%else
%if "%{_arch}" == "x86_64"
%global archive_arch x86-64
%else
%global archive_arch %{_arch}
%endif
%endif

%if 0%{?centos} >= 7 || 0%{?fedora} >= 17 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

Name:    ea-redis62
Vendor:  cPanel, Inc.
Summary: Redis
Version: 6.2.14
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: BSD-3-Clause
Group:   System Environment/Daemons
URL: https://github.com/redis/redis

Source0: https://github.com/redis/redis/archive/refs/tags/%{version}.tar.gz
Source1: pkg.prerm
Source2: redis.conf
Source3: podman_entrypoint.sh
Source4: ea-podman-local-dir-setup
Source5: README.md
Source6: pkg.postinst

# if I do not have autoreq=0, rpm build will recognize that the ea_
# scripts need perl and some Cpanel pm's to be on the disk.
# unfortunately they cannot be satisfied via the requires: tags.
Autoreq: 0

Requires: ea-podman

%description
Redis is an open source key-value store that functions as a data structure server.

%prep

# nothing to do here

%build
# empty build section

%install

mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-redis62
echo -n "%{version}-%{release_prefix}" > $RPM_BUILD_ROOT/opt/cpanel/ea-redis62/pkg-version
cp %{SOURCE2} $RPM_BUILD_ROOT/opt/cpanel/ea-redis62/
cp %{SOURCE3} $RPM_BUILD_ROOT/opt/cpanel/ea-redis62/
cp %{SOURCE4} $RPM_BUILD_ROOT/opt/cpanel/ea-redis62/
cp %{SOURCE5} $RPM_BUILD_ROOT/opt/cpanel/ea-redis62/README.md

cat << EOF > $RPM_BUILD_ROOT/opt/cpanel/ea-redis62/ea-podman.json
{
    "ports" : [],
    "image" : "docker.io/library/redis:%{version}",
    "startup" : {
        "-v"     : [
            ":/socket_dir",
            "redis.conf:/usr/local/etc/redis/redis.conf",
            "podman_entrypoint.sh:/usr/local/bin/docker-entrypoint.sh"
       ]
    }
}
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%preun

%include %{SOURCE1}

%files
%defattr(0644,root,root,-)
/opt/cpanel/ea-redis62
%attr(0755,root,root) /opt/cpanel/ea-redis62/ea-podman-local-dir-setup
%attr(0755,root,root) /opt/cpanel/ea-redis62/podman_entrypoint.sh

%changelog
* Thu Jan 18 2024 Cory McIntire <cory@cpanel.net> - 6.2.14-1
- EA-11922: Update ea-redis62 from v6.2.8 to v6.2.14
- CVE-2023-45145 ( Bypass permissions on socket on startups )
- CVE-2022-24834 ( RCE )
- CVE-2023-28856 ( Users can crash redis with invalid data )
- CVE-2023-25155 ( Integer overflow can cause redis to terminate )
- CVE-2022-36021 ( DoS - can cause redis to hang and consume 100% CPU time )
- CVE-2022-35977, CVE-2023-22458 ( integer overflow issues / oom panic fixes )

* Mon May 08 2023 Brian Mendoza <brian.mendoza@cpanel.net> - 6.2.8-2
- ZC-10936: Clean up Makefile and remove debug-package-nil

* Thu Dec 15 2022 Cory McIntire <cory@cpanel.net> - 6.2.8-1
- EA-11106: Update ea-redis62 from v6.2.7 to v6.2.8

* Thu May 05 2022 Cory McIntire <cory@cpanel.net> - 6.2.7-1
- EA-10686: Update ea-redis62 from v6.2.6 to v6.2.7

* Mon Apr 25 2022 Julian Brown <julian.brown@cpanel.net> - 6.2.6-1
- ZC-9895: Add container based redis

