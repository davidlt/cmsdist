### RPM external frontier_client 2.8.5
Source: http://frontier.cern.ch/dist/%{n}__%{realversion}__src.tar.gz
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

Requires: expat
Requires: openssl
%if "%online" != "true"
Requires: zlib
%else
Requires: onlinesystemtools
%endif

Patch0: frontier_client-2.8.5-fix-gcc47

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

%prep
%setup -n %{n}__%{realversion}__src

%if "%online" != "true"
%define makeargs "EXPAT_DIR=$EXPAT_ROOT COMPILER_TAG=gcc_%{gccver} ZLIB_DIR=$ZLIB_ROOT  OPENSSL_DIR=$OPENSSL_ROOT"
%else
%define makeargs "EXPAT_DIR=$EXPAT_ROOT COMPILER_TAG=gcc_%{gccver}"
%endif

%patch0 -p1

%build

export MAKE_ARGS=%{makeargs}
make $MAKE_ARGS CXXFLAGS="%cms_cxxflags"

%install
mkdir -p %i/lib
mkdir -p %i/include
export MAKE_ARGS=%{makeargs}
make $MAKE_ARGS distdir=%i dist

case $(uname) in 
  Darwin ) 
    so=dylib 
    ln -sf libfrontier_client.%{realversion}.$so %i/lib/libfrontier_client.$so
    ln -sf libfrontier_client.$so.%{realversion} %i/libfrontier_client.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/").$so
    ;; 
  * ) 
    so=so 
    ln -sf libfrontier_client.$so.%{realversion} %i/lib/libfrontier_client.$so
    ln -sf libfrontier_client.$so.%{realversion} %i/lib/libfrontier_client.$so.%(echo %v | sed -e "s/\([0-9]*\)\..*/\1/")
    ;; 
esac
