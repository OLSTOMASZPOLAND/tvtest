# -*- coding: utf-8 -*-

import unittest

from xmlrunner import XMLTestRunner
from NewTvTesting.Utils import createAndGetXmlDirPath, writeTsSummaryToFiles

from OPL_Testing.TC_9798_T000000_Auto_Display_and_Use_Zapping_Banner import TC_9798_T000000_Auto_Display_and_Use_Zapping_Banner
from OPL_Testing.TC_3368_T014506_consult_prepaid_account import TC_3368_T014506_consult_prepaid_account
from OPL_Testing.TC_9470_T014339_Zap_to_basic_channel import TC_9470_T014339_Zap_to_basic_channel

if __name__ == '__main__':
    
    suite = unittest.TestSuite()
    
    ''' add the TC list below '''
    suite.addTest(TC_9470_T014339_Zap_to_basic_channel("test"))
    suite.addTest(TC_9470_T014339_Zap_to_basic_channel("test"))
    suite.addTest(TC_9470_T014339_Zap_to_basic_channel("test"))


    
    runner = XMLTestRunner(createAndGetXmlDirPath())
    result = runner.run(suite)
    writeTsSummaryToFiles(result)
    if not result.wasSuccessful():
        exit(1)
    
    exit()