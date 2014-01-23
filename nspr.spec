### RPM external nspr 4.10.1
Source: https://ftp.mozilla.org/pub/mozilla.org/nspr/releases/v%{realversion}/src/nspr-%{realversion}.tar.gz
%define strip_files %{i}/lib

%define isamd64 %(case %{cmsplatf} in (*amd64*|*_mic_*|*_aarch64_*) echo 1 ;; (*) echo 0 ;; esac)
%prep  
%setup -n nspr-%{realversion}

%build
pushd nspr

# Update config.{sub,quess} for AArch64
rm -f ./build/autoconf/config.{sub,guess}
curl -L -k -s -o ./build/autoconf/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./build/autoconf/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'

CONF_OPTS="--disable-static --prefix=%{i} --build=%{_build} --host=%{_host}"
%if %isamd64
CONF_OPTS="${CONF_OPTS} --enable-64bit"
%endif

./configure ${CONF_OPTS}
make %{makeprocesses}
popd

%install
pushd nspr
make install
popd
