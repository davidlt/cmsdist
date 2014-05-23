### RPM external python 2.7.5
## INITENV +PATH PATH %{i}/bin
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib64
## INITENV SETV PYTHON_PLAT_LIB_SITE_PACKAGES lib64/python%{python_major_version}/site-packages
## INITENV SETV PYTHON_PURE_LIB_SITE_PACKAGES lib/python%{python_major_version}/site-packages
## INITENV SETV PYTHONHASHSEED random
# OS X patches and build fudging stolen from fink
%{expand:%%define python_major_version %(echo %realversion | cut -d. -f1,2)}

%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isnotonline %(case %{cmsplatf} in (*onl_*_*) echo 0 ;; (*) echo 1 ;; esac)

Requires: expat bz2lib db6 gdbm openssl libffi

%if %isnotonline
Requires: zlib sqlite readline ncurses
%endif

# FIXME: readline, crypt 
# FIXME: gmp, panel, tk/tcl, x11

Source0: http://www.python.org/ftp/%n/%realversion/Python-%realversion.tgz
Patch1: python-fix-macosx-relocation
Patch2: python-2.7.3-fix-pyport
Patch3: python-2.7.3-ssl-fragment
Patch4: python-2.7.5-lib64-fix-for-test_install
Patch5: python-2.7.5-lib64-sysconfig
Patch6: python-2.7.5-lib64
Patch7: python-2.7.5-dont-detect-dbm
Patch8: python-2.7.5-fix-libffi-paths

%prep
%setup -n Python-%realversion
find . -type f | while read f; do
  if head -n1 $f | grep -q /usr/local; then
    perl -p -i -e "s|#!.*/usr/local/bin/python|#!/usr/bin/env python|" $f
  else :; fi
done
%patch1 -p0

%if %isdarwin
%patch2 -p1
%endif

%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

rm -rf Modules/expat || exit 1
rm -rf Modules/zlib || exit 1
for SUBDIR in darwin libffi libffi_arm_wince libffi_msvc libffi_osx ; do
  rm -rf Modules/_ctypes/$SUBDIR || exit 1 ;
done
for FILE in md5module.c md5.c shamodule.c sha256module.c sha512module.c ; do
  rm -f Modules/$FILE || exit 1
done

%build
# Python is awkward about passing other include or library directories
# to it.  Basically there is no way to pass anything from configure to
# make, or down to python itself.  To get python detect the extensions
# we want to enable, we simply have to link the contents into python's
# own include/lib directories.  Ugh.
#
# NB: It would sort-of make sense to link more stuff from /sw on OS X,
# but we simply cannot link the whole world.  If you need something,
# see above for the commented-out list of packages that could be
# linked specifically, or could be built by ourselves, depending on
# whether we like to pick up system libraries or want total control.
#mkdir -p %i/include %i/lib
mkdir -p %{i}/{include,lib64,bin}

%if %isnotonline
%define extradirs ${ZLIB_ROOT} ${SQLITE_ROOT} ${READLINE_ROOT} ${NCURSES_ROOT}
%else
%define extradirs %{nil}
%endif

dirs="${EXPAT_ROOT} ${BZ2LIB_ROOT} ${DB4_ROOT} ${GDBM_ROOT} ${OPENSSL_ROOT} ${LIBFFI_ROOT} %{extradirs}"

# We need to export it because setup.py now uses it to determine the actual
# location of DB4, this was needed to avoid having it picked up from the system.
export DB4_ROOT
export LIBFFI_ROOT

# Python's configure parses LDFLAGS and CPPFLAGS to look for aditional library and include directories
echo $dirs
LDFLAGS=""
CPPFLAGS=""
for d in $dirs; do
  LDFLAGS="$LDFLAGS -L$d/lib -L$d/lib64"
  CPPFLAGS="$CPPFLAGS -I$d/include"
done
export LDFLAGS
export CPPFLAGS

# Bugfix for dbm package. Use ndbm.h header and gdbm compatibility layer.
sed -ibak "s/ndbm_libs = \[\]/ndbm_libs = ['gdbm', 'gdbm_compat']/" setup.py

sed -ibak "s|LIBFFI_INCLUDEDIR=.*|LIBFFI_INCLUDEDIR=\"${LIBFFI_ROOT}/include\"|g" configure

./configure \
  --prefix=%{i} \
  --libdir=%{i}/lib64 \
  --enable-shared \
  --with-system-ffi \
  --with-system-expat \
  $additionalConfigureOptions

