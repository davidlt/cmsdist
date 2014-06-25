### RPM cms cmssw-dictdb CMSSW_7_2_X_2014-06-18-1400

Source: http://davidlt.web.cern.ch/davidlt/dictdb/%{realversion}/allditcs.zip

# Below are example instructions for generating alldicts.zip on x86_64
# for corresponding CMSSW version.

# export SCRAM_ARCH=slc6_amd64_gcc490
# scram p CMSSW_7_2_X_2014-06-18-1400
# cd CMSSW_7_2_X_2014-06-18-1400
# eval $(scram r -sh)
# rm -rf src
# cp -r -L $CMSSW_RELEASE_BASE/src .
# scram b -v -j $(getconf _NPROCESSORS_ONLN) precompile 2>&1 | tee b.log
# cd tmp/$SCRAM_ARCH
# find src -name '*.cc'  | zip -@ allditcs
# mv allditcs.zip ../..
# cd ../..
# cat <EOF > do.py
# import re
# import json
# from os.path import dirname
# from os import environ, getcwd
# 
# if __name__ == '__main__':
#   header_file = None
#   selection_file = None
#   dict_file = None
#   cap_file = None
#   dict_db = {}
#   with open('b.log') as build_log:
#     for line in build_log:
#       if 'bin/genreflex' in line:
#         args = re.split('[\s=]', line.strip())
#         header_file = args[1]
#         selection_file = args[3]
#         dict_file = args[args.index('-o') + 1].replace('tmp/{0}/'.format(environ['SCRAM_ARCH']), '')
#         cap_file = args[args.index('--capabilities') + 1].replace('tmp/{0}/'.format(environ['SCRAM_ARCH']), '')
#         cap_file = "{0}/{1}".format(dirname(dict_file), cap_file)
#         dict_db[header_file] = [selection_file, dict_file, cap_file]
#       if 'bin/rootcint' in line:
#         args = re.split('[\s=]', line.strip())
#         header_file = args[-1].replace('{0}/'.format(getcwd()), '')
#         dict_file = args[args.index('-f') + 1].replace('tmp/{0}/'.format(environ['SCRAM_ARCH']), '')
#         dict_db[header_file] = [dict_file]
#   print(json.dumps(dict_db, sort_keys=True, indent=4))
# EOF
# python do.py > db.json
# zip -g allditcs.zip db.json
# unzip -l allditcs.zip

%prep

%build

%install
mkdir -p %{i}/share/%{n}
cp %{SOURCE0} %{i}/share/%{n}
