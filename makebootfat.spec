%define new_ldlinux	0

Summary: Utility for creation bootable FAT disk
Name: makebootfat
Version: 1.4
Release: 10%{?dist}
Group: 	Applications/System
License: GPLv2+
URL: http://advancemame.sourceforge.net/doc-makebootfat.html
Source0: http://dl.sourceforge.net/sourceforge/advancemame/%{name}-%{version}.tar.gz
Source1: makebootfat-README.usbboot

%if %{new_ldlinux}
#  Get syslinux-VERSION.tar.bz2 from
#	ftp://ftp.kernel.org/pub/linux/utils/boot/syslinux/
#  or
#	ftp://ftp.kernel.org/pub/linux/utils/boot/syslinux/Old/
#  Then
#	bunzip2 -cd syslinux-VERSION.tar.bz2 | tar -xvf -
#	cp syslinux-VERSION/ldlinux.bss ldlinux.bss-VERSION
#	cp syslinux-VERSION/ldlinux.sys ldlinux.sys-VERSION
#	rm -rf syslinux-VERSION
#
Source2: ldlinux.bss-3.36
Source3: ldlinux.sys-3.36
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
This utility creates a bootable FAT filesystem and populates it
with files and boot tools.

It was mainly designed to create bootable USB and Fixed disk
for the AdvanceCD project (http://advancemame.sourceforge.net), but
can be successfully used separately for any purposes.


%prep
%setup -q

install -p -m644 %{SOURCE1} README.usbboot


%build

%configure
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/x86
install -p -m644 mbrfat.bin $RPM_BUILD_ROOT%{_datadir}/%{name}/x86
%if %{new_ldlinux}
install -p -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/%{name}/x86/ldlinux.bss
install -p -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/%{name}/x86/ldlinux.sys
%else
install -p -m644 test/ldlinux.bss $RPM_BUILD_ROOT%{_datadir}/%{name}/x86
install -p -m644 test/ldlinux.sys $RPM_BUILD_ROOT%{_datadir}/%{name}/x86
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc AUTHORS COPYING HISTORY README README.usbboot
%{_bindir}/*
%{_datadir}/%{name}
%{_mandir}/*/*


%changelog
* Fri Jun 18 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1.4-10
- Rebuilt with -fno-strict-aliasing (#605200)

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.4-9.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4-7
- Autorebuild for GCC 4.3

* Thu Sep 27 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.4-6
- always distribute own ldlinux.sys as well as ldlinux.bss
- add conditional macro %%{new_ldlinux} (default off) to build the package
  with ldlinux.bss and ldlinux.sys taken from some syslinux source directly.
- Update README.usbboot .

* Fri Aug 17 2007 Dmitry Butskoy <Dmitry@Butskoy.name>
- Change License tag to GPLv2+

* Fri Sep  1 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.4-5
- rebuild for FC6

* Tue Aug  1 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.4-4
- avoid world-writable docs (#200829)

* Wed Feb 15 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.4-3
- rebuild for FC5

* Mon Dec 26 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.4-2
- place mbrfat.bin and ldlinux.bss under %%{_datadir}/%%{name}/x86

* Mon Dec 24 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.4-1
- accepted for Fedora Extra (review by John Mahowald <jpmahowald@gmail.com>)

* Mon Oct  3 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 1.4-1
- initial release
- install mbrfat.bin and ldlinux.bss binary files, they are
  actually needed to create something useful here.
- add README.usbboot -- instruction how to make diskboot.img more helpful
  (written by me).

