### RPM external gccxml 0.9.0-20131116-0

BuildRequires: cmake

%define commit b040a46352e4d5c11a0304e4fcb6f7842008942a
Source: git+https://github.com/gccxml/gccxml.git?obj=master/%{commit}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tar.gz

%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%prep
%setup -n %{n}-%{realversion}

# Update to get AArch64
rm -f ./GCC/config.{sub,guess}
curl -L -k -s -o ./GCC/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./GCC/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./GCC/config.{sub,guess}

%if %isdarwin
# Drop no more supported -no-cpp-precomp on Darwin.
sed -i '' 's/-no-cpp-precomp//g' \
  GCC/CMakeLists.txt \
  GCC/configure.in \
  GCC/configure
%endif

%build
mkdir gccxml-build
cd gccxml-build
cmake .. \
   -DCMAKE_INSTALL_PREFIX:PATH=%{i}
make %makeprocesses

%install
cd gccxml-build
make install

%define drop_files %i/share/{man,doc}

%post
%{relocateConfig}share/gccxml-0.9/gccxml_config
