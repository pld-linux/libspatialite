#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	libxml2		# XML documents support
%bcond_without	lwgeom		# LWGEOM support
%bcond_with	bootstrap	# bootstrap without postgis dependency

%if %{with bootstrap}
%undefine	with_lwgeom
%endif

Summary:	Spatial SQL database engine based on SQLite
Summary(pl.UTF-8):	Silnik przestrzennej bazy danych SQL oparty na SQLite
Name:		libspatialite
Version:	4.3.0a
Release:	2
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		Libraries
Source0:	http://www.gaia-gis.it/gaia-sins/libspatialite-sources/%{name}-%{version}.tar.gz
# Source0-md5:	6b380b332c00da6f76f432b10a1a338c
Patch0:		%{name}-lwgeom.patch
URL:		https://www.gaia-gis.it/fossil/libspatialite
%{?with_apidocs:BuildRequires:	doxygen >= 1.7.3}
BuildRequires:	freexl-devel >= 1.0.1
BuildRequires:	geos-devel >= 3.4.0
%{?with_lwgeom:BuildRequires:	liblwgeom-devel}
%{?with_libxml2:BuildRequires:	libxml2-devel >= 2.0}
BuildRequires:	proj-devel >= 4.8.0
BuildRequires:	sqlite3-devel >= 3.7.3
BuildRequires:	zlib-devel
Requires:	freexl >= 1.0.1
Requires:	geos >= 3.4.0
Requires:	proj >= 4.8.0
Requires:	sqlite3 >= 3.7.3
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
Requires:	geos-devel >= 3.4.0
%{?with_lwgeom:Requires:	liblwgeom-devel}
%{?with_libxml2:Requires:	libxml2-devel >= 2.0}
Requires:	proj-devel >= 4.8.0
Requires:	sqlite3-devel >= 3.7.3
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API and internal documentation for spatialite library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki spatialite.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--enable-geocallbacks \
	--enable-geopackage \
	%{?with_libxml2:--enable-libxml2} \
	%{?with_lwgeom:--enable-lwgeom}

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
%attr(755,root,root) %ghost %{_libdir}/libspatialite.so.7
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
%doc html/*
%endif
