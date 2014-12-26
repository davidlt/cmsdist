### RPM external file 5.18
## INITENV SET MAGIC %{i}/share/misc/magic.mgc

Source: ftp://ftp.fu-berlin.de/unix/tools/%{n}/%{n}-%{realversion}.tar.gz

%define keep_archives true
%define drop_files %{i}/share/man

%prep
%setup -n %{n}-%{realversion}

%build
./configure --prefix=%{i} --build="%{_build}" --host="%{_host}" \
            --enable-static --disable-shared CFLAGS="-fPIC"
make %{makeprocesses}
