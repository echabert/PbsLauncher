#PBS -u echabert
#!/bin/bash
#./submit.sh script.sh jobid
# script.sh is the job to be ran on the cluster
# jobid is a label (period_id)

echo $PWD

if [  "$#" -ne 3 ]; then
  echo "Script submit.sh"
  echo " -- goal:  	use to launch executable on pbs "
  echo " -- usage: 	./submit.sh script.sh jobid"
  echo "    scripts.sh: job to be ran"
  echo "    jobid:	label (ex: period_id)"
  exit
fi



export HOME="/home-pbs/echabert/HSCP/"
export X509_USER_PROXY="$PWD/proxy/x509up_u7737"
que="sbg_local_mdm"
output="$PWD/logs/${2}.out"
error="$PWD/logs/${2}.err"
qsub -q  ${que}  -o ${output} -e ${error} ${1}
