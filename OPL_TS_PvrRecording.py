# -*- coding: utf-8 -*-

import unittest

from xmlrunner import XMLTestRunner
from NewTvTesting.Utils import createAndGetXmlDirPath, writeTsSummaryToFiles

from OPL_Testing.TC_F601_PVR_InstantLiveRecordAndCheckAndDelete import TC_F601_PVR_InstantLiveRecordAndCheckAndDelete
from OPL_Testing.TC_F602_PVR_InstantLiveRecordAndCheckAllCsaSamples import TC_F602_PVR_InstantLiveRecordAndCheckAllCsaSamples
from OPL_Testing.TC_F603_PVR_InstantManualRecordAndCheckAndDelete import TC_F603_PVR_InstantManualRecordAndCheckAndDelete
from OPL_Testing.TC_F604_PVR_FutureManualRecordAndCheckAndDelete import TC_F604_PVR_FutureManualRecordAndCheckAndDelete
from OPL_Testing.TC_F605_PVR_InstantEpgRecordAndCheckAndDelete import TC_F605_PVR_InstantEpgRecordAndCheckAndDelete
from OPL_Testing.TC_F606_PVR_InstantEpgDetailsRecordAndCheckAndDelete import TC_F606_PVR_InstantEpgDetailsRecordAndCheckAndDelete
from OPL_Testing.TC_F607_PVR_FutureEpgRecordAndCheckAndDelete import TC_F607_PVR_FutureEpgRecordAndCheckAndDelete
from OPL_Testing.TC_F608_PVR_FutureEpgDetailsRecordAndCheckAndDelete import TC_F608_PVR_FutureEpgDetailsRecordAndCheckAndDelete

if __name__ == '__main__':
    
    suite = unittest.TestSuite()
    
    suite.addTest(TC_F601_PVR_InstantLiveRecordAndCheckAndDelete("test"))
    suite.addTest(TC_F603_PVR_InstantManualRecordAndCheckAndDelete("test"))
    suite.addTest(TC_F604_PVR_FutureManualRecordAndCheckAndDelete("test"))
    suite.addTest(TC_F605_PVR_InstantEpgRecordAndCheckAndDelete("test"))
    suite.addTest(TC_F606_PVR_InstantEpgDetailsRecordAndCheckAndDelete("test"))
    suite.addTest(TC_F607_PVR_FutureEpgRecordAndCheckAndDelete("test"))
    suite.addTest(TC_F608_PVR_FutureEpgDetailsRecordAndCheckAndDelete("test"))
    
    #suite.addTest(TC_F602_PVR_InstantLiveRecordAndCheckAllCsaSamples("test"))
    
    runner = XMLTestRunner(createAndGetXmlDirPath())
    result = runner.run(suite)
    writeTsSummaryToFiles(result)
    if not result.wasSuccessful():
        exit(1)
    
    exit()