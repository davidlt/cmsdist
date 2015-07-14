### RPM external professor 1.4.0
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_PURE_LIB_SITE_PACKAGES}
Source: http://www.hepforge.org/archive/professor/professor-%{realversion}.tar.gz

Requires: py2-numpy py2-scipy pyminuit2 py2-matplotlib
%prep
%setup -n professor-%{realversion}

%build
${PYTHON_ROOT}/bin/python setup.py build

%install
${PYTHON_ROOT}/bin/python setup.py install --prefix=%i
