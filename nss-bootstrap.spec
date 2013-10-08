### RPM external nss-bootstrap 3.15.2
%define release_version %(echo "%{realversion}" | tr . _)_RTM
Source: https://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/NSS_%{release_version}/src/nss-%{realversion}.tar.gz
Requires: nspr-bootstrap sqlite-bootstrap
Patch0: nss-3.15.2-add-SQLITE-LIBS-DIR
Patch1: nss-3.15.2-add-ZLIB-LIBS-DIR-and-ZLIB-INCLUDE-DIR

%define isamd64 %(case %{cmsplatf} in (*amd64*|*_mic_*) echo 1 ;; (*) echo 0 ;; esac)

Requires: zlib-bootstrap

%prep
%setup -n nss-%{realversion}
%patch0 -p1
%patch1 -p1

%build
export NSPR_INCLUDE_DIR="${NSPR_BOOTSTRAP_ROOT}/include/nspr"
export NSPR_LIB_DIR="${NSPR_BOOTSTRAP_ROOT}/lib"
export USE_SYSTEM_ZLIB=1
export ZLIB_INCLUDE_DIR="${ZLIB_BOOTSTRAP_ROOT}/include"
export ZLIB_LIBS_DIR="${ZLIB_BOOTSTRAP_ROOT}/lib"
export NSS_USE_SYSTEM_SQLITE=1
export SQLITE_INCLUDE_DIR="${SQLITE_BOOTSTRAP_ROOT}/include"
export SQLITE_LIBS_DIR="${SQLITE_BOOTSTRAP_ROOT}/lib"
export NSS_NO_PKCS11_BYPASS=1
export FREEBL_NO_DEPEND=1
export NSS_BUILD_WITHOUT_SOFTOKEN=1
export USE_SYSTEM_FREEBL=1
export USE_SYSTEM_SOFTOKEN=1
export BUILD_OPT=1
%if %isamd64
export USE_64=1
%endif

# We are not building freebl/softoken/util
%{__rm} -rf ./nss/lib/freebl
%{__rm} -rf ./nss/lib/softoken
%{__rm} -rf ./nss/lib/util

make -C ./nss/coreconf clean
make -C ./nss/lib/dbm clean
make -C ./nss clean
make -C ./nss/coreconf
make -C ./nss/lib/dbm
make -C ./nss

%install
case %{cmsplatf} in
  osx*)
    soname=dylib ;;
  *)
    soname=so ;;
esac

install -d %{i}/include/nss3
install -d %{i}/lib
find mozilla/dist/public/nss -name '*.h' -exec install -m 644 {} %{i}/include/nss3 \;
find . -path "*/mozilla/dist/*.OBJ/lib/*.${soname}" -exec install -m 755 {} %{i}/lib \;
%define strip_files %{i}/lib
