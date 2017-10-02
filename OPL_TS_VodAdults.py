# -*- coding: utf-8 -*-

import unittest

from xmlrunner import XMLTestRunner
from NewTvTesting.Utils import createAndGetXmlDirPath, writeTsSummaryToFiles

from OPL_Testing.TC_3816_T014443 import TC_3816_T014443
from OPL_Testing.TC_3817_T014444 import TC_3817_T014444
from OPL_Testing.TC_3824_T014495 import TC_3824_T014495
from OPL_Testing.TC_3825_T014501 import TC_3825_T014501
from OPL_Testing.TC_3862_T015590 import TC_3862_T015590
from OPL_Testing.TC_3865_T015595 import TC_3865_T015595
from OPL_Testing.TC_3866_T015596 import TC_3866_T015596
from OPL_Testing.TC_10700_Txxxxxx import TC_10700_Txxxxxx

if __name__ == '__main__':
    
    suite = unittest.TestSuite()
    suite.addTest(TC_3816_T014443("test"))
    suite.addTest(TC_3817_T014444("test"))
    suite.addTest(TC_3824_T014495("test"))
    suite.addTest(TC_3825_T014501("test"))
    suite.addTest(TC_3862_T015590("test"))
    suite.addTest(TC_3865_T015595("test"))
    suite.addTest(TC_3866_T015596("test"))
    suite.addTest(TC_10700_Txxxxxx("test"))
    
    runner = XMLTestRunner(createAndGetXmlDirPath())
    result = runner.run(suite)
    writeTsSummaryToFiles(result)
    if not result.wasSuccessful():
        exit(1)
    
    exit()