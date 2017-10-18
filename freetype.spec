### RPM external freetype 2.5.3
Source: http://download.savannah.gnu.org/releases/freetype/freetype-%{realversion}.tar.bz2
Requires: bz2lib zlib libpng

Patch0: a

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
./configure \
  --prefix %{i} \
  --with-bzip2==${BZ2LIB_ROOT} \
  --with-zlib=${ZLIB_ROOT} \
  --with-png=${LIBPNG_ROOT} \
  --with-harfbuzz=no

make %{makeprocesses}

%install
make install
%ifos darwin
install_name_tool -id %{i}/lib/libfreetype-cms.dylib -change %{i}/lib/libfreetype.6.dylib %{i}/lib/libfreetype-cms.dylib %{i}/lib/libfreetype.6.dylib
ln -s libfreetype.6.dylib %{i}/lib/libfreetype-cms.dylib
perl -p -i -e 's|-lfreetype|-lfreetype-cms|' %{i}/bin/freetype-config
%endif

echo "DEBUG_PATH: ${ZLIB_ROOT}"
sed -ibak "s;\(my_magic_path=\)\(.*\);\1${ZLIB_ROOT};g" %{i}/bin/freetype-config

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
%post
%{relocateConfig}bin/freetype-config
