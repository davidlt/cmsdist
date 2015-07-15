### RPM external tbb 43_20150424oss
Source: https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/%{n}%{realversion}_src.tgz

Patch0: tbb43_20150424oss.clang.use.__sync_

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -n tbb%{realversion}
%patch0 -p1

%build

CXX="%cms_cxx" CXXFLAGS="%cms_cxxflags" make %makeprocesses

%install
install -d %i/lib
cp -r include %i/include
case %cmsplatf in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac
find build -name "*.$SONAME*" -exec cp {} %i/lib \; 
