Name: libmlx4
Version: 1.0.4
Release: 1%{?dist}
Summary: Mellanox ConnectX InfiniBand HCA Userspace Driver
Provides: libibverbs-driver.%{_arch}
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://openfabrics.org/
Source: http://openfabrics.org/downloads/mlx4/%{name}-%{version}.tar.gz
Source1: libmlx4-modprobe.conf
Source2: libmlx4-mlx4.conf
Source3: libmlx4-setup-mlx4.awk
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Provides: libmlx4-devel = %{version}-%{release}
BuildRequires: libibverbs-devel > 1.1.4
BuildRequires: valgrind-devel
ExcludeArch: s390 s390x

%description
libmlx4 provides a device-specific userspace driver for Mellanox
ConnectX HCAs for use with the libibverbs library.

%package static
Summary: Static version of the libmlx4 driver
Group: System Environment/Libraries
Provides: %{name}-devel-static = %{version}-%{release}
Obsoletes: %{name}-devel-static <= 1.0.1-1
Requires: %{name} = %{version}-%{release}

%description static
Static version of libmlx4 that may be linked directly to an
application, which may be useful for debugging.

%prep
%setup -q

%build
%configure --with-valgrind
make CFLAGS="$CFLAGS -fno-strict-aliasing" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} install
install -D -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_sysconfdir}/modprobe.d/libmlx4.conf
install -D -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_sysconfdir}/rdma/mlx4.conf
install -D -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/rdma/setup-mlx4.awk
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la $RPM_BUILD_ROOT%{_libdir}/libmlx4.so

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libmlx4-rdmav2.so
%{_sysconfdir}/libibverbs.d/mlx4.driver
%{_sysconfdir}/modprobe.d/libmlx4.conf
%config(noreplace) %{_sysconfdir}/rdma/mlx4.conf
%{_sysconfdir}/rdma/setup-mlx4.awk
%doc AUTHORS COPYING README

%files static
%defattr(-,root,root,-)
%{_libdir}/libmlx4.a

%changelog
* Sun Oct 14 2012 Doug Ledford <dledford@redhat.com> - 1.0.4-1
- Update to latest upstream version
- Related: bz756396

* Tue Mar 20 2012 Doug Ledford <dledford@redhat.com> - 1.0.2-5
- Fix an issue in the modprobe file that could render a machine unbootable
- Related: bz805129

* Tue Jan 31 2012 Doug Ledford <dledford@redhat.com> - 1.0.2-4
- Update to latest git head by adding patches not yet rolled into a release
- Related: bz756399

* Wed Aug 03 2011 Doug Ledford <dledford@redhat.com> - 1.0.2-3
- Fix fix to modprobe file
- Related: bz725016

* Mon Jul 25 2011 Doug Ledford <dledford@redhat.com> - 1.0.2-2
- Add missing arch macro to libibverbs-driver provide
- Related: bz725016

* Fri Jul 22 2011 Doug Ledford <dledford@redhat.com> - 1.0.2-1
- Update to latest upstream release (1.0.1 -> 1.0.2)
- Remove 5 patches rolled into upstream release
- Drop ifnarch ia64 use around valgrind as we don't build on ia64 any more
- Fix broken libmlx4-modprobe.conf
- Related: bz725016

* Wed Aug 11 2010 Doug Ledford <dledford@redhat.com> - 1.0.1-7
- Add missing PCI device IDs
- Resolves: bz616434

* Wed Jun 16 2010 Doug Ledford <dledford@redhat.com> - 1.0.1-6
- Internal build

* Mon Jan 25 2010 Doug Ledford <dledford@redhat.com> - 1.0.1-5
- Update upstream URLs
- Related: bz543948

* Mon Jan 11 2010 Doug Ledford <dledford@redhat.com> - 1.0.1-4
- Don't try to build on s390(x) as the hardware doesn't exist there

* Sat Dec 05 2009 Doug Ledford <dledford@redhat.com> - 1.0.1-3
- Tweak the provides and obsoletes a little bit to make sure we only pull in
  the -static package to replace past -devel-static packages, and not past
  -devel packages.

* Tue Dec 01 2009 Doug Ledford <dledford@redhat.com> - 1.0.1-2
- Merge various bits from Red Hat package into Fedora package

* Tue Dec 01 2009 Doug Ledford <dledford@redhat.com> - 1.0.1-1
- Update to latest upstream release
- Add pseudo provides of libibverbs-driver
- Update buildrequires for libibverbs API change

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 27 2008 Roland Dreier <rdreier@cisco.com> - 1.0-2
- Spec file cleanups, based on Fedora review: don't mark
  libmlx4.driver as a config file, since it is not user modifiable,
  and change the name of the -devel-static package to plain -devel,
  since it would be empty without the static library.

* Sun Dec  9 2007 Roland Dreier <rdreier@cisco.com> - 1.0-1
- New upstream release

* Fri Apr  6 2007 Roland Dreier <rdreier@cisco.com> - 1.0-0.1.rc1
- Initial Fedora spec file
