# -*- coding: utf-8 -*-

import unittest

from xmlrunner import XMLTestRunner
from NewTvTesting.Utils import createAndGetXmlDirPath, writeTsSummaryToFiles

from OPL_Testing.TC_3343_T014474_VOD import TC_3343_T014474_VOD
from OPL_Testing.TC_3343_T014474_PVR import TC_3343_T014474_PVR
from OPL_Testing.TC_3343_T014474_LIVE import TC_3343_T014474_LIVE
from OPL_Testing.TC_3345_T014476_VOD import TC_3345_T014476_VOD
from OPL_Testing.TC_3345_T014476_PVR import TC_3345_T014476_PVR
from OPL_Testing.TC_3345_T014476_LIVE import TC_3345_T014476_LIVE
from OPL_Testing.TC_3346_T014477_VOD import TC_3346_T014477_VOD
from OPL_Testing.TC_3346_T014477_PVR import TC_3346_T014477_PVR
from OPL_Testing.TC_3346_T014477_LIVE import TC_3346_T014477_LIVE
from OPL_Testing.TC_3347_T014478 import TC_3347_T014478
from OPL_Testing.TC_3348_T014479_VOD import TC_3348_T014479_VOD
from OPL_Testing.TC_3348_T014479_PVR import TC_3348_T014479_PVR
from OPL_Testing.TC_3348_T014479_LIVE import TC_3348_T014479_LIVE

if __name__ == '__main__':
    
    suite = unittest.TestSuite()
    
    suite.addTest(TC_3343_T014474_VOD("test"))
    suite.addTest(TC_3343_T014474_PVR("test"))
    suite.addTest(TC_3343_T014474_LIVE("test"))
    suite.addTest(TC_3345_T014476_VOD("test"))
    suite.addTest(TC_3345_T014476_PVR("test"))
    suite.addTest(TC_3345_T014476_LIVE("test"))
    suite.addTest(TC_3346_T014477_VOD("test"))
    suite.addTest(TC_3346_T014477_PVR("test"))
    suite.addTest(TC_3346_T014477_LIVE("test"))
    suite.addTest(TC_3347_T014478("test"))
    suite.addTest(TC_3348_T014479_VOD("test"))
    suite.addTest(TC_3348_T014479_PVR("test"))
    suite.addTest(TC_3348_T014479_LIVE("test"))
    
    runner = XMLTestRunner(createAndGetXmlDirPath())
    result = runner.run(suite)
    writeTsSummaryToFiles(result)
    if not result.wasSuccessful():
        exit(1)
    
    exit()