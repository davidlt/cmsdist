### RPM cms oracle-env 29
## NOCOMPILER
## INITENV +PATH SQLPATH %{i}/etc
## INITENV SET TNS_ADMIN %{i}/etc

Patch0: oracle-env-online

%prep
# NOP

%build
# NOP

%install
mkdir -p %{i}/etc
cd %{i}/etc
curl -s -S -L -k -o sqlnet.ora http://cvs.web.cern.ch/cvs/cgi-bin/viewcvs.cgi/COMP/PHEDEX/Schema/login.sql?revision=1.2
curl -s -S -L -k -o tnsnames.ora http://cvs.web.cern.ch/cvs/cgi-bin/viewcvs.cgi/COMP/PHEDEX/Schema/tnsnames.ora?revision=1.45
curl -s -S -L -k -o login.sql http://cvs.web.cern.ch/cvs/cgi-bin/viewcvs.cgi/COMP/PHEDEX/Schema/sqlnet.ora?revision=1.1
patch -p0 < %{_sourcedir}/oracle-env-online
