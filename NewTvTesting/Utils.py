# -*- coding: utf-8 -*-
import time
import unittest
import sys

from NewTvTesting.Config import *


def getReportsDirPath():
    return "./" + Env.REPORT_DIR

def createAndGetXmlDirPath():
    if not os.path.exists(getReportsDirPath() + "/" + Env.XML_DIR):
        os.makedirs(getReportsDirPath() + "/" + Env.XML_DIR)

    return getReportsDirPath() + "/" + Env.XML_DIR

def createAndGetTextDirPath():
    if not os.path.exists(getReportsDirPath() + "/" + Env.TEXT_DIR):
        os.makedirs(getReportsDirPath() + "/" + Env.TEXT_DIR)

    return getReportsDirPath() + "/" + Env.TEXT_DIR

def createDirectoriesForReports(testPath):
    if not os.path.exists(getReportsDirPath() + "/" + testPath):
        os.makedirs(getReportsDirPath() + "/" + testPath)

    os.makedirs(getReportsDirPath() + "/" + testPath + "/" + Env.TC_SCREENSHOTS_DIR)
    os.makedirs(getReportsDirPath() + "/" + testPath + "/" + Env.TC_STBLOGS_DIR)

def getTcReportFilePath(testPath):
    return getReportsDirPath() + "/" + testPath + "/" + Env.TC_RUNLOGS_FILE

def generateScreenFilePath(testPath, stepId):
    return getReportsDirPath() + "/" + testPath + "/" + Env.TC_SCREENSHOTS_DIR + "/" + time.strftime("%Y-%m-%d_%H:%M:%S") + "_" + stepId + ".png"

def generateStbLogFilePath(testPath, stepId):
    return getReportsDirPath() + "/" + testPath + "/" + Env.TC_STBLOGS_DIR + "/" + time.strftime("%Y-%m-%d_%H:%M:%S") + "_" + stepId + "_log.html"

def writeStbLogsToFile(stbLogsHtml, filePath):
    with open(filePath, 'w') as f:
        f.write(stbLogsHtml)

def writeLastPageSourceToFile(pageSource, testPath):
    with open(getTcReportFilePath(testPath) + "_pageSourceAfterError.html", 'w') as f:
        f.write(pageSource.encode('utf-8'))

def writeTsSummaryToFiles(result):
    timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
    try:
        suiteName = sys.argv[0].rsplit("/", 1)[1].split(".py")[0]
        report = prepareTsSummaryReport(result, timestamp, suiteName)
    except:
        report = prepareTsSummaryReport(result, timestamp)
    # last
    with open(getReportsDirPath() + "/" + Env.TS_SUMMARY, 'w') as f:
        f.write(report)
    # history
    with open(createAndGetTextDirPath() + "/" + timestamp + "_" + Env.TS_SUMMARY, 'w') as f:
        f.write(report)

def prepareTsSummaryReport(result, timestamp, tsName=None):
    l = []
    l.append("\n")
    l.append("\n")
    l.append("=========== TESTS RUN SUMMARY ===========" + "\n")
    l.append("\n")
    if (tsName is not None):
        l.append("TS filename: " + tsName + "\n")
    l.append("Finished at: " + timestamp + "\n")
    l.append("\n")
    l.append("TOTAL of tests run: %d" % result.testsRun + "\n")
    l.append(" - successes: %d" % len(result.successes) + "\n")
    l.append(" - failures: %d" % len(result.failures) + "\n")
    l.append(" - errors: %d" % len(result.errors) + "\n")
    l.append("\n")
    l.append("----- SUCCESSES -----" + "\n")
    for test_info in result.successes:
        desc = test_info.get_description()
        desc = desc[desc.rindex('.') + 1:-1]
        l.append(desc + " (time: " + timeInSecondsToHumanFriendlyString(test_info.elapsed_time) + ")\n")
    l.append("\n")
    l.append("----- FAILURES -----" + "\n")
    for test_info in result.failures:
        desc = test_info.get_description()
        desc = desc[desc.rindex('.') + 1:-1]
        l.append(desc + " (time: " + timeInSecondsToHumanFriendlyString(test_info.elapsed_time) + ")\n")
    l.append("\n")
    l.append("----- ERRORS -----" + "\n")
    for test_info in result.errors:
        desc = test_info.get_description()
        desc = desc[desc.rindex('.') + 1:-1]
        l.append(desc + " (time: " + timeInSecondsToHumanFriendlyString(test_info.elapsed_time) + ")\n")
    l.append("\n")
    l.append("=========================================" + "\n")
    l.append("\n")
    l.append("\n")
    return ''.join(l)

def timeInSecondsToHumanFriendlyString(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

