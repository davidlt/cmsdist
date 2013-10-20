### RPM external nss-bootstrap 3.15.2
%define release_version %(echo "%{realversion}" | tr . _)_RTM
Source: https://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/NSS_%{release_version}/src/nss-%{realversion}.tar.gz
Requires: nspr-bootstrap sqlite-bootstrap
Patch0: nss-3.15.2-0001-Add-support-for-non-standard-location-zlib.patch

%define isamd64 %(case %{cmsplatf} in (*amd64*|*_mic_*|*_aarch64_*) echo 1 ;; (*) echo 0 ;; esac)

# TODO: No need for SQLite3, it's used only for libsoftokn3, which we do not distribute.
#       Some details: http://www.linuxfromscratch.org/blfs/view/svn/postlfs/nss.html

Requires: zlib-bootstrap

%prep
%setup -n nss-%{realversion}
%patch0 -p1

%build
export NSPR_INCLUDE_DIR="${NSPR_BOOTSTRAP_ROOT}/include/nspr"
export NSPR_LIB_DIR="${NSPR_BOOTSTRAP_ROOT}/lib"
export FREEBL_LOWHASH=1
export FREEBL_NO_DEPEND=1
export BUILD_OPT=1
export NSS_NO_PKCS11_BYPASS=1
export ZLIB_INCLUDE_DIR="${ZLIB_BOOTSTRAP_ROOT}/include"
export ZLIB_LIB_DIR="${ZLIB_BOOTSTRAP_ROOT}/lib"
%if %isamd64
export USE_64=1
%endif

make -C ./nss/coreconf clean
make -C ./nss/lib/dbm clean
make -C ./nss clean
make -C ./nss/coreconf
make -C ./nss/lib/dbm
make -C ./nss 

%install
rm -rf %{i}/lib/libsoftokn3*
rm -rf %{i}/lib/libsql*
rm -rf %{i}/lib/libfreebl3*

install -d %{i}/include/nss3
install -d %{i}/lib
find ./dist/public/nss -name '*.h' -exec install -m 644 {} %{i}/include/nss3 \;
find ./dist/*.OBJ/lib -name '*.dylib' -o -name '*.so' -exec install -m 755 {} %{i}/lib \;
%define strip_files %{i}/lib
