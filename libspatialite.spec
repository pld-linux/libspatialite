#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Spatial SQL database engine based on SQLite
Summary(pl.UTF-8):	Silnik przestrzennej bazy danych SQL oparty na SQLite
Name:		libspatialite
Version:	3.0.1
Release:	2
License:	MPL v1.1 or GPL v2+ or LGPL v2.1+
Group:		Libraries
Source0:	http://www.gaia-gis.it/gaia-sins/libspatialite-sources/%{name}-%{version}.tar.gz
# Source0-md5:	450d1a0d9da1bd9f770b7db3f2509f69
URL:		https://www.gaia-gis.it/fossil/libspatialite
%{?with_apidocs:BuildRequires:	doxygen >= 1.7.3}
BuildRequires:	freexl-devel >= 0.0.4
BuildRequires:	geos-devel >= 3.3.0
BuildRequires:	proj-devel >= 4
BuildRequires:	sqlite3-devel >= 3.7.3
Requires:	freexl >= 0.0.4
Requires:	geos >= 3.3.0
Requires:	proj >= 4
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
Requires:	freexl-devel >= 0.0.4
Requires:	geos-devel >= 3.3.0
Requires:	proj-devel >= 4
Requires:	sqlite3-devel >= 3.7.3

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

%description apidocs
API and internal documentation for spatialite library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki spatialite.

%prep
%setup -q

%build
%configure

%{__make}

%{?with_apidocs:doxygen}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libspatialite.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS
%attr(755,root,root) %{_libdir}/libspatialite.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libspatialite.so.2

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
