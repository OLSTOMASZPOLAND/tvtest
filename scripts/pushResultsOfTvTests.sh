#!/bin/bash
#

DIR_APP="/home/tvtest/testEnv/tvtest_OPL/"
DIR_HOME="${DIR_APP}scripts/"
FILE_CONFIG="${DIR_APP}config.ini"
FILE_LOG="${DIR_HOME}scriptsLog_$(date '+%Y%m%d').log"

echo "" | tee -a $FILE_LOG
echo "=========== TEST_ENV pushResultsOfTvTests.sh started at $(date '+%Y.%m.%d_%H:%M:%S') ===========" | tee -a $FILE_LOG

#WARNING: before first run the SSH session should be established manually to accept keys, managing server should be configured to use keys authentication and proper keys should be shared !!!
#managing host configuration
MANAGE_HOST="antonio.is-very-bad.org"
MANAGE_PORT="2001"
MANAGE_USER="tvtest"
MANAGE_DIR="/home/tvtest/test_run_reports/"

#check files
if [ ! -e ${DIR_HOME}read_ini.sh ] || [ ! -e $FILE_CONFIG ]
then
	echo "ERROR: Configuration files don't exist, EXIT!" | tee -a $FILE_LOG
	exit 2
fi

#the repository branch
cd $DIR_APP
GIT_BRANCH=`git status | head -n1 | awk -F' ' '{print $3}'`

#environment name
ENV_NAME=""
if [ -n "$1" ]
then
	ENV_NAME=$1
else
	echo "ERROR: ENV NAME doesn't passed, EXIT!" | tee -a $FILE_LOG
	exit 2
fi
ENV_NAME=`echo $ENV_NAME | awk '{print toupper($0)}'`

#read environment configuration
. ${DIR_HOME}read_ini.sh
read_ini $FILE_CONFIG

#set variables
echo "Environment settings:" | tee -a $FILE_LOG
DIR_RESULTS="${DIR_APP}${INI__general__report_dir}/"
echo "- reports directory: $DIR_RESULTS" | tee -a $FILE_LOG
TS_SUMMARY_REPORT="${DIR_RESULTS}${INI__general__ts_summaryReport}"
echo "- expected summary report file: $TS_SUMMARY_REPORT" | tee -a $FILE_LOG
RA_VER="${INI__stb_environment__ra_version}"
echo "- resident application version: $RA_VER" | tee -a $FILE_LOG
FW_VER="${INI__stb_environment__fw_version}"
echo "- firmware version: $FW_VER" | tee -a $FILE_LOG
LO_VER="${INI__stb_environment__lo_version}"
echo "- loader version: $LO_VER" | tee -a $FILE_LOG
ZONE="${INI__stb_environment__zone}"
echo "- zone: $ZONE" | tee -a $FILE_LOG
STB_MODEL="${INI__stb_environment__stb_model}"
echo "- STB model: $STB_MODEL" | tee -a $FILE_LOG
CPE_MODEL="${INI__stb_environment__cpe_model}"
echo "- CPE model: $CPE_MODEL" | tee -a $FILE_LOG
CONNECTION="${INI__stb_environment__connection}"
echo "- CPE model: $CONNECTION" | tee -a $FILE_LOG

echo "- Environment name: $ENV_NAME" | tee -a $FILE_LOG

echo "- The repository branch name: $GIT_BRANCH" | tee -a $FILE_LOG

ENV_PATH="${ENV_NAME}_${GIT_BRANCH}_${RA_VER}_${FW_VER}_${LO_VER}_${ZONE}_${STB_MODEL}_${CPE_MODEL}_${CONNECTION}"

echo "Sending reports generated for test configuration: ${ENV_PATH}" | tee -a $FILE_LOG

cd $DIR_RESULTS

ssh -p ${MANAGE_PORT} ${MANAGE_USER}@${MANAGE_HOST} 1>>${FILE_LOG} 2>>${FILE_LOG} << SSH_END
cd ${MANAGE_DIR}
if [ ! -d ${ENV_PATH} ]
then
mkdir -p ${ENV_PATH}
rm ${ENV_NAME}_LAST
ln -s ${ENV_PATH} ${ENV_NAME}_LAST
fi
exit
SSH_END

scp -v -P ${MANAGE_PORT} -r * ${MANAGE_USER}@${MANAGE_HOST}:${MANAGE_DIR}${ENV_PATH} 1>>${FILE_LOG} 2>>${FILE_LOG}

#print summary to the standard output
echo ""
echo "`cat ${TS_SUMMARY_REPORT}`"
echo ""

exit 0
