### RPM external fastjet 3.0.3
Source: http://www.lpthe.jussieu.fr/~salam/fastjet/repo/%n-%realversion.tar.gz
Patch1: fastjet-3.0.3-nobanner
Patch2: fastjet-3.0.1-siscone-banner
Patch3: fastjet-3.0.1-noemptyareawarning
Patch4: fastjet-3.0.1-nodegeneracywarning
Patch5: fastjet-3.0.1-cluster-sequence-banner
Patch6: fastjet-3.0.1-silence-warnings

%prep
%setup -n %n-%realversion
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# Update for AArch64 support
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

rm -f ./plugins/SISCone/siscone/config.{sub,guess}
curl -L -k -s -o ./plugins/SISCone/siscone/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./plugins/SISCone/siscone/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./plugins/SISCone/siscone/config.{sub,guess}

case %{cmsplatf} in
    *_amd64_*) CXXFLAGS="-O3 -Wall -ffast-math -std=c++11 -msse3 -ftree-vectorize" ;;
    *) CXXFLAGS="-O3 -Wall -ffast-math -std=c++11 -ftree-vectorize" ;;
esac


./configure --enable-shared  --enable-atlascone --enable-cmsiterativecone --enable-siscone --prefix=%i --enable-allcxxplugins ${CXXFLAGS+CXXFLAGS="$CXXFLAGS"}

%build
make %makeprocesses

%install
make install
rm -rf %i/lib/*.la
%post
%{relocateConfig}bin/fastjet-config
