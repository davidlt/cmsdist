### RPM external xz 5.0.3__5.1.2alpha
%define generic_version 5.0.3
%define fcarm_version 5.1.2alpha
Source0: http://tukaani.org/%{n}/%{n}-%{generic_version}.tar.gz
Source1: http://tukaani.org/%{n}/%{n}-%{fcarm_version}.tar.gz

%define isfcarm %(case %{cmsplatf} in (fc*_arm*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%if %isfcarm
%setup -b 1 -n %{n}-%{fcarm_version}
%else
%setup -b 0 -n %{n}-%{generic_version}
%endif

%build
# Update for AArch64 support
rm -f ./build-aux/config.{sub,guess}
curl -L -k -s -o ./build-aux/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./build-aux/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'

./configure CFLAGS='-fPIC -Ofast' --prefix=%{i} --disable-static
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
