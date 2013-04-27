#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	Implementation of SVG Tiny
Name:		libsvgtiny
Version:	0.1.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://download.netsurf-browser.org/libs/releases/%{name}-%{version}-src.tar.gz
# Source0-md5:	b1da875a8cfa4e005bb74c6aac62baf1
URL:		http://www.netsurf-browser.org/projects/libsvgtiny/
BuildRequires:	libdom-devel >= 0.0.1
BuildRequires:	libwapcaplet-devel >= 0.2.0
BuildRequires:	netsurf-buildsystem
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libsvgtiny is an implementation of SVG Tiny, written in C. It is
currently in development for use with NetSurf and is intended to be
suitable for use in other projects too.

The overall idea of the library is to take some SVG as input, and
return a list of paths and texts which can be rendered easily. The
library does not do the actual rendering.

%package devel
Summary:	libsvgtiny library headers
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libsvgtiny
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the libraries, include files and other resources you can use
to incorporate libsvgtiny into applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe pozwalające na używanie biblioteki libsvgtiny w
swoich programach.

%package static
Summary:	libsvgtiny static libraries
Summary(pl.UTF-8):	Statyczne biblioteki libsvgtiny
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This is package with static libsvgtiny libraries.

%description static -l pl.UTF-8
Statyczna biblioteka libsvgtiny.

%prep
%setup -q

%build
CFLAGS="%{rpmcflags}"
LDFLAGS="%{rpmldflags}"
export CFLAGS
export LDFLAGS

%{__make} PREFIX=%{_prefix} COMPONENT_TYPE=lib-shared Q='' \
	-Iinclude -Isrc"
%if %{with static_libs}
%{__make} PREFIX=%{_prefix} COMPONENT_TYPE=lib-static Q='' \
	-Iinclude -Isrc"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-shared \
	Q=''

%if %{with static_libs}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	COMPONENT_TYPE=lib-static \
	Q=''
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/*.h
%{_pkgconfigdir}/*pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
