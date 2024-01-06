#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Implementation of SVG Tiny
Summary(pl.UTF-8):	Implementacja SVG Tiny
Name:		libsvgtiny
Version:	0.1.8
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	77bc020beb58781a11404ff09c261fc3
URL:		http://www.netsurf-browser.org/projects/libsvgtiny/
BuildRequires:	gperf
BuildRequires:	libdom-devel >= 0.4.2
BuildRequires:	libwapcaplet-devel >= 0.4.1
BuildRequires:	netsurf-buildsystem >= 1.10
BuildRequires:	pkgconfig
Requires:	libdom >= 0.4.2
Requires:	libwapcaplet >= 0.4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libsvgtiny is an implementation of SVG Tiny, written in C. It is
currently in development for use with NetSurf and is intended to be
suitable for use in other projects too.

The overall idea of the library is to take some SVG as input, and
return a list of paths and texts which can be rendered easily. The
library does not do the actual rendering.

%description -l pl.UTF-8
Libsvgtiny to implementacja SVG Tiny napisana w C. Jest obecnie
rozwijana do wykorzystania w ramach projektu NetSurf, ale także z
myślą o możliwości użycia w innych projektach.

Ogólna idea biblioteki polega na przyjęciu SVG na wejściu i zwróceniu
listy ścieżek oraz tekstów, które można łatwo wyrenderować. Biblioteka
nie wykonuje samego renderowania.

%package devel
Summary:	libsvgtiny library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libsvgtiny
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libdom-devel >= 0.4.2

%description devel
This package contains the include files and other resources you can
use to incorporate libsvgtiny into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libsvgtiny w
swoich programach.

%package static
Summary:	libsvgtiny static library
Summary(pl.UTF-8):	Statyczna biblioteka libsvgtiny
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libsvgtiny library.

%description static -l pl.UTF-8
Statyczna biblioteka libsvgtiny.

%prep
%setup -q

%build
export AR="%{__ar}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} -j1 \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared

%if %{with static_libs}
%{__make} -j1 \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static
%endif

%install
rm -rf $RPM_BUILD_ROOT

export AR="%{__ar}"
export CC="%{__cc}"
export CFLAGS="%{rpmcflags}"
export LDFLAGS="%{rpmldflags}"

%{__make} -j1 install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-shared \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -j1 install \
	Q= \
	PREFIX=%{_prefix} \
	LIBDIR=%{_lib} \
	COMPONENT_TYPE=lib-static \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libsvgtiny.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsvgtiny.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsvgtiny.so
%{_includedir}/svgtiny.h
%{_pkgconfigdir}/libsvgtiny.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsvgtiny.a
%endif
