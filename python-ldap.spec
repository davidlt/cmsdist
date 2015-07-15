### RPM external python-ldap 2.4.10
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}

Source: http://pypi.python.org/packages/source/p/%{n}/%{n}-%{realversion}.tar.gz
Requires: python openssl openldap

%define isaarch64 %(case %{cmsplatf} in (*_aarch64_*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%setup -q -n %{n}-%{realversion}

%build
sed -i'' "s:\(library_dirs =\)\(.*\):\1 ${OPENSSL_ROOT}\/lib ${PYTHON_ROOT}\/lib ${OPENLDAP_ROOT}\/lib:g" setup.cfg
sed -i'' "s:\(include_dirs =\)\(.*\):\1 ${OPENSSL_ROOT}\/include ${PYTHON_ROOT}\/include ${OPENLDAP_ROOT}\/include:g" setup.cfg
sed -i'' "s:\(defines = \)\(.*\):\1 HAVE_TLS HAVE_LIBLDAP_R:g" setup.cfg

python setup.py build

%install

%if 0%{isaarch64}
  mkdir -p %{i}/${PYTHON_LIB_SITE_PACKAGES}
  export PYTHONPATH=%{i}/${PYTHON_LIB_SITE_PACKAGES}:${PYTHONPATH}
%endif

python setup.py install --skip-build --prefix=%{i}
