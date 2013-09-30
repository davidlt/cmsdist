### RPM external openblas v0.2.8

Source: https://github.com/xianyi/OpenBLAS/archive/%{realversion}.tar.gz

%prep
%setup -q -n OpenBLAS-%(echo "%{realversion}" | sed 's/^v//')

%build
FC=gfortran USE_THREAD=0 DYNAMIC_ARCH=1 make %{makeprocesses}

%install
make install PREFIX=%{i}
