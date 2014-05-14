### RPM external py2-sqlalchemy 0.8.2
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_PLAT_LIB_SITE_PACKAGES}

Source: https://pypi.python.org/packages/source/S/SQLAlchemy/SQLAlchemy-%{realversion}.tar.gz
Requires: python 

Patch0: py2-sqlalchemy-0.8.2-add-frontier-dialect

%prep
%setup -n SQLAlchemy-%{realversion}
%patch0 -p1

%build
python setup.py build

%install
python setup.py install --skip-build --prefix=%{i}

find %{i} -name '*.egg-info' -exec rm {} \;
