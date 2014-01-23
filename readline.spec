### RPM external readline 6.2
Source: ftp://ftp.cwru.edu/pub/bash/%{n}-%{realversion}.tar.gz
%define keep_archives true
%define drop_files %{i}/lib/*.so

%prep
%setup -n %{n}-%{realversion}

%build
# Update for AArch64 support
rm -f ./support/config.{sub,guess}
curl -L -k -s -o ./support/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./support/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'

./configure --prefix %{i} --build="%{_build}" --host="%{_host}" \
            --disable-shared --enable-static
make %{makeprocesses} CFLAGS="-O2 -fPIC"

%install
make install
