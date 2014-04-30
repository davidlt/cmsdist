### RPM external curl 7.36.0
Source: http://curl.haxx.se/download/%{n}-%{realversion}.tar.gz
Requires: nss
Requires: zlib
   
%prep
%setup -n %{n}-%{realversion}

%build
export ZLIB_ROOT
export NSS_ROOT
case %{cmsplatf} in
  slc6*|fc*) KERBEROS_ROOT=/usr ;;
  slc5*) KERBEROS_ROOT=/usr/kerberos ;;
  osx*) KERBEROS_ROOT=/usr/heimdal ;;
esac

./configure \
  --prefix=%{i} \
  --disable-static \
  --without-libidn \
  --disable-ldap \
  --with-zlib=${ZLIB_ROOT} \
  --without-ssl \
  --with-nss=${NSS_ROOT} \
  --with-gssapi=${KERBEROS_ROOT} \
  CPPFLAGS="-I${NSPR_ROOT}/include/nspr -I${NSS_ROOT}/include/nss3" \
  LDFLAGS="-L${NSPR_ROOT}/lib -L${NSS_ROOT}/lib"

make %{makeprocesses}

%install
make install
case %{cmsos} in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

# Trick to get our version of curl pick up our version of its associated shared
# library (which is different from the one coming from the system!).
case %cmsos in
  osx*)
install_name_tool -id %i/lib/libcurl-cms.dylib -change %i/lib/libcurl.4.dylib %i/lib/libcurl-cms.dylib  %i/lib/libcurl.4.dylib
install_name_tool -change %i/lib/libcurl.4.dylib %i/lib/libcurl-cms.dylib %i/bin/curl
ln -s libcurl.4.dylib %i/lib/libcurl-cms.dylib
  ;;
esac

# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %{i}/lib/pkgconfig

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Read documentation online.
%define drop_files %{i}/share

%post
%{relocateConfig}bin/curl-config
