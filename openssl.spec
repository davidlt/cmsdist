### RPM external openssl 0.9.8e__1.0.1g
%define slc_version 0.9.8e
%define generic_version 1.0.1g
Source0: http://www.openssl.org/source/%{n}-%{generic_version}.tar.gz
Source1: http://cmsrep.cern.ch/cmssw/openssl-sources/openssl-fips-%{slc_version}-usa.tar.bz2
Patch0: openssl-0.9.8e-rh-0.9.8e-12.el5_4.6
Patch1: openssl-x86-64-gcc420
Patch2: openssl-1.0.1g-disable-install_docs
Patch3: openssl-1.0.1g-use-lib64-for-krb5
Patch4: openssl-1.0.1-beta2-rpmbuild
Patch5: openssl-1.0.1g-fix-libcrypto-linkage

%define ismac %(case %{cmsplatf} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isfc %(case %{cmsplatf} in (fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isslc %(case %{cmsplatf} in (slc*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%if %ismac
%setup -b 0 -n %{n}-%{generic_version}
%patch2 -p1
%endif
%if %isfc
%setup -b 0 -n %{n}-%{generic_version}
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%endif
%if %isslc
%setup -b 1 -n openssl-fips-%{slc_version}
%patch0 -p1
%patch1 -p1
%endif

%build

case "%{cmsplatf}" in
  slc*)
    RPM_OPT_FLAGS="-O2 -fPIC -g -pipe -Wall -Wa,--noexecstack -fno-strict-aliasing \
                   -Wp,-DOPENSSL_USE_NEW_FUNCTIONS -Wp,-D_FORTIFY_SOURCE=2 -fexceptions \
                   -fstack-protector --param=ssp-buffer-size=4"
    ;;
  fc*)
    RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"
    ;;
esac

case "%{cmsplatf}" in
  osx*) target=darwin64-x86_64-cc ;;
  *)    target=linux-generic64 ;;
esac

case "%{cmsplatf}" in
  osx*)
    cfg_args="-DOPENSSL_USE_NEW_FUNCTIONS"
    ;;
  fc*)
    cfg_args="--with-krb5-flavor=MIT --with-krb5-dir=/usr enable-krb5 no-zlib"
    ;;
  *)
    cfg_args="--with-krb5-flavor=MIT enable-krb5 fipscanisterbuild"
    ;;
esac

perl ./Configure ${target} ${cfg_args} enable-seed enable-tlsext enable-rfc3779 no-asm \
                 no-idea no-mdc2 no-rc5 no-ec no-ecdh no-ecdsa shared --prefix=%{i}

case "%{cmsplatf}" in
  fc*|osx*)
    make depend
    ;;
esac

make

%install
case "%{cmsplatf}" in
  slc*)
    RPM_OPT_FLAGS="-O2 -fPIC -g -pipe -Wall -Wa,--noexecstack -fno-strict-aliasing \
                   -Wp,-DOPENSSL_USE_NEW_FUNCTIONS -Wp,-D_FORTIFY_SOURCE=2 -fexceptions \
                   -fstack-protector --param=ssp-buffer-size=4"
    ;;
  fc*)
    RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"
    ;;
esac

make install

rm -rf %{i}/lib/pkgconfig
# We remove archive libraries because otherwise we need to propagate everywhere
# their dependency on kerberos.
rm -rf %{i}/lib/*.a

sed -ideleteme -e 's;^#!.*perl;#!/usr/bin/env perl;' \
  %{i}/ssl/misc/CA.pl \
  %{i}/bin/c_rehash
find %{i} -name '*deleteme' -type f -print0 | xargs -0 rm -f 
