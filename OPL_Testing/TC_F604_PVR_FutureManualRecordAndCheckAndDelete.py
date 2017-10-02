# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta


class TC_F604_PVR_FutureManualRecordAndCheckAndDelete(TC_OPL_template):
    """Implementation of the HP QC test ID - 9727 - T016359_Schedule a future record - manually recording; check record during recording; finally delete record
    
    @author: Leszek Wawrzonkowski
    """
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        recordLength = PvrData.LENGTH_2
        recordName = "tc-f604"
        recordDelayFromNow = PvrData.LENGTH_1
        
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
        recordStartDate = recordStartDate + timedelta(minutes = recordDelayFromNow)
        self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "  >>   ERR: problem selecting >" + Menu.pvrManualRecord + "<")
        time.sleep(2)
        idOne = self.page.actionScheduleRecord(1, recordStartDate, recordLength, name=recordName)
        self.assertTrue(idOne != False, "  >>   ERR: problem during scheduling record")
        self.logStepResults("STEP - start recording "+recordName)
        
        ''' step '''
        self.logStepBeginning("STEP - check is it in my records scheduled just after scheduling")
        #step logic
        self.assertTrue(self.page.goToPvrMyScheduled())
        self.assertTrue(self.page.verifyPvrOnSchedulingMosaic(recordName, recordName, recordStartDate, maxMinutesDiff=0))
        self.logStepResults("STEP - check is it in my records scheduled just after scheduling")
        
        ''' step '''
        self.logStepBeginning("STEP - check details of the record item just after scheduling")
        #step logic
        self.rc.sendKeys(["KEY_OK"])
        #details check
        self.assertTrue(self.page.verifyPvrOnRecordScreen(recordName, recordName, False, recordStartDate, recordLength, csaClass=None, maxMinutesDiff=0))
        self.logStepResults("STEP - check details of the record item just after scheduling")
        
        ''' step '''
        self.logStepBeginning("STEP - check is it not in my records mosaic just after scheduling")
        #step logic
        #if my records mosaic is not empty
        if not self.page.goToPvrMyRecords(shouldBeEmpty=True):
            #the first record should be different than just scheduled
            self.assertFalse(self.page.verifyPvrOnMyRecordsMosaic(recordName, recordName, False, recordStartDate, maxMinutesDiff=0))
        self.logStepResults("STEP - check is it not in my records mosaic just after scheduling")
        
        ''' step '''
        self.logStepBeginning("STEP - check is it not in my records scheduled just after recording has started")
        #step logic
        #wait until record will start
        currentDate = self.page.getClock()
        self.assertTrue(type(currentDate) is datetime, "  >>   ERR: wrong record data")
        time.sleep((recordStartDate - currentDate).total_seconds())
        #check
        self.assertTrue(self.page.goToPvrMyScheduled(shouldBeEmpty=True))
        self.logStepResults("STEP - check is it not in my records scheduled just after recording has started")
        
        ''' step '''
        self.logStepBeginning("STEP - check is it in my records mosaic just after recording has started")
        #step logic
        self.assertTrue(self.page.goToPvrMyRecords())
        #details check
        self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(recordName, recordName, True, recordStartDate, maxMinutesDiff=0))
        self.logStepResults("STEP - check is it in my records mosaic just after recording has started")
        
        ''' step '''
        self.logStepBeginning("STEP - check details of the record item just after recording has started")
        #step logic
        self.rc.sendKeys(["KEY_OK"])
        #details check
        self.assertTrue(self.page.verifyPvrOnRecordScreen(recordName, recordName, True, recordStartDate, recordLength, csaClass=None, maxMinutesDiff=0))
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
        self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(recordName, recordName, False, recordStartDate, maxMinutesDiff=0))
        self.logStepResults("STEP - check my records mosaic after recording")
        
        ''' step '''
        self.logStepBeginning("STEP - check details of the record item after recording")
        #step logic
        self.rc.sendKeys(["KEY_OK"])
        #details check
        self.assertTrue(self.page.verifyPvrOnRecordScreen(recordName, recordName, False, recordStartDate, recordLength, csaClass=None, maxMinutesDiff=0))
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