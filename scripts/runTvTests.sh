#!/bin/bash
#

DIR_APP="/home/tvtest/testEnv/tvtest_OPL/"
DIR_HOME="${DIR_APP}scripts/"
FILE_CONFIG="${DIR_APP}config.ini"
FILE_LOG="${DIR_HOME}scriptsLog_$(date '+%Y%m%d').log"

echo "" | tee -a $FILE_LOG
echo "=========== TEST_ENV runTvTests.sh started at $(date '+%Y.%m.%d_%H:%M:%S') ===========" | tee -a $FILE_LOG

#check files
if [ ! -e ${DIR_HOME}read_ini.sh ] || [ ! -e $FILE_CONFIG ]
then
	echo "ERROR: Configuration files don't exist, EXIT!" | tee -a $FILE_LOG
	exit 2
fi

#read environment configuration
. ${DIR_HOME}read_ini.sh
read_ini $FILE_CONFIG

cd $DIR_APP

echo "Synchronization with the repository:" | tee -a $FILE_LOG

#change the repository branch
GIT_BRANCH="develop"
if [ -n "$1" ]
then
	GIT_BRANCH=$1
else
	echo "WARNIG: The repository branch name doesn't passed, changing to default: $GIT_BRANCH" | tee -a $FILE_LOG
fi
if ! git checkout $GIT_BRANCH 2>>${FILE_LOG}
then
	echo "ERROR: Problem during changing the repository branch to $GIT_BRANCH occurred, EXIT!" | tee -a $FILE_LOG
	exit 2
fi

#synchronize with the repository
if ! git pull 2>>${FILE_LOG}
then
	echo "ERROR: Problem during synchronization with the repository occurred, EXIT!" | tee -a $FILE_LOG
	exit 2
fi

#set TS file
TS_FILENAME="OPL_TS_template.py"
if [ -n "$2" ]
then
	TS_FILENAME=$2
else
	echo "WARNIG: TS file doesn't passed, starting default: $TS_FILENAME" | tee -a $FILE_LOG
fi
#check TS file
if [ ! -e ${DIR_APP}$TS_FILENAME ] 
then
	echo "ERROR: TS file ${TS_FILENAME} doesn't exist, EXIT!" | tee -a $FILE_LOG
	exit 2
fi

#set variables
echo "Environment settings:" | tee -a $FILE_LOG
DIR_RESULTS="${DIR_APP}${INI__general__report_dir}/"
echo "- reports directory: $DIR_RESULTS" | tee -a $FILE_LOG
echo "- chosen TS: ${TS_FILENAME}" | tee -a $FILE_LOG
TS_SUMMARY_REPORT="${DIR_RESULTS}${INI__general__ts_summaryReport}"
echo "- expected summary report file: $TS_SUMMARY_REPORT" | tee -a $FILE_LOG
DIR_RESULTS_XML="${DIR_RESULTS}${INI__general__xml_dir}/"
echo "- expected XML directory: $DIR_RESULTS_XML" | tee -a $FILE_LOG
DIR_RESULTS_TEXT="${DIR_RESULTS}${INI__general__text_dir}/"
echo "- expected TEXT directory: $DIR_RESULTS_TEXT" | tee -a $FILE_LOG

#clean CAREFULLY the results catalog (cleaning depends on config.ini so it's easy to clean something else....)
echo "Cleaning actions before run:" | tee -a $FILE_LOG
if [ -e $TS_SUMMARY_REPORT ]
then
	echo "- removing old summary report file" | tee -a $FILE_LOG
	rm $TS_SUMMARY_REPORT
fi
if [ -e $DIR_RESULTS_XML ]
then
	echo "- removing old XML directory and TC directories" | tee -a $FILE_LOG #uruchomienie TS tworzy katalog XML wiec jesli go nie ma to nie bezpieczenie jest kasowac katalogi TC
	rm -rf $DIR_RESULTS_XML
	rm -rf ${DIR_RESULTS}TC_*
fi
if [ -e $DIR_RESULTS_TEXT ]
then
	echo "- removing old TEXT directory" | tee -a $FILE_LOG
	rm -rf $DIR_RESULTS_TEXT
fi

#starting TS
cd $DIR_APP #zeby start byl we wlasciwym miejscu, kwestia dostepnosci plikow
export DISPLAY=:0.0
nohup python ${DIR_APP}${TS_FILENAME} >>${FILE_LOG} 2>>${FILE_LOG} < /dev/null &

echo "TS ${DIR_APP}${TS_FILENAME} started at $(date '+%Y.%m.%d_%H:%M:%S')" | tee -a $FILE_LOG
echo "" | tee -a $FILE_LOG

exit 0

