### RPM external nss-bootstrap 3.17.4
%define tag 54d4a1c5f968f7d329c2d076bac2c54b6421ea71
%define branch cms/v3.17.4
%define github_user cms-externals
Source: git+https://github.com/%github_user/nss.git?obj=%{branch}/%{tag}&export=nss-%{realversion}&output=/nss-%{realversion}-%{tag}.tgz

Requires: nspr-bootstrap sqlite-bootstrap zlib-bootstrap

%define strip_files %{i}/lib

%prep
%setup -n nss-%{realversion}

%build
export NSPR_INCLUDE_DIR="${NSPR_BOOTSTRAP_ROOT}/include/nspr"
export NSPR_LIB_DIR="${NSPR_BOOTSTRAP_ROOT}/lib"
export FREEBL_LOWHASH=1
export FREEBL_NO_DEPEND=1
export BUILD_OPT=1
export NSS_NO_PKCS11_BYPASS=1
export ZLIB_INCLUDE_DIR="${ZLIB_BOOTSTRAP_ROOT}/include"
export ZLIB_LIB_DIR="${ZLIB_BOOTSTRAP_ROOT}/lib"
case "%{cmsplatf}" in
  *_amd64_*|*_aarch64_* )
    export USE_64=1
    ;;
esac

make -C ./nss/coreconf clean
make -C ./nss/lib/dbm clean
make -C ./nss clean
make -C ./nss/coreconf
make -C ./nss/lib/dbm
make -C ./nss

%install
install -d %{i}/include/nss3
install -d %{i}/lib
find ./dist/public/nss -name '*.h' -exec install -m 644 {} %{i}/include/nss3 \;
find ./dist/*.OBJ/lib \( -name '*.dylib' -o -name '*.so' \) -exec install -m 755 {} %{i}/lib \;

rm -rf %{i}/lib/libsoftokn3*
rm -rf %{i}/lib/libsql*
rm -rf %{i}/lib/libfreebl3*
