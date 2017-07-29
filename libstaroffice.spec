#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Library for importing of StarOffice documents
Summary(pl.UTF-8):	Biblioteka do importowania dokumentów StarOffice'a
Name:		libstaroffice
Version:	0.0.4
Release:	1
License:	MPL v2.0
Group:		Libraries
#Source0Download: https://github.com/fosnola/libstaroffice/releases
Source0:	https://github.com/fosnola/libstaroffice/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	cc9ab242fdc3d1a96151912610d57fb1
URL:		https://github.com/fosnola/libstaroffice/wiki
BuildRequires:	doxygen
BuildRequires:	librevenge-devel >= 0.0
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libstaroffice is a library for importing of StarOffice documents.

%description -l pl.UTF-8
libstaroffice to biblioteka do importowania i konwersji dokumentów
StarOffice'a.

%package devel
Summary:	Development files for libstaroffice
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libstaroffice
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	librevenge-devel >= 0.0
Requires:	libstdc++-devel >= 6:4.7
Requires:	zlib-devel

%description devel
This package contains the header files for developing applications
that use libstaroffice.

%description devel -l pl.UTF-8
Ten pakiet zawiera biblioteki i pliki nagłówkowe do tworzenia
aplikacji wykorzystujących bibliotekę libstaroffice.

%package static
Summary:	Static libstaroffice library
Summary(pl.UTF-8):	Statyczna biblioteka libstaroffice
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libstaroffice library.

%description static -l pl.UTF-8
Statyczna biblioteka libstaroffice.

%package apidocs
Summary:	API documentation for libstaroffice library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libstaroffice
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for libstaroffice library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libstaroffice.

%package tools
Summary:	Tools to transform StarOffice files into other formats
Summary(pl.UTF-8):	Narzędzia do przekształcania plików StarOffice'a do innych formatów
Group:		Applications/Publishing
Requires:	%{name} = %{version}-%{release}

%description tools
Tools to transform StarOffice files into other formats. Currently
supported: CSV, HTML, SVG, text, raw.

%description tools -l pl.UTF-8
Narzędzia do przekształcania plików StarOffice'a do innych formatów.
Obecnie obsługiwane są: CSV, HTML, SVG, tekstowy i surowy.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-sharedptr=c++11

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

# we install API docs directly from build
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libstaroffice-0.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstaroffice-0.0.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libstaroffice-0.0.so
%{_includedir}/libstaroffice-0.0
%{_pkgconfigdir}/libstaroffice-0.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libstaroffice-0.0.a
%endif

%files apidocs
%defattr(644,root,root,755)
%doc docs/doxygen/html/*

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sd2raw
%attr(755,root,root) %{_bindir}/sd2svg
%attr(755,root,root) %{_bindir}/sd2text
%attr(755,root,root) %{_bindir}/sdc2csv
%attr(755,root,root) %{_bindir}/sdw2html
