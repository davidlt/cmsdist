### RPM external xerces-c 3.1.1
Source: http://mirror.switch.ch/mirror/apache/dist//xerces/c/3/sources/xerces-c-%{realversion}.tar.gz

Requires: curl

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++11
%endif

%prep
%setup -n %{n}-%{realversion}

# Update to get AArch64
rm -f ./config/config.{sub,guess}
curl -L -k -s -o ./config/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config/config.{sub,guess}

%build
CFLAGS=
CXXFLAGS="%{cms_cxxflags}"
case "%{cmsplatf}" in
  osx*)
    CFLAGS="-arch x86_64 ${CFLAGS}"
    CXXFLAGS="-arch x86_64 ${CXXFLAGS}"
    ;;
esac

./configure \
  --prefix=%{i} \
  --disable-rpath \
  --disable-static \
  --disable-pretty-make \
  --disable-dependency-tracking \
  --with-curl="${CURL_ROOT}" \
  CFLAGS="${CFLAGS}" \
  CXXFLAGS="${CXXFLAGS}"

make %{makeprocesses}

%install
make install
