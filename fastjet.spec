### RPM external fastjet 3.1.0
%define tag b22035e7b44afb596fce6d393139b59b8bb00d47
%define branch cms/v%realversion
%define github_user cms-externals
Source: git+https://github.com/%github_user/fastjet.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%prep
%setup -n %n-%realversion

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
