Name: libmlx4
Version: 1.0.5
Release: 7%{?dist}
Summary: Mellanox ConnectX InfiniBand HCA Userspace Driver
Provides: libibverbs-driver.%{_arch}
Group: System Environment/Libraries
License: GPLv2 or BSD
Url: http://www.openfabrics.org/
Source: http://www.openfabrics.org/downloads/mlx4/%{name}-%{version}.tar.gz
Source1: libmlx4-modprobe.conf
Source2: libmlx4-mlx4.conf
Source3: libmlx4-setup.sh
Source4: libmlx4-dracut-module-setup.sh
Source5: libmlx4-modprobe-2.conf
Patch1: 0001-Infra-structure-changes-to-support-verbs-extensions.patch
Patch2: 0002-Add-support-for-XRC-QPs.patch
Patch3: 0003-Add-RoCE-IP-based-addressing-support-for-UD-QPs.patch
Patch4: 0004-Add-ibv_query_port_ex-support.patch
Patch5: 0005-Add-receive-flow-steering-support.patch
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: libibverbs-devel >= 1.1.7-5
%ifnarch ia64 %{sparc} %{arm}
BuildRequires: valgrind-devel
%endif
ExcludeArch: s390 s390x
Requires: dracut
%global dracutlibdir %{_prefix}/lib/dracut

%description
libmlx4 provides a device-specific userspace driver for Mellanox
ConnectX HCAs for use with the libibverbs library.

%package static
Summary: Static version of the libmlx4 driver
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description static
Static version of libmlx4 that may be linked directly to an
application, which may be useful for debugging.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%ifnarch ia64 %{sparc} %{arm}
%configure --with-valgrind
%else
%configure
%endif
make CFLAGS="$CFLAGS -fno-strict-aliasing" %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/modprobe.d/libmlx4.conf
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rdma/mlx4.conf
install -D -m 755 %{SOURCE3} %{buildroot}%{_libexecdir}/setup-mlx4.sh
install -D -m 755 %{SOURCE4} %{buildroot}%{dracutlibdir}/modules.d/04mlx4/module-setup.sh
install -D -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/modprobe.d/mlx4.conf
# Remove unpackaged files
rm -f %{buildroot}%{_libdir}/libmlx4.{la,so}

%files
%defattr(-,root,root,-)
%{_libdir}/libmlx4-rdmav2.so
%{_sysconfdir}/libibverbs.d/mlx4.driver
%{_sysconfdir}/modprobe.d/libmlx4.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/mlx4.conf
%config(noreplace) %{_sysconfdir}/rdma/mlx4.conf
%{_libexecdir}/setup-mlx4.sh
%dir %{dracutlibdir}/modules.d/04mlx4
%{dracutlibdir}/modules.d/04mlx4/module-setup.sh
%doc AUTHORS COPYING README

%files static
%defattr(-,root,root,-)
%{_libdir}/libmlx4.a

%changelog
* Fri Feb 28 2014 Doug Ledford <dledford@redhat.com> - 1.0.5-7
- Fix dracut module support to work with rdma dracut module
- Add support for IP based RoCE addressing and UD QPs
- Add flow steering support
- Related: bz1064316, bz1062284, bz1058538

* Thu Jan 23 2014 Doug Ledford <dledford@redhat.com> - 1.0.5-6
- Add support for XRC extension
- Related: bz1056145

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.5-5
- Mass rebuild 2013-12-27

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

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Doug Ledford <dledford@redhat.com> - 1.0.4-3
- Fix Url and Source tags for real this time

* Mon Nov 26 2012 Doug Ledford <dledford@redhat.com> - 1.0.4-2
- Fix Url and Source tags
- Drop old Provides/Obsoletes we used to change package names
- Pick up a bug fix to modprobe.d/libmlx4.conf

* Sun Oct 21 2012 Jon Stanley <jonstanley@gmail.com> - 1.0.4-1
- Update to latest upstream
- Drop upstreamed patches

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 03 2012 Doug Ledford <dledford@redhat.com> - 1.0.2-3
- Actually bump the release number this time

* Tue Jan 03 2012 Doug Ledford <dledford@redhat.com> - 1.0.2-2
- Update with changesets in current git head so we can get IBoE
  support

* Wed Jul 20 2011 Doug Ledford <dledford@redhat.com> - 1.0.2-1
- Update to latest version
- Fix modprobe.conf to look in /etc/rdma instead of /etc/ofed

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Dennis Gilmore <dennis@ausil.us> - 1.0.1-7
- arm arches dont have valgrind disable its support on them

* Wed Mar 24 2010 Dennis Gilmore <dennis@ausil.us> - 1.0.1-6
- sparc arches dont have valgrind disable its support on them

* Thu Feb 11 2010 Doug Ledford <dledford@redhat.com> - 1.0.1-5
- Minor cleanups to Obsoletes to resolve some repo issues

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
