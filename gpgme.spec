Summary:	Library for accessing GnuPG
Name:		gpgme
Version:	1.4.2
Release:	1
Epoch:		1
License:	LGPL v2.1+
Group:		Libraries
Source0:	ftp://ftp.gnupg.org/gcrypt/gpgme/%{name}-%{version}.tar.bz2
# Source0-md5:	c8cb345ba7c0353e47bdf3c5c05e49be
Patch0:		%{name}-kill-tests.patch
URL:		http://www.gnupg.org/gpgme.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libassuan-devel
BuildRequires:	libgpg-error-devel
BuildRequires:	libtool
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A library for accessing GnuPG.

%package devel
Summary:	Header files for GPGME library
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files for GPGME library, needed for compiling programs using
GPGME.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static		\
	--with-gpg=%{_bindir}/gpg	\
	--with-gpgsm=%{_bindir}/gpgsm
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc README ChangeLog THANKS TODO NEWS AUTHORS
%attr(755,root,root) %ghost %{_libdir}/libgpgme-pthread.so.??
%attr(755,root,root) %ghost %{_libdir}/libgpgme.so.??
%attr(755,root,root) %{_libdir}/libgpgme-pthread.so.*.*.*
%attr(755,root,root) %{_libdir}/libgpgme.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gpgme-config
%attr(755,root,root) %{_libdir}/libgpgme-pthread.so
%attr(755,root,root) %{_libdir}/libgpgme.so
%{_libdir}/libgpgme-pthread.la
%{_libdir}/libgpgme.la
%{_includedir}/*.h
%{_aclocaldir}/*.m4
%{_infodir}/*.info*

