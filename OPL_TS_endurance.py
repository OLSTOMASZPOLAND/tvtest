# -*- coding: utf-8 -*-

import unittest

from xmlrunner import XMLTestRunner
from NewTvTesting.Utils import createAndGetXmlDirPath, writeTsSummaryToFiles

from OPL_Testing.TC_E701_ParentalControlAndVodMenu import TC_E701_ParentalControlAndVodMenu
from OPL_Testing.TC_0000_Unitary_zapping_test import TC_0000_Unitary_zapping_test
from OPL_Testing.TC_0000_endurance_epg_with_power_off import TC_0000_endurance_with_power_off

if __name__ == '__main__':

    suite = unittest.TestSuite()

    ''' add the TC list below '''
    # suite.addTest(TC_E701_ParentalControlAndVodMenu("test"))
    suite.addTest(TC_0000_endurance_with_power_off("test"))

    runner = XMLTestRunner(createAndGetXmlDirPath())
    result = runner.run(suite)
    writeTsSummaryToFiles(result)
    if not result.wasSuccessful():
        exit(1)

    exit()
