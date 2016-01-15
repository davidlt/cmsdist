### RPM external starlight r193

%define tag 36d8af7c6bb23b209e6c9bb40f3df543f85cb214
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: clhep

BuildRequires:	cmake

Patch0: star-fix

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
rm -rf ../build
mkdir ../build
cd ../build

export CLHEPDIR=${CLHEP_ROOT}

cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DCMAKE_BUILD_TYPE=Release \
  -DENABLE_CLHEP=ON

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1

rm -rf %{i}/lib/archive
