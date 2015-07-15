### RPM external openssl 0.9.8e__1.0.2d
%define slc_version 0.9.8e
%define generic_version 1.0.2d
Source0: http://davidlt.web.cern.ch/davidlt/vault/openssl-1.0.2d-5675d07a144aa1a6c85f488a95aeea7854e86059.tar.bz2
Source1: http://cmsrep.cern.ch/cmssw/openssl-sources/openssl-fips-%{slc_version}-usa.tar.bz2
Patch0: openssl-0.9.8e-rh-0.9.8e-12.el5_4.6
Patch1: openssl-x86-64-gcc420
Patch2: openssl-1.0.1g-disable-install_docs

%define ismac %(case %{cmsplatf} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isaarch64 %(case %{cmsplatf} in (*_aarch64_*) echo 1 ;; (*) echo 0 ;; esac)
%define isslc_amd64 %(case %{cmsplatf} in (slc*_amd64_*) echo 1 ;; (*) echo 0 ;; esac)
%define isfc %(case %{cmsplatf} in (fc*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%if 0%{isaarch64}%{isfc}%{ismac}
%setup -b 0 -n openssl-%{generic_version}
%patch2 -p1
%endif
%if 0%{isslc_amd64}
%setup -b 1 -n openssl-fips-%{slc_version}
%patch0 -p1
%patch1 -p1
%endif

%build

case "%{cmsplatf}" in
  slc*_amd64_*)
    RPM_OPT_FLAGS="-O2 -fPIC -g -pipe -Wall -Wa,--noexecstack -fno-strict-aliasing \
                   -Wp,-DOPENSSL_USE_NEW_FUNCTIONS -Wp,-D_FORTIFY_SOURCE=2 -fexceptions \
                   -fstack-protector --param=ssp-buffer-size=4 -mtune=generic"
    ;;
  *_aarch64_*|fc*)
    RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"
    ;;
esac

case "%{cmsplatf}" in
  osx*)         target=darwin64-x86_64-cc ;;
  *_armv7hl_*)  target=linux-armv4 ;;
  *_aarch64_*)  target=linux-aarch64 ;;
  *_ppc64le_*)  target=linux-ppc64le ;;
  *)            target=linux-generic64 ;;
esac

case "%{cmsplatf}" in
  osx*)
    cfg_args="-DOPENSSL_USE_NEW_FUNCTIONS"
    ;;
  *_aarch64_*|fc*)
    cfg_args="--with-krb5-flavor=MIT --with-krb5-dir=/usr enable-krb5 no-zlib --openssldir=%{_sysconfdir}/pki/tls fips no-ec2m no-gost no-srp"
    ;;
  *)
    cfg_args="--with-krb5-flavor=MIT enable-krb5 fipscanisterbuild no-ec no-ecdh no-ecdsa"
    ;;
esac

export RPM_OPT_FLAGS

perl ./Configure ${target} ${cfg_args} enable-seed enable-tlsext enable-rfc3779 no-asm \
                 no-idea no-mdc2 no-rc5 shared --prefix=%{i}

case "%{cmsplatf}" in
  *_aarch64_*|fc*|osx*)
    make depend
    ;;
esac

make all

%install
case "%{cmsplatf}" in
  slc*_amd64_*)
    RPM_OPT_FLAGS="-O2 -fPIC -g -pipe -Wall -Wa,--noexecstack -fno-strict-aliasing \
                   -Wp,-DOPENSSL_USE_NEW_FUNCTIONS -Wp,-D_FORTIFY_SOURCE=2 -fexceptions \
                   -fstack-protector --param=ssp-buffer-size=4 -mtune=generic"
    ;;
  *_aarch64_*|fc*)
    RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -DPURIFY"
    ;;
esac

export RPM_OPT_FLAGS

make install

rm -rf %{i}/lib/pkgconfig
# We remove archive libraries because otherwise we need to propagate everywhere
# their dependency on kerberos.
rm -rf %{i}/lib/*.a

sed -ideleteme -e 's;^#!.*perl;#!/usr/bin/env perl;' \
  %{i}/bin/c_rehash
find %{i} -name '*deleteme' -type f -print0 | xargs -0 rm -f

%post
%{relocateConfig}bin/c_rehash
%{relocateConfig}include/openssl/opensslconf.h
