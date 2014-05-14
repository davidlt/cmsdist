### RPM external qd 2.3.13
Source: http://crd.lbl.gov/~dhbailey/mpdist/qd-%{realversion}.tar.gz

%prep
%setup -n qd-%{realversion}

# Update to get AArch64
rm -f ./config/config.{sub,guess}
curl -L -k -s -o ./config/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config/config.{sub,guess}

./configure --prefix=%i --enable-shared 
# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
%build
make %{makeprocesses}
%install
make install
