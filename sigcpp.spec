### RPM external sigcpp 2.3.1
%define majorv %(echo %realversion | cut -d. -f1,2) 
Source: http://ftp.gnome.org/pub/GNOME/sources/libsigc++/%{majorv}/libsigc++-%{realversion}.tar.xz

BuildRequires: autotools

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++ -std=c++0x
%endif

%prep
%setup -q -n libsigc++-%{realversion}

# Update to get AArch64
rm -f ./build/config.{sub,guess}
curl -L -k -s -o ./build/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./build/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./build/config.{sub,guess}

./configure --prefix=%{i} --disable-static CXX="%cms_cxx"

%build
make %makeprocesses 
%install
make install
# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config 
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %i/lib/pkgconfig
# Read documentation online.
%define drop_files %i/share
cp %i/lib/sigc++-2.0/include/sigc++config.h %i/include/sigc++-2.0/
