### RPM external file-bootstrap 5.15
## INITENV SET MAGIC %{i}/share/misc/magic.mgc

Source: ftp://ftp.fu-berlin.de/unix/tools/file/file-%{realversion}.tar.gz

BuildRequires: autotools

%define keep_archives true
%define drop_files %{i}/share/man

%prep  
%setup -n file-%{realversion}

%build

case %{cmsplatf} in
  *_aarch64_* )
    # Rerun autoconf to get support for AArch64
    autoreconf -fiv
  ;;
esac

./configure --prefix=%{i} --build="%{_build}" --host="%{_host}" \
            --enable-static --disable-shared CFLAGS="-fPIC"
make %{makeprocesses}
