Summary: Python bindings for libparted.
Name: pylibparted
Version: 0.9.0
Release: 1
License: GPL
Group: System Environment/Libraries
Source0: %{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: parted >= 1.6.22, python
BuildRequires: parted-devel >= 1.6.22, python-devel, python-tools, python

%description
Python bindings for libparted functions to manipulate partition tables.

%prep
%setup -q

%build
make

%install
rm -rf ${RPM_BUILD_ROOT}
destdir=$(basename $(find /usr/lib -maxdepth 1 -mindepth 1 -name 'python*'))
broot=%{buildroot}
broot=${broot//\//\\/}
%makeinstall destdir=${destdir} buildroot=${broot} srcdir=${RPM_BUILD_DIR}/%{name}-%{version}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc README COPYING %{name}.html
%{_libdir}/python?.?/site-packages/*.so

%changelog
* Wed Aug 31 2005 Ulisses Furquim <ulissesf@gmail.com>
- Fixed installation of the API documentation file.

* Tue Aug 30 2005 Ulisses Furquim <ulissesf@gmail.com>
- Added API documentation.

* Wed Aug 24 2005 Ulisses Furquim <ulissesf@gmail.com>
- Initial spec version.
