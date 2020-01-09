Name: libmlx4
Version: 1.0.6
Release: 7%{?dist}
Summary: Mellanox ConnectX InfiniBand HCA Userspace Driver
Provides: libibverbs-driver.%{_arch}
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: https://www.openfabrics.org/
Source: https://www.openfabrics.org/downloads/mlx4/%{name}-%{version}.tar.gz
Patch0: 0001-Add-ibv_query_port-caching-support.patch
Patch1: 0002-Add-RoCE-IP-based-addressing-support-for-UD-QPs.patch
Patch2: libmlx4-1.0.6-compiler-warnings.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Provides: libmlx4-devel = %{version}-%{release}
BuildRequires: libibverbs-devel >= 1.1.8-2.el6
BuildRequires: valgrind-devel
ExcludeArch: s390 s390x
Requires: rdma >= 6.7_3.15-1.el6
Obsoletes: libmlx4-rocee < 1.0.6

%description
libmlx4 provides a device-specific userspace driver for Mellanox
ConnectX HCAs for use with the libibverbs library.

%package static
Summary: Static version of the libmlx4 driver
Group: System Environment/Libraries
Provides: %{name}-devel-static = %{version}-%{release}
Obsoletes: %{name}-devel-static <= 1.0.1-1
Obsoletes: libmlx4-rocee-static < 1.0.6
Requires: %{name} = %{version}-%{release}

%description static
Static version of libmlx4 that may be linked directly to an
application, which may be useful for debugging.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%build
%configure --with-valgrind
make CFLAGS="$CFLAGS -fno-strict-aliasing" %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
# Remove unpackaged files
rm -f %{buildroot}%{_libdir}/libmlx4.{la,so}

%files
%defattr(-,root,root,-)
%{_libdir}/libmlx4-rdmav2.so
%{_sysconfdir}/libibverbs.d/mlx4.driver
%doc AUTHORS COPYING README

%files static
%defattr(-,root,root,-)
%{_libdir}/libmlx4.a

%changelog
* Wed Mar 11 2015 Doug Ledford <dledford@redhat.com> - 1.0.6-7
- Add compiler warnings patch
- Rebuild against latest libibverbs and valgrind-devel
- Move module init code to rdma package and require rdma package
- Resolves: bz1142161, bz1163527

* Wed Jul 30 2014 Doug Ledford <dledford@redhat.com> - 1.0.6-6
- Fix obsoletes tag for sub packages
- Related: bz1053500

* Thu Jul 24 2014 Doug Ledford <dledford@redhat.com> - 1.0.6-5
- Add IP based RoCE GID support
- Resolves: bz1053500

* Wed Jun 18 2014 Doug Ledford <dledford@redhat.com> - 1.0.6-4
- Another minor fix for the dracut modules
- Related: bz1059094

* Wed Jun 18 2014 Doug Ledford <dledford@redhat.com> - 1.0.6-3
- Actually use the right %source macro when installing the new
  mlx4.conf file this time
- Related: bz1059094

* Wed Jun 18 2014 Doug Ledford <dledford@redhat.com> - 1.0.6-2
- Add the modprobe.d/mlx4.conf for user set module options that we
  don't replace on upgrade
- Rename the dracut module to just mlx4 instead of -libmlx4 (dracut
  takes a dash between the number and the name literally)
- Add obsoletes tag to make us replace libmlx4-rocee
- Related: bz1059094

* Mon Jun 16 2014 Doug Ledford <dledford@redhat.com> - 1.0.6-1.el6
- Update to latest upstream release
- Resolves: bz1059094

* Wed Aug 14 2013 Michal Schmidt <mschmidt@redhat.com> 1.0.5-4.el6.1
- Fix dracut module for compatibility with RHEL6 version of dracut.
- Resolves: bz789121

* Mon Aug 12 2013 Michal Schmidt <mschmidt@redhat.com> - 1.0.5-4
- Add dracut module
- Fix URL

* Thu Aug 01 2013 Doug Ledford <dledford@redhat.com> - 1.0.5-3
- Reduce the dependencies of the setup script even further, it no longer
  needs grep

* Fri Jul 19 2013 Doug Ledford <dledford@redhat.com> - 1.0.5-2
- The setup script needs to have execute permissions

* Wed Jul 17 2013 Doug Ledford <dledford@redhat.com> - 1.0.5-1
- Update to latest upstream
- Drop awk based setup for a bash based setup, making including
  the setup code on an initramfs easier
- Modernize spec file
- Related: bz950915

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
