#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	libxml2		# XML documents support

Summary:	Spatial SQL database engine based on SQLite
Summary(pl.UTF-8):	Silnik przestrzennej bazy danych SQL oparty na SQLite
Name:		libspatialite
Version:	5.1.0
Release:	2
# libspatialite itself is MPL v1.1 or GPL v2+ or LGPL v2.1+, but gcp and rttopo features enforce GPL
License:	GPL v2+
Group:		Libraries
Source0:	http://www.gaia-gis.it/gaia-sins/libspatialite-sources/%{name}-%{version}.tar.gz
# Source0-md5:	2db597114bd6ee20db93de3984fd116c
URL:		https://www.gaia-gis.it/fossil/libspatialite
%{?with_apidocs:BuildRequires:	doxygen >= 1.7.3}
BuildRequires:	freexl-devel >= 2.0.0
BuildRequires:	geos-devel >= 3.10.0
BuildRequires:	librttopo-devel >= 1.1.0
%{?with_libxml2:BuildRequires:	libxml2-devel >= 2.0}
BuildRequires:	minizip-devel
BuildRequires:	proj-devel >= 4.8.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	sqlite3-devel >= 3.8.5
BuildRequires:	zlib-devel
Requires:	freexl >= 1.0.1
Requires:	geos >= 3.7.0
Requires:	librttopo >= 1.1.0
Requires:	proj >= 4.8.0
Requires:	sqlite3 >= 3.8.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Spatial SQL database engine based on SQLite.

%description -l pl.UTF-8
Silnik przestrzennej bazy danych SQL oparty na SQLite.

%package devel
Summary:	Header files for spatialite library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki spatialite
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	freexl-devel >= 1.0.1
Requires:	geos-devel >= 3.7.0
Requires:	librttopo-devel >= 1.1.0
%{?with_libxml2:Requires:	libxml2-devel >= 2.0}
Requires:	minizip-devel
Requires:	proj-devel >= 4.8.0
Requires:	sqlite3-devel >= 3.8.5
Requires:	zlib-devel

%description devel
Header files for spatialite library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki spatialite.

%package static
Summary:	Static spatialite library
Summary(pl.UTF-8):	Statyczna biblioteka spatialite
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static spatialite library.

%description static -l pl.UTF-8
Statyczna biblioteka spatialite.

%package apidocs
Summary:	spatialite API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki spatialite
Group:		Documentation
BuildArch:	noarch

%description apidocs
API and internal documentation for spatialite library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki spatialite.

%prep
%setup -q

%build
%configure \
	--enable-geocallbacks \
	--enable-geopackage \
	%{!?with_libxml2:--disable-libxml2}

%{__make}

%{?with_apidocs:doxygen}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# loadable module
%{__rm} $RPM_BUILD_ROOT%{_libdir}/mod_spatialite.la
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libspatialite.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/libspatialite.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspatialite.so.8
# sqlite3 module
%attr(755,root,root) %{_libdir}/mod_spatialite.so*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspatialite.so
%{_includedir}/spatialite
%{_includedir}/spatialite.h
%{_pkgconfigdir}/spatialite.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libspatialite.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc html/{search,*.css,*.html,*.js,*.png}
%endif
