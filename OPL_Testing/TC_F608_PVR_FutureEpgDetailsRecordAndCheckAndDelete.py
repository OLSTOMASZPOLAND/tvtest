# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta


class TC_F608_PVR_FutureEpgDetailsRecordAndCheckAndDelete(TC_OPL_template):
    """Implementation of the HP QC test ID - 9728 - T016360_Schedule a record - EPG programming; Schedule Future recording from EPG - Record menu item on EPG details screen; check record during recording; finally delete record
    
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
        #choose program in the future
        countProgramMaxSearch = 10
        programFound = False
        for x in range(0, countProgramMaxSearch):
            self.rc.sendKeys(["KEY_RIGHT"])
            time.sleep(5)
            currentProgramInfo = self.page.getInfoFromEpgFocus()
            self.assertTrue(type(currentProgramInfo) is ProgramInfoItem, "  >>   ERR: EPG info - wrong record data")
            self.assertFalse(type(currentProgramInfo.getStart()) is None, "  >>   ERR: EPG info - start date is not set")
            self.assertFalse(type(currentProgramInfo.getClock()) is None, "  >>   ERR: EPG info - clock is not set")
            #not recording and start at least ten minutes from now
            if (not currentProgramInfo.getRecording()) and (currentProgramInfo.getStart() > currentProgramInfo.getClock()+timedelta(minutes = 10)):
                programFound = True
                break
        self.assertTrue(programFound, "  >>   ERR: program in the future doesn't found")
        self.rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.actionSelect(Menu.epgRecord), "  >>   ERR: problem selecting >" + Menu.epgRecord + "<")
        time.sleep(5)
        self.rc.sendKeys(["KEY_DOWN"]) #no margin after record - TODO maybe to API function with choice in ResidentAppPage
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(10) #wait until confirmation POPUP hide
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(3)
        currentProgramInfo = self.page.getInfoFromEpgFocus()
        self.assertTrue(type(currentProgramInfo) is ProgramInfoItem, "  >>   ERR: EPG info - wrong record data")
        self.assertFalse(type(currentProgramInfo.getStart()) is None, "  >>   ERR: EPG info - start date is not set")
        self.assertFalse(type(currentProgramInfo.getLength()) is None, "  >>   ERR: EPG info - length is not set")
        self.assertFalse(type(currentProgramInfo.getClock()) is None, "  >>   ERR: EPG info - clock is not set")
        self.assertTrue(currentProgramInfo.getRecording(), "  >>   ERR: problem checking is recording")
        self.logStepResults("STEP - start recording")
        
        ''' step '''
        self.logStepBeginning("STEP - check is it in my records scheduled just after scheduling")
        #step logic
        self.assertTrue(self.page.goToPvrMyScheduled())
        self.assertTrue(self.page.verifyPvrOnSchedulingMosaic(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), currentProgramInfo.getStart(), maxMinutesDiff=0))
        self.logStepResults("STEP - check is it in my records scheduled just after scheduling")
        
        ''' step '''
        self.logStepBeginning("STEP - check details of the record item just after scheduling")
        #step logic
        self.rc.sendKeys(["KEY_OK"])
        #details check
        self.assertTrue(self.page.verifyPvrOnRecordScreen(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getStart(), int(currentProgramInfo.getLength().seconds/60), csaClass=None, maxMinutesDiff=0))
        self.logStepResults("STEP - check details of the record item just after scheduling")
        
        ''' step '''
        self.logStepBeginning("STEP - check is it not in my records mosaic just after scheduling")
        #step logic
        #if my records mosaic is not empty
        if not self.page.goToPvrMyRecords(shouldBeEmpty=True):
            #the first record should be different than just scheduled
            self.assertFalse(self.page.verifyPvrOnMyRecordsMosaic(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getStart(), maxMinutesDiff=0))
        self.logStepResults("STEP - check is it not in my records mosaic just after scheduling")
        
        ''' step '''
        self.logStepBeginning("STEP - check is it not in my records scheduled just after recording has started")
        #step logic
        #wait until record will start
        currentDate = self.page.getClock()
        self.assertTrue(type(currentDate) is datetime, "  >>   ERR: wrong record data")
        time.sleep((currentProgramInfo.getStart() - currentDate).total_seconds())
        #check
        self.assertTrue(self.page.goToPvrMyScheduled(shouldBeEmpty=True))
        self.logStepResults("STEP - check is it not in my records scheduled just after recording has started")
        
        ''' step '''
        self.logStepBeginning("STEP - check is it in my records mosaic just after recording has started")
        #step logic
        self.assertTrue(self.page.goToPvrMyRecords())
        #details check
        self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), True, currentProgramInfo.getStart(), maxMinutesDiff=0))
        self.logStepResults("STEP - check is it in my records mosaic just after recording has started")
        
        ''' step '''
        self.logStepBeginning("STEP - check details of the record item just after recording has started")
        #step logic
        self.rc.sendKeys(["KEY_OK"])
        #details check
        self.assertTrue(self.page.verifyPvrOnRecordScreen(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), True, currentProgramInfo.getStart(), int(currentProgramInfo.getLength().seconds/60), csaClass=None, maxMinutesDiff=0))
        self.logStepResults("STEP - check details of the record item just after recording has started")
        
        ''' step '''
        self.logStepBeginning("STEP - check record motion at a half of record length")
        #step logic
        time.sleep(int(currentProgramInfo.getLength().seconds/2))
        self.assertTrue(self.page.goToPvrMyRecords())
        self.rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=10))
        self.logStepResults("STEP - check record motion at a half of record length")
        
        ''' step '''
        self.logStepBeginning("STEP - check my records mosaic after recording")
        #step logic
        time.sleep(int(currentProgramInfo.getLength().seconds/2))
        self.assertTrue(self.page.goToPvrMyRecords())
        #details check
        self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getStart(), maxMinutesDiff=0))
        self.logStepResults("STEP - check my records mosaic after recording")
        
        ''' step '''
        self.logStepBeginning("STEP - check details of the record item after recording")
        #step logic
        self.rc.sendKeys(["KEY_OK"])
        #details check
        self.assertTrue(self.page.verifyPvrOnRecordScreen(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getStart(), int(currentProgramInfo.getLength().seconds/60), csaClass=None, maxMinutesDiff=0))
        #play check
        self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=10))
        self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=currentProgramInfo.getLength().seconds/2))
        self.logStepResults("STEP - check details of the record item after recording")
        
        ''' step '''
        self.logStepBeginning("STEP - delete record")
        #step logic
        self.assertTrue(self.page.deletePvrRecord())
        self.logStepResults("STEP - delete record")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")