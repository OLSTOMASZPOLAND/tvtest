#!/bin/bash
#

DIR_APP="/home/tvtest/testEnv/tvtest_OPL/"
DIR_HOME="${DIR_APP}scripts/"
TS_RE_RUN="OPL_TS_re_run_template.py"
FILE_CONFIG="${DIR_APP}config.ini"
FILE_LOG="${DIR_HOME}scriptsLog_$(date '+%Y%m%d').log"

echo "" | tee -a $FILE_LOG
echo "=========== TEST_ENV checkIfTvTestsAreDone.sh started at $(date '+%Y.%m.%d_%H:%M:%S') ===========" | tee -a $FILE_LOG

#check files
if [ ! -e ${DIR_HOME}read_ini.sh ] || [ ! -e $FILE_CONFIG ]
then
	echo "ERROR: Configuration files don't exist, EXIT!" | tee -a $FILE_LOG
	exit 2
fi

if [ ! -n $1 ]; then
	echo "Please provide run logic as a first argument" | tee -a $FILE_LOG
	exit 2
fi

#read environment configuration
. ${DIR_HOME}read_ini.sh
read_ini $FILE_CONFIG

#set variables
DIR_RESULTS="${DIR_APP}${INI__general__report_dir}/"
TS_SUMMARY_REPORT="${DIR_RESULTS}${INI__general__ts_summaryReport}"
TEXT_OUTPUT_FOLDER="${DIR_RESULTS}${INI__general__text_dir}"

#check
if [ -e $TS_SUMMARY_REPORT ]
then
	if [ "$1" == "re_run" ]
	then
		${DIR_HOME}re_run.py $TS_SUMMARY_REPORT >>${FILE_LOG} 2>>${FILE_LOG}
		EXIT_CODE=$?
		if [[ $EXIT_CODE != 0 ]]
		then
		  echo "Cannot start re_run job, quitting" | tee -a $FILE_LOG
		  exit 3
		fi
		rm $TS_SUMMARY_REPORT
		cd $DIR_APP #zeby start byl we wlasciwym miejscu, kwestia dostepnosci plikow
		export DISPLAY=:0.0
		nohup python ${DIR_APP}${TS_RE_RUN} >>${FILE_LOG} 2>>${FILE_LOG} < /dev/null &
		echo "Summary report file found, running re_run." | tee -a $FILE_LOG
		exit 0
	elif [ "$1" == "complete_results" ]
	then
		"${DIR_HOME}complete_results.py" ${TEXT_OUTPUT_FOLDER}  >>${FILE_LOG} 2>>${FILE_LOG}
		EXIT_CODE=$?
		if [[ $EXIT_CODE != 0 ]]
		 then 	 
		 echo "Cannot start complete_results job, quitting" | tee -a $FILE_LOG
		 exit 3
		fi
		echo "Summary report completed." | tee -a $FILE_LOG
		exit 0
	else
		echo "Summary report file found, all tests finished." | tee -a $FILE_LOG
		exit 0
	fi
else
	exit 1
fi
