### RPM external ncurses-bootstrap 5.9
Source: http://ftp.gnu.org/pub/gnu/ncurses/ncurses-%{realversion}.tar.gz
%define keep_archives true
%define drop_files %{i}/lib/*.so

%prep
%setup -n ncurses-%{realversion}

%build
# Update for AArch64 support
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'

./configure --prefix="%{i}" \
            --build="%{_build}" \
            --host="%{_host}" \
            --disable-shared \
            --enable-static \
            --without-debug \
            --without-ada \
            --without-manpages \
            --disable-database \
            --enable-termcap

make %{makeprocesses} CFLAGS="-O2 -fPIC" CXXFLAGS="-O2 -fPIC -std=c++11"

%install
make install
