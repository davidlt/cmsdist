### RPM external professor 1.0.0
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_PURE_LIB_SITE_PACKAGES}
Source: http://www.hepforge.org/archive/professor/professor-%{realversion}.tar.gz

Requires: py2-numpy py2-scipy pyminuit2 py2-matplotlib

%prep
%setup -n %{n}-%{realversion}

%build
python setup.py build

%install
export MPLCONFIGDIR=${PWD}

mkdir -p %{i}/${PYTHON_PURE_LIB_SITE_PACKAGES}
export PYTHONPATH=%{i}/${PYTHON_PURE_LIB_SITE_PACKAGES}:${PYTHONPATH}
python setup.py install --record=/dev/null --skip-build --prefix=%{i}
find %{i}/${PYTHON_PURE_LIB_SITE_PACKAGES} -name '*.egg' -type d -print0 | xargs -0 rm -rf

find %{i} -type f -exec sed -ideleteme '1 { s|^#!.*/bin/python|#!/usr/bin/env python| }' {} \;
find %{i} -name '*deleteme' -delete
