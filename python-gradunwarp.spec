%global modname gradunwarp
# we don't want to provide private python extension libs in the python2 dir
%global __provides_exclude_from ^%{python_sitearch}/.*\\.so$

Name:           python-%{modname}
Version:        1.0.2
Release:        2%{?dist}
Summary:        Gradient Unwarping

License:        MIT
URL:            https://github.com/Washington-University/gradunwarp
Source0:        https://github.com/Washington-University/gradunwarp/archive/v%{version}/%{modname}-%{version}.tar.gz
# Python 3 support
# https://github.com/Washington-University/gradunwarp/pull/4
Patch0:         0001-py3-make-modules-compatible.patch
Patch1:         0002-py3-make-other-stuff-compatible.patch

BuildRequires:  git-core
BuildRequires:  gcc

%description
Python/Numpy package used to unwarp the distorted volumes (due to the gradient
field inhomogenities).

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel
BuildRequires:  numpy scipy
BuildRequires:  python2-nibabel
BuildRequires:  python2-nose
Requires:       numpy scipy
Requires:       python2-nibabel

%description -n python2-%{modname}
Python/Numpy package used to unwarp the distorted volumes (due to the gradient
field inhomogenities).

Python 2 version.

%package -n python3-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-numpy python3-scipy
BuildRequires:  python3-nibabel
BuildRequires:  python3-nose
Requires:       python3-numpy python3-scipy
Requires:       python3-nibabel

%description -n python3-%{modname}
Python/Numpy package used to unwarp the distorted volumes (due to the gradient
field inhomogenities).

Python 3 version.

%prep
%autosetup -n %{modname}-%{version} -S git

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

mv %{buildroot}%{_bindir}/gradient_unwarp.py %{buildroot}%{_bindir}/gradient_unwarp
sed -i -e '1s|^.*$|#!%{__python3}|' %{buildroot}%{_bindir}/gradient_unwarp

find %{buildroot}%{python2_sitearch}/%{modname} -name '*.c' -delete
find %{buildroot}%{python3_sitearch}/%{modname} -name '*.c' -delete

# remove file which installs into bindir
rm -f %{buildroot}%{python2_sitearch}/%{modname}/core/gradient_unwarp.py*
rm -f %{buildroot}%{python3_sitearch}/%{modname}/core/gradient_unwarp.py*

# fix perms on .so
find %{buildroot}%{python2_sitearch}/%{modname}/ -name '*.so' -exec chmod 755 {} ';'
find %{buildroot}%{python3_sitearch}/%{modname}/ -name '*.so' -exec chmod 755 {} ';'

%check
pushd gradunwarp/core/tests/
  PYTHONPATH=%{buildroot}%{python2_sitearch} nosetests-%{python2_version} -v
  PYTHONPATH=%{buildroot}%{python3_sitearch} nosetests-%{python3_version} -v
popd

%files -n python2-%{modname}
%license Copying.md
%doc README.md
%{python2_sitearch}/%{modname}*

%files -n python3-%{modname}
%license Copying.md
%doc README.md
%{_bindir}/gradient_unwarp
%{python3_sitearch}/%{modname}*

%changelog
* Wed Nov 25 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.2-2
- Fix shebang
- Add python3 version
- Fix perms on so

* Sun Nov 08 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.2-1
- Initial package
