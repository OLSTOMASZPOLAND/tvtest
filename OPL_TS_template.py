# -*- coding: utf-8 -*-

import unittest

from xmlrunner import XMLTestRunner
from NewTvTesting.Utils import createAndGetXmlDirPath, writeTsSummaryToFiles

from OPL_Testing.TC_0000_T999999 import TC_0000_T999999

if __name__ == '__main__':
    
    suite = unittest.TestSuite()
    
    ''' add the TC list below '''

    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))
    suite.addTest(TC_0000_T999999("test"))



    runner = XMLTestRunner(createAndGetXmlDirPath())
    result = runner.run(suite)
    writeTsSummaryToFiles(result)
    if not result.wasSuccessful():
        exit(1)
    
    exit()
