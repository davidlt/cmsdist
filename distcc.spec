### RPM external distcc 3.2rc1
Source: https://distcc.googlecode.com/files/distcc-%realversion.tar.gz
Requires: python

%prep
%setup -n %n-%realversion
%build
# Update to get AArch64
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

CFLAGS="-O2 -Wno-unused-but-set-variable"
case %cmsplatf in
  *gcc4[89]*)
    CFLAGS="$CFLAGS -Wno-unused-local-typedefs -Wno-unused-parameter"
    ;;
esac
./configure \
  --prefix %{i} \
  --without-gtk \
  --without-gnome \
  --without-avahi \
  CFLAGS="$CFLAGS" \
  CC="$(which gcc)" \
  PYTHON=$PYTHON_ROOT/bin/python
make %makeprocesses
%install
make install
ln -sf distcc %i/bin/c++
ln -sf distcc %i/bin/cc
ln -sf distcc %i/bin/gcc
ln -sf distcc %i/bin/gfortran
%post
%{relocateConfig}bin/pump
