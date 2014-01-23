### RPM external gdbm 1.10
Source: http://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build
# Update to get AArch64
rm -f ./build-aux/config.{sub,guess}
curl -L -k -s -o ./build-aux/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./build-aux/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'

./configure \
  --enable-libgdbm-compat \
  --prefix=%{i} \
  --disable-dependency-tracking \
  --disable-nls \
  --disable-rpath

make %{makeprocesses}

%define strip_files %{i}/lib
%define drop_files %{i}/share
