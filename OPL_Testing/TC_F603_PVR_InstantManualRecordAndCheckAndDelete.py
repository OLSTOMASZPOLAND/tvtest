# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta


class TC_F603_PVR_InstantManualRecordAndCheckAndDelete(TC_OPL_template):
    """Implementation of the HP QC test ID - 9711 - T016358_Schedule an instant record - manually recording; check record during recording; finally delete record
    
    @author: Leszek Wawrzonkowski
    """
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        recordLength = PvrData.LENGTH_2
        recordName = "tc-f603"
        
        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")
        
        ''' step '''
        self.logStepBeginning("STEP - check conditions before start")
        #step logic
        self.assertTrue(self.page.waitForPvrNoCurrentAndScheduledRecords())
        self.logStepResults("STEP - check conditions before start")
        
        ''' step '''
        self.logStepBeginning("STEP - start recording "+recordName)
        #step logic
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_GREEN"])
        time.sleep(2)
        recordStartDate = self.page.getClock()
        self.assertTrue(type(recordStartDate) is datetime, "  >>   ERR: wrong record data")
        self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "  >>   ERR: problem selecting >" + Menu.pvrManualRecord + "<")
        time.sleep(2)
        idOne = self.page.actionScheduleRecord(1, recordStartDate, recordLength, name=recordName)
        self.assertTrue(idOne != False, "  >>   ERR: problem during scheduling record")
        self.logStepResults("STEP - start recording "+recordName)
        
        ''' step '''
        self.logStepBeginning("STEP - check is it not in my records scheduled just after recording has started")
        #step logic
        self.assertTrue(self.page.goToPvrMyScheduled(shouldBeEmpty=True))
        self.logStepResults("STEP - check is it not in my records scheduled just after recording has started")
        
        ''' step '''
        self.logStepBeginning("STEP - check is it in my records mosaic just after recording has started")
        #step logic
        self.assertTrue(self.page.goToPvrMyRecords())
        #details check
        self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(recordName, recordName, True, recordStartDate, maxMinutesDiff=2))
        self.logStepResults("STEP - check is it in my records mosaic just after recording has started")
        
        ''' step '''
        self.logStepBeginning("STEP - check details of the record item just after recording has started")
        #step logic
        self.rc.sendKeys(["KEY_OK"])
        #details check
        self.assertTrue(self.page.verifyPvrOnRecordScreen(recordName, recordName, True, recordStartDate, recordLength, csaClass=None, maxMinutesDiff=2))
        self.logStepResults("STEP - check details of the record item just after recording has started")
        
        ''' step '''
        self.logStepBeginning("STEP - check record motion at a half of record length")
        #step logic
        time.sleep(int(recordLength*60/2))
        self.assertTrue(self.page.goToPvrMyRecords())
        self.rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=10))
        self.logStepResults("STEP - check record motion at a half of record length")
        
        ''' step '''
        self.logStepBeginning("STEP - check my records mosaic after recording")
        #step logic
        time.sleep(int(recordLength*60/2))
        self.assertTrue(self.page.goToPvrMyRecords())
        #details check
        self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(recordName, recordName, False, recordStartDate, maxMinutesDiff=2))
        self.logStepResults("STEP - check my records mosaic after recording")
        
        ''' step '''
        self.logStepBeginning("STEP - check details of the record item after recording")
        #step logic
        self.rc.sendKeys(["KEY_OK"])
        #details check
        self.assertTrue(self.page.verifyPvrOnRecordScreen(recordName, recordName, False, recordStartDate, recordLength, csaClass=None, maxMinutesDiff=2))
        #play check
        self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=10))
        self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=recordLength*60/2))
        self.logStepResults("STEP - check details of the record item after recording")
        
        ''' step '''
        self.logStepBeginning("STEP - delete record")
        #step logic
        self.assertTrue(self.page.deletePvrRecord())
        self.logStepResults("STEP - delete record")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")