### RPM cms cmssw-dictdb-toolfile 1.0
Requires: cmssw-dictdb
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE > %{i}/etc/scram.d/root_dictcache.xml
<tool name="root_dictcache" version="@TOOL_VERSION@">
  <client>
    <environment name="CMSSW_DICTDB_BASE" default="@TOOL_ROOT@"/>
  </client>
  <runtime name="CMSSW_DICTDB_PATH" value="$CMSSW_DICTDB_BASE/share/cmssw-dictdb/allditcs.zip" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
