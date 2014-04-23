### RPM external nspr 4.10.4
Source: https://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{realversion}/src/nspr-%{realversion}.tar.gz
%define strip_files %{i}/lib

%prep
%setup -n nspr-%{realversion}

%build
pushd nspr

# Update config.{sub,quess} for AArch64
rm -f ./build/autoconf/config.{sub,guess}
curl -L -k -s -o ./build/autoconf/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./build/autoconf/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./build/autoconf/config.{sub,guess}

CONF_OPTS="--disable-static --prefix=%{i} --build=%{_build} --host=%{_host}"
case "%{cmsplatf}" in
  *_aarch64_*|*_amd64_* )
    CONF_OPTS="${CONF_OPTS} --enable-64bit"
    ;;
esac

./configure ${CONF_OPTS}
make %{makeprocesses}
popd

%install
pushd nspr
make install
popd