# Modify pyconfig.h to match macros from GLIBC features.h on Linux machines.
# _POSIX_C_SOURCE and _XOPEN_SOURCE macros are not identical anymore
# starting GLIBC 2.10.1. Python.h is not included before standard headers
# in CMSSW and pyconfig.h is not smart enough to detect already defined
# macros on Linux. The following problem does not exists on BSD machines as
# cdefs.h does not define these macros.
case %cmsplatf in
  slc6*|fc*)
    rm -f cms_configtest.cpp
    cat <<CMS_EOF > cms_configtest.cpp
#include <features.h>

int main() {
  return 0;
}
CMS_EOF

    FEATURES=$(g++ -dM -E -DGNU_GCC=1 -D_GNU_SOURCE=1 -D_DARWIN_SOURCE=1 cms_configtest.cpp \
      | grep -E '_POSIX_C_SOURCE |_XOPEN_SOURCE ')
    rm -f cms_configtest.cpp a.out

    POSIX_C_SOURCE=$(echo "${FEATURES}" | grep _POSIX_C_SOURCE | cut -d ' ' -f 3)
    XOPEN_SOURCE=$(echo "${FEATURES}" | grep _XOPEN_SOURCE | cut -d ' ' -f 3)

    sed -ibak "s/\(#define _POSIX_C_SOURCE \)\(.*\)/\1${POSIX_C_SOURCE}/g" pyconfig.h
    sed -ibak "s/\(#define _XOPEN_SOURCE \)\(.*\)/\1${XOPEN_SOURCE}/g" pyconfig.h
  ;;
esac

# Modify pyconfig.h to disable GCC format attribute as it is used incorrectly.
# Triggers an error if -Werror=format is used with GNU GCC 4.8.0+.
sed -ibak "s/\(#define HAVE_ATTRIBUTE_FORMAT_PARSETUPLE .*\)/\/* \1 *\//g" pyconfig.h

make %makeprocesses

%install
# We need to export it because setup.py now uses it to determine the actual
# location of DB4, this was needed to avoid having it picked up from the system.
export DB4_ROOT
export LIBFFI_ROOT
make install
%define pythonv %(echo %realversion | cut -d. -f 1,2)

case %cmsplatf in
  osx*)
   make install prefix=%i 
   (cd Misc; /bin/rm -rf RPM)
   mkdir -p %i/share/doc/%n
   cp -R Demo Doc %i/share/doc/%n
   cp -R Misc Tools %i/lib64/python%{pythonv}
   gcc -dynamiclib -all_load -single_module \
    -framework System -framework CoreServices -framework Foundation \
    %i/lib64/python%{pythonv}/config/libpython%{pythonv}.a \
    -undefined dynamic_lookup \
    -o %i/lib64/python%{pythonv}/config/libpython%{pythonv}.dylib \
    -install_name %i/lib64/python%{pythonv}/config/libpython%{pythonv}.dylib \
    -current_version %{pythonv} -compatibility_version %{pythonv} -ldl
   (cd %i/lib64/python%{pythonv}/config
    perl -p -i -e 's|-fno-common||g' Makefile)

   find %i/lib64/python%{pythonv}/config -name 'libpython*' -exec mv -f {} %i/lib64 \;
  ;;
esac

 perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/idle \
                     %{i}/bin/pydoc \
                     %{i}/bin/python-config \
                     %{i}/bin/2to3 \
                     %{i}/bin/python2.7-config \
                     %{i}/bin/smtpd.py

find %{i}/lib64 -maxdepth 1 -mindepth 1 ! -name '*python*' -exec rm {} \;
find %{i}/include -maxdepth 1 -mindepth 1 ! -name '*python*' -exec rm {} \;

# remove executable permission anything which is *.py script,
# is executable, but does not start with she-bang so not valid
# executable; this avoids problems with rpm 4.8+ find-requires
find %i -name '*.py' -perm +0111 | while read f; do
  if head -n1 $f | grep -q '"'; then chmod -x $f; else :; fi
done

# remove tkinter that brings dependency on libtk:
find %{i}/lib64 -type f -name "_tkinter.so" -exec rm {} \;

# Remove documentation, examples and test files. 
%define drop_files { %i/share %{i}/lib64/python%{pythonv}/test \
                   %{i}/lib64/python%{pythonv}/distutils/tests \
                   %{i}/lib64/python%{pythonv}/json/tests \
                   %{i}/lib64/python%{pythonv}/ctypes/test \
                   %{i}/lib64/python%{pythonv}/sqlite3/test \
                   %{i}/lib64/python%{pythonv}/bsddb/test \
                   %{i}/lib64/python%{pythonv}/email/test \
                   %{i}/lib64/python%{pythonv}/lib2to3/tests \
                   %{i}/lib64/pkgconfig }

# Remove .pyo files
find %i -name '*.pyo' -exec rm {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}lib64/python2.7/config/Makefile
%{relocateConfig}lib64/python2.7/_sysconfigdata.py
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
