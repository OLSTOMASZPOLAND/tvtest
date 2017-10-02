# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_F601_PVR_InstantLiveRecordAndCheckAndDelete(TC_OPL_template):
    """Implementation of the HP QC test ID - 9713 - T016935_Launch Instant recording_Record key on Live program; check record during recording; finally delete record
    
    @author: Leszek Wawrzonkowski
    """
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        recordLength = PvrData.LENGTH_2
        
        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")
        
        ''' step '''
        self.logStepBeginning("STEP - check conditions before start")
        #step logic
        self.assertTrue(self.page.waitForPvrNoCurrentAndScheduledRecords())
        self.logStepResults("STEP - check conditions before start")
        
        ''' step '''
        self.logStepBeginning("STEP - start recording")
        #step logic
        self.assertTrue(self.page.goToLiveByCsaCategory())
        self.rc.sendKeys(["KEY_INFO"])
        currentProgramInfo = self.page.getInfoFromLiveBanner()
        self.assertTrue(type(currentProgramInfo) is ProgramInfoItem, "  >>   ERR: wrong record data")
        self.rc.sendKeys(["KEY_RECORD"])
        time.sleep(10)
        self.page.actionInstantRecord(recordLength) #record length in DataSet configuration
        self.logStepResults("STEP - start recording")
        
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
        self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), True, currentProgramInfo.getClock()))
        self.logStepResults("STEP - check is it in my records mosaic just after recording has started")
        
        ''' step '''
        self.logStepBeginning("STEP - check details of the record item just after recording has started")
        #step logic
        self.rc.sendKeys(["KEY_OK"])
        #details check
        self.assertTrue(self.page.verifyPvrOnRecordScreen(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), True, currentProgramInfo.getClock(), recordLength, csaClass=currentProgramInfo.getCsaClass()))
        self.logStepResults("STEP - check details of the record item just after recording has started")
        
        ''' step '''
        self.logStepBeginning("STEP - check tv channel and record motion at a half of record length")
        #step logic
        time.sleep(int(recordLength*60/2))
        self.rc.sendKeys(["KEY_TV"])
        if Env.VIDEO:
            self.logger.debug("  >>   motionDetection")
            self.assertTrue(motionDetection(), "  >>   ERR: problem checking motionDetection")
        self.assertTrue(self.page.goToPvrMyRecords())
        self.rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=10))
        self.logStepResults("STEP - check tv channel and record motion at a half of record length")
        
        ''' step '''
        self.logStepBeginning("STEP - check my records mosaic after recording")
        #step logic
        time.sleep(int(recordLength*60/2))
        self.assertTrue(self.page.goToPvrMyRecords())
        #details check
        self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock()))
        self.logStepResults("STEP - check my records mosaic after recording")
        
        ''' step '''
        self.logStepBeginning("STEP - check details of the record item after recording")
        #step logic
        self.rc.sendKeys(["KEY_OK"])
        #details check
        self.assertTrue(self.page.verifyPvrOnRecordScreen(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock(), recordLength, csaClass=currentProgramInfo.getCsaClass()))
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