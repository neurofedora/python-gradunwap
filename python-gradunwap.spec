%global modname gradunwarp
# we don't want to provide private python extension libs in either the python2 or python3 dirs
%global __provides_exclude_from ^(%{python_sitearch}|%{python3_sitearch})/.*\\.so$

Name:           python-%{modname}
Version:        1.0.2
Release:        1%{?dist}
Summary:        Gradient Unwarping

License:        MIT
URL:            https://github.com/Washington-University/gradunwarp
Source0:        https://github.com/Washington-University/gradunwarp/archive/v%{version}/%{modname}-%{version}.tar.gz

%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel
BuildRequires:  numpy
BuildRequires:  python2-nose
BuildRequires:  gcc
Requires:       numpy

%description
Python/Numpy package used to unwarp the distorted volumes (due to the gradient
field inhomogenities).

%prep
%autosetup -n %{modname}-%{version}

%build
%py2_build

%install
%py2_install

mv %{buildroot}%{_bindir}/gradient_unwarp.py %{buildroot}%{_bindir}/gradient_unwarp
sed -i -e '1s|^.*$|#!/usr/bin/env %{__python2}|' %{buildroot}%{_bindir}/gradient_unwarp

find %{buildroot}%{python2_sitearch}/%{modname} -name '*.c' -delete

# remove file which installs into bindir
rm -f %{buildroot}%{python2_sitearch}/%{modname}/core/gradient_unwarp.py*

%check
pushd gradunwarp/core/tests/
  PYTHONPATH=%{buildroot}%{python2_sitearch} nosetests-%{python2_version} -v
popd

%files
%{_bindir}/gradient_unwarp
%{python2_sitearch}/%{modname}*

%changelog
* Sun Nov 08 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.2-1
- Initial package