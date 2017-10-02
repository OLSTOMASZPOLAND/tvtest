# -*- coding: utf-8 -*-
import unittest
from xmlrunner import XMLTestRunner
from NewTvTesting.Utils import createAndGetXmlDirPath, writeTsSummaryToFiles
# from OPL_Testing.Pawel_Endurance_Test import pawel_endurance_test
from OPL_Testing.pawel_endurance_test_with_epg import pawel_endurance_test_with_epg

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(pawel_endurance_test_with_epg("test"))
    
    

    runner = XMLTestRunner(createAndGetXmlDirPath())
    result = runner.run(suite)
    writeTsSummaryToFiles(result)
    if not result.wasSuccessful():
        exit(1)
    
    exit()

