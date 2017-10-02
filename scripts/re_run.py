#!/usr/bin/python

import re
from sys import argv

class TestResult(object):
    def __init__(self, path):  # sciezka do pliku summaryReport.log
        self.path = path
        self.errors = {}
        self.failures = {}

    def generate_report(self):
        with open(self.path, "r") as f:
            data = f.read()
            failures = data[data.index("----- FAILURES -----") + len("----- FAILURES -----"):data.index("----- ERRORS -----")]
            result = re.findall("(TC_\d.*)\s(\(.*)", failures)
            for TC in result:
                self.failures[TC[0]] = TC[1]
            errors = data[data.index("----- ERRORS -----") + len("----- ERRORS -----"):data.index("=========================================")]
            result = re.findall("(TC_\d.*)\s(\(.*)", errors)
            for TC in result:
                self.errors[TC[0]] = TC[1]

    def save_template(self):
        result = "# -*- coding: utf-8 -*-\nimport unittest\n" + \
                    "from xmlrunner import XMLTestRunner\n" + \
                    "from NewTvTesting.Utils import createAndGetXmlDirPath, writeTsSummaryToFiles\n"

        for i in self.errors:
            result += "\nfrom OPL_Testing." + i + " import " + i

        for i in self.failures:
            result += "\nfrom OPL_Testing." + i + " import " + i

        result += "\nif __name__ == '__main__':\n\tsuite = unittest.TestSuite()\n\t" + \
                    "\n\t''' add the TC list below '''\n"

        for i in self.errors:
            result += "\tsuite.addTest(" + i + "('test'))\n"

        for i in self.failures:
            result += "\tsuite.addTest(" + i + "('test'))\n"

        result += "\trunner = XMLTestRunner(createAndGetXmlDirPath())\n" + \
                 "\tresult = runner.run(suite)\n" + \
                 "\twriteTsSummaryToFiles(result)\n" + \
                 "\tif not result.wasSuccessful():\n" + \
                 "\t\texit(1)\n\n" + \
                 "\texit()"
        with open(self.path.rsplit("/", 2)[0] + "/OPL_TS_re_run_template.py", "w") as f:
            f.write(result)            
        
        print "Saving new re_run_template to: " + self.path.rsplit("/", 2)[0] + "/OPL_TS_re_run_template.py"

if __name__ == '__main__':

    if len(argv) == 1:
        print "Please provide path to summaryReport.log file as a first argument"
        exit(1)
    a = TestResult(argv[1])
    a.generate_report()
    a.save_template()
    exit(0)

