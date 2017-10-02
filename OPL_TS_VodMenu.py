# -*- coding: utf-8 -*-

import unittest

from xmlrunner import XMLTestRunner
from NewTvTesting.Utils import createAndGetXmlDirPath, writeTsSummaryToFiles

from OPL_Testing.TC_3835_T014528 import TC_3835_T014528
from OPL_Testing.TC_3836_T014529 import TC_3836_T014529

if __name__ == '__main__':
    
    suite = unittest.TestSuite()
    
    suite.addTest(TC_3835_T014528("test"))
    suite.addTest(TC_3836_T014529("test"))
    
    runner = XMLTestRunner(createAndGetXmlDirPath())
    result = runner.run(suite)
    writeTsSummaryToFiles(result)
    if not result.wasSuccessful():
        exit(1)
    
    exit()