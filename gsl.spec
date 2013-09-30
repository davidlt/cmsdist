### RPM external gsl 1.16
Source: ftp://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.gz
Patch0:  gsl-1.10-gcc46

%define keep_archives true
%define drop_files %{i}/share

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
./configure \
  --prefix=%{i} \
  --with-pic \
  --disable-dependency-tracking \
  --disable-silent-rules \
  CFLAGS="-O2"

make %{makeprocesses}

%install
make install

find %{i}/lib -name '*.la' -delete

%post
%{relocateConfig}bin/gsl-config
