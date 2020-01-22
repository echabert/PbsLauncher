# PbsLauncher


 - Before launching jobs on pbs
   - launch the proxy command voms-proxy-init -voms cms -hours 48 
   - copy the proxy-file (ex: /tmp/x509up_u7737) in proxy/
 - Usage:
   - Modify the file template.sh if needed
      - change the variables (workdir, X509_USER_PROXY, EXECUTABLE,  outdir)
      - three modes: 
        - compile: 	to compile the code on the cluster environement (only 1 pilot job)
	- debug:	test on a file
	- run: 		default mode (run the program)
   - Modify the file launch.py if needed
   /home-pbs/echabert/HSCP/launch/submit.sh
     -  variables related to the input files (directory and periods)
     -  TemplateScript = "template.sh"
     -  SubmitScript = "/home-pbs/echabert/HSCP/launch/submit.sh"
     -  NFilesPerJob = 5

