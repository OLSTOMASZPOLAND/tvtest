# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta


class TC_F605_PVR_InstantEpgRecordAndCheckAndDelete(TC_OPL_template):
    """Launch Instant recording from EPG - Record key on EPG mosaic; check record during recording; finally delete record
    
    @author: Leszek Wawrzonkowski
    """
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
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
        self.rc.sendKeys(["KEY_GUIDE"])
        self.assertTrue(self.page.actionSelect(Menu.epgWeek), "  >>   ERR: problem selecting >" + Menu.epgWeek + "<")
        currentProgramInfo = self.page.getInfoFromEpgFocus()
        self.assertTrue(type(currentProgramInfo) is ProgramInfoItem, "  >>   ERR: EPG info - wrong record data")
        self.assertFalse(type(currentProgramInfo.getStart()) is None, "  >>   ERR: EPG info - start date is not set")
        self.assertFalse(type(currentProgramInfo.getLength()) is None, "  >>   ERR: EPG info - length is not set")
        self.assertFalse(type(currentProgramInfo.getClock()) is None, "  >>   ERR: EPG info - clock is not set")
        self.assertFalse(currentProgramInfo.getRecording(), "  >>   ERR: problem checking is recording")
        self.rc.sendKeys(["KEY_RECORD"])
        time.sleep(5)
        self.rc.sendKeys(["KEY_OK"])
        currentProgramInfo = self.page.getInfoFromEpgFocus()
        self.assertTrue(type(currentProgramInfo) is ProgramInfoItem, "  >>   ERR: EPG info - wrong record data")
        self.assertFalse(type(currentProgramInfo.getStart()) is None, "  >>   ERR: EPG info - start date is not set")
        self.assertFalse(type(currentProgramInfo.getLength()) is None, "  >>   ERR: EPG info - length is not set")
        self.assertFalse(type(currentProgramInfo.getClock()) is None, "  >>   ERR: EPG info - clock is not set")
        self.assertTrue(currentProgramInfo.getRecording(), "  >>   ERR: problem checking is recording")
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
        recordDetails = self.page.getInfoFromRecordPage()
        self.assertTrue(type(recordDetails) is RecordDetailedItem, "  >>   ERR: wrong record data")
        #check the end date - should be not earlier then program end
        if not (currentProgramInfo.getStart()+currentProgramInfo.getLength() <= recordDetails.getDate()+recordDetails.getLength()):
            self.assertTrue(False, "  >>   ERR: record length to short")
        #the rest of details check
        self.assertTrue(self.page.verifyPvrOnRecordScreen(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), True, currentProgramInfo.getClock(), int(recordDetails.getLength().seconds/60), csaClass=currentProgramInfo.getCsaClass()))
        self.logStepResults("STEP - check details of the record item just after recording has started")
        
        ''' step '''
        self.logStepBeginning("STEP - check tv channel and record motion at a half of record length")
        #step logic
        time.sleep(int(recordDetails.getLength().seconds/2))
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
        time.sleep(int(recordDetails.getLength().seconds/2))
        self.assertTrue(self.page.goToPvrMyRecords())
        #details check
        self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock()))
        self.logStepResults("STEP - check my records mosaic after recording")
        
        ''' step '''
        self.logStepBeginning("STEP - check details of the record item after recording")
        #step logic
        self.rc.sendKeys(["KEY_OK"])
        #details check
        self.assertTrue(self.page.verifyPvrOnRecordScreen(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock(), int(recordDetails.getLength().seconds/60), csaClass=currentProgramInfo.getCsaClass()))
        #play check
        self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=10))
        self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=recordDetails.getLength().seconds/2))
        self.logStepResults("STEP - check details of the record item after recording")
        
        ''' step '''
        self.logStepBeginning("STEP - delete record")
        #step logic
        self.assertTrue(self.page.deletePvrRecord())
        self.logStepResults("STEP - delete record")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")