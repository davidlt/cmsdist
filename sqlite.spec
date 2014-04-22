### RPM external sqlite 3.8.4.3
Source: https://sqlite.org/2014/sqlite-autoconf-3080403.tar.gz

BuildRequires: autotools

%prep
%setup -n sqlite-autoconf-3080403

%build

./configure --build="%{_build}" --host="%{_host}" --prefix=%{i} \
            --disable-static --disable-dependency-tracking
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
%define strip_files %{i}/lib
