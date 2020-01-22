#! /bin/bash
echo 'Starting Job' 
export V0_CMS_SW_DIR=/cvmfs/cms.cern.ch/
source $V0_CMS_SW_DIR/cmsset_default.sh
export workdir="/home-pbs/echabert/HSCP/"
export X509_USER_PROXY="/home-pbs/echabert/HSCP/launch/proxy/x509up_u7737"
export EXECUTABLE="testAnalysis/csvMaker.exe"
export outdir="/dpm/in2p3.fr/home/cms/phedex/store/user/echabert/HSCP/CSVFiles/"
alias cmsenv='eval `scramv1 runtime -sh`'

debug=false
compile=false
run=true

#CMS env
cd $workdir/CMSSW_10_3_4/src/
eval `scramv1 runtime -sh`

#info about the machine OS
uname -a

#setup env
cd $workdir/HSCP
source setup.sh

if $compile ; then
  make clean
  make folders
  make -j 4
  #Used to recompile the code on the plateform
  g++ `root-config --glibs --cflags` -L lib -lHSCP testAnalysis/csvMaker.cpp  -o testAnalysis/csvMaker.exe
fi


if $debug ; then 
   ./${EXECUTABLE} period 1 root://sbgse1.in2p3.fr://dpm/in2p3.fr/home/cms/phedex/store/user/ccollard/HSCP/prodOct2019_CMSSW_10_6_2/SingleMuon/run2017B/191023_141349/0000/nt_data_aod_96.root
done

#launch execuctabl
if $run ; then
  ./${EXECUTABLE} PERIOD LABEL FILES
done



#copy outputs

rfdir $outdir
rfcp PERIOD_LABEL.csv $outdir 
rm PERIOD_LABEL.csv

#cleaning

echo 'Completed Job' 
