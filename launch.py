from multiprocessing import Pool, TimeoutError
import multiprocessing as mp
from Queue import Queue
from threading import Thread
import threading
import subprocess
import time
import os,subprocess,sys

#input directory for the files to be analyzed
directory = "/dpm/in2p3.fr/home/cms/phedex/store/user/ccollard/HSCP/prodOct2019_CMSSW_10_6_2/SingleMuon/"
#list of periods corresponding to subdirectories in directory
periods = ["run2017B","run2017C","run2017D","run2017E","run2017F","run2018A","run2018B","run2018C","run2018D"]
#assume a structur like this directory/period/subdir/subsubdir/files_id.root
#periods = ["run2017B"]
#Name of the script description the job to be launch
# contents 3 keywords that will be replaced
#   PEDIOD correspond to the periods above mentioned
#   LABEL  typically the integer of the first files ran
#   FILES  list of files to be analyzed
TemplateScript = "template.sh"
#abolute path to the script for submission
SubmitScript = "/home-pbs/echabert/HSCP/launch/submit.sh"
#number of files ran in a single job
NFilesPerJob = 5


for period in periods:
	cdir = directory+period
	command =  ["rfdir",cdir] 
	process = subprocess.Popen(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	#first first subdir
	subdir = stdout.split()[8]
	cdir +="/"+subdir
	command =  ["rfdir",cdir] 
	process = subprocess.Popen(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	#first subsubdir
	subdir = stdout.split()[8]
	print(stdout)
	cdir +="/"+subdir
	#directory has been updated
	#find all files
	command =  ["rfdir",cdir] #,"|","awk","'{print $9}'"]
	process = subprocess.Popen(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	#split per line
	listFiles = stdout.split('\n')
	#print(listFiles)
	#search for the name (9th and last element in a line)
	listFiles = [e.split()[8] for e in listFiles if len(e.split())==9]
	print(listFiles)

	print("In directory",cdir,"\t nof files = ",len(listFiles))
	
	pairFiles = []
	count = 1
	gcount = 1
	idForJob = 1
	sfilesForJob = ""
	for f in listFiles:
		idfile = f.split("_")[3].split(".")[0]
		if count == 1: 
			idForJob = idfile
			sfilesForJob = ""
		#print(idfile)
    		fullfilename = "root://sbgse1.in2p3.fr:/"+cdir+"/"+f
		#print(idfile,fullfilename)
		sfilesForJob+=" "+fullfilename
		count+=1
		gcount+=1
		if count==(NFilesPerJob+1) or gcount==len(listFiles):
			#Ready !!
			shfile = open(TemplateScript)
			content = shfile.read()
			#replace the keywords by the values
			content = content.replace("PERIOD",period)
			content = content.replace("FILES",sfilesForJob)
			content = content.replace("LABEL",idForJob)
			#write content in a file
			ofilename = "jobs/job_"+period+"_"+idForJob+".sh"
			ofile = open(ofilename,"w")
			ofile.write(content)
			ofile.close()
			#ready to launch the job
			command = ["source "+SubmitScript+" "+ofilename+" "+period+"_"+idForJob+" "+sfilesForJob]
			print(command)
			#subprocess.check_call(command)
			process = subprocess.Popen(command,shell=True)
			#process = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			#stdout, stderr = process.communicate()
			#print(stdout,stderr)

			count = 1

