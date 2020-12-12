#
# Conditional build:
%bcond_with	gpl2	# GPL v2 compatible package (drop Apache v2 licensed components)

Summary:	C library for Storj V3 Network
Summary(pl.UTF-8):	Biblioteka C do sieci Storj V3
Name:		storj-uplink-c
Version:	1.2.0
Release:	1
License:	MIT, other (used go components)
Group:		Libraries
#Source0Download: https://github.com/storj/uplink-c/releases
Source0:	https://github.com/storj/uplink-c/archive/v%{version}/uplink-c-%{version}.tar.gz
# Source0-md5:	fd3b321db1b48839f58ca8da896f17b1
Patch0:		%{name}-libdir.patch
URL:		https://github.com/storj/uplink-c
BuildRequires:	golang >= 1.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C library for Storj V3 Network.

%description -l pl.UTF-8
Biblioteka C do sieci Storj V3.

%package devel
Summary:	Header files for Storj uplink library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Storj uplink
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Storj uplink library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Storj uplink.

%package static
Summary:	Static Storj uplink library
Summary(pl.UTF-8):	Statyczna biblioteka Storj uplink
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Storj uplink library.

%description static -l pl.UTF-8
Statyczna biblioteka Storj uplink.

%prep
%setup -q -n uplink-c-%{version}
%patch0 -p1

cat > scripts/version <<EOF
#!/bin/sh
echo %{version}
EOF

sed -i -e 's,^prefix=.*,prefix=%{_prefix},' \
	-e 's,^libdir=.*,libdir=%{_libdir},' scripts/gen-pkg-config

%build
%{__make} build \
	%{?with_gpl2:GPL2=true}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/libuplink.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/uplink
%{_pkgconfigdir}/libuplink.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libuplink.a
