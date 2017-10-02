# -*- coding: utf-8 -*-
import unittest
from xmlrunner import XMLTestRunner
from NewTvTesting.Utils import createAndGetXmlDirPath, writeTsSummaryToFiles
from OPL_Testing.Pawel_Endurance_Test import pawel_endurance_test

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(pawel_endurance_test("test"))
    
    

    runner = XMLTestRunner(createAndGetXmlDirPath())
    result = runner.run(suite)
    writeTsSummaryToFiles(result)
    if not result.wasSuccessful():
        exit(1)
    
    exit()

