#!/usr/bin/python

import os
import re
from sys import argv

class TestResult(object):
    def __init__(self, path):  # sciezka do katalogu TextOutput
        self.path = path
        self.reportFiles = []
        self.successes = {}
        self.errors = {}
        self.failures = {}
        self.dateFinished = ""
        self.TSname = ""

        dirs = os.listdir(path)
        self.runs_number = len(dirs)
        for f in dirs:
            if not "~" in f:
                self.reportFiles.append(path + "/" + f)

        if len(self.reportFiles) == 0:
            print "Report files not found!"
            exit(1)

        self.reportFiles.sort()

    def generate_report(self):
        reportNumber = 0
        for i in range(len(self.reportFiles)):
            reportNumber += 1
            with open(self.reportFiles[i], "r") as f:
                data = f.read()
                successes = data[data.index("----- SUCCESSES -----") + len("----- SUCCESSES -----"):data.index("----- FAILURES -----")]
                result = re.findall("(TC_\d.*)\s\((.*)\)", successes)
                for TC in result:
                    self.successes[TC[0]] = [TC[1], reportNumber]

                if i == 0:
                    try:
                        self.TSname = re.findall("TS filename:.*", data)[0]
                    except:
                        pass

                if i == len(self.reportFiles) - 1:
                    failures = data[data.index("----- FAILURES -----") + len("----- FAILURES -----"):data.index("----- ERRORS -----")]
                    result = re.findall("(TC_\d.*)\s\((.*)\)", failures)
                    for TC in result:
                        self.failures[TC[0]] = [TC[1], self.runs_number]
                    errors = data[data.index("----- ERRORS -----") + len("----- ERRORS -----"):data.index("=========================================")]
                    result = re.findall("(TC_\d.*)\s\((.*)\)", errors)
                    for TC in result:
                        self.errors[TC[0]] = [TC[1], self.runs_number]
                    self.dateFinished = re.findall("Finished at:.*", data)[0]

    def save_report(self):
        report = "\n\n=========== TESTS RUN SUMMARY ===========\n" + self.TSname + "\n" + self.dateFinished + "\nNumber of runs: " + str(self.runs_number)
        report += "\nTOTAL of tests run: " + str(len(self.successes) + len(self.errors) \
                                         + len(self.failures))
        report += "\n - successes: %i\n - failures: %i\n - errors: %i\n" % \
                    (len(self.successes), len(self.failures), len(self.errors))

        report += "\n----- SUCCESSES -----\n"

        for i in self.successes:
            report += i + " (" + self.successes[i][0] + ", runs: " + str(self.successes[i][1]) + ")\n"

        report += "\n----- FAILURES -----\n"

        for i in self.failures:
            report += i + " (" + self.failures[i][0] + ", runs: " + str(self.failures[i][1]) + ")\n"

        report += "\n----- ERRORS -----\n"

        for i in self.errors:
            report += i + " (" + self.errors[i][0] + ", runs: " + str(self.errors[i][1]) + ")\n"

        report += "\n========================================="

        with open(self.path.rsplit("/", 1)[0] + "/summaryReport.log", "w") as f:
            f.write(report)

        print "Summary raport created..."

if __name__ == '__main__':

    if len(argv) == 1:
        print "Please provide path to TextOutput folder as a first argument!"
        exit(1)
    a = TestResult(argv[1])
    a.generate_report()
    a.save_report()
    exit(0)
