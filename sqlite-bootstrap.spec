### RPM external sqlite-bootstrap 3.8.1
Source: http://www.sqlite.org/2013/sqlite-autoconf-3080100.tar.gz

BuildRequires: autotools

%prep
%setup -n sqlite-autoconf-3080100

%build

case %{cmsplatf} in
  *_aarch64_* )
    # Rerun with a new autoconf to add support for AArch64
    autoreconf -fiv
    ;;
esac

./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-tcl --disable-static
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
