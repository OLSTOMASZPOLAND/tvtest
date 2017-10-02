# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_F602_PVR_InstantLiveRecordAndCheckAllCsaSamples(TC_OPL_template):
    """Record all CSA samples for Parental Control PVR tests
    
    @author: Leszek Wawrzonkowski
    """
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")
            
            recordLength = PvrData.LENGTH_1
            
            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            
            ''' step '''
            self.logStepBeginning("STEP - check conditions before start")
            #step logic
            self.assertTrue(self.page.waitForPvrNoCurrentAndScheduledRecords())
            self.logStepResults("STEP - check conditions before start")
            
            ''' step '''
            self.logStepBeginning("STEP - set no parental control")
            self.assertTrue(self.page.setParentalControl(ParentalControl.SetDeactive))
            self.logStepResults("STEP - set no parental control")
            
            ''' step '''
            self.logStepBeginning("STEP - start recording CSA1")
            #step logic
            self.assertTrue(self.page.goToLiveByCsaCategory(csaCat=ParentalControl.CssClassCsa1))
            self.rc.sendKeys(["KEY_INFO"])
            currentProgramInfo = self.page.getInfoFromLiveBanner()
            self.assertTrue(type(currentProgramInfo) is ProgramInfoItem, "  >>   ERR: wrong record data")
            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(10)
            self.page.actionInstantRecord(recordLength) #record length in DataSet configuration
            time.sleep(10)
            self.logStepResults("STEP - start recording CSA1")
            
            time.sleep(int(recordLength*60))
            
            ''' step '''
            self.logStepBeginning("STEP - check my records mosaic and details of the record after recording CSA1")
            #step logic
            self.assertTrue(self.page.goToPvrMyRecords())
            self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock()))
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.verifyPvrOnRecordScreen(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock(), recordLength, currentProgramInfo.getCsaClass()))
            self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=10))
            self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=recordLength*60/2))
            self.logStepResults("STEP - check my records mosaic and details of the record after recording CSA1")
            
            ''' step '''
            self.logStepBeginning("STEP - start recording CSA2")
            #step logic
            self.assertTrue(self.page.goToLiveByCsaCategory(csaCat=ParentalControl.CssClassCsa2))
            self.rc.sendKeys(["KEY_INFO"])
            currentProgramInfo = self.page.getInfoFromLiveBanner()
            self.assertTrue(type(currentProgramInfo) is ProgramInfoItem, "  >>   ERR: wrong record data")
            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(10)
            self.page.actionInstantRecord(recordLength) #record length in DataSet configuration
            time.sleep(10)
            self.logStepResults("STEP - start recording CSA2")
            
            time.sleep(int(recordLength*60))
            
            ''' step '''
            self.logStepBeginning("STEP - check my records mosaic and details of the record after recording CSA2")
            #step logic
            self.assertTrue(self.page.goToPvrMyRecords())
            self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock()))
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.verifyPvrOnRecordScreen(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock(), recordLength, currentProgramInfo.getCsaClass()))
            self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=10))
            self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=recordLength*60/2))
            self.logStepResults("STEP - check my records mosaic and details of the record after recording CSA2")
            
            ''' step '''
            self.logStepBeginning("STEP - start recording CSA3")
            #step logic
            self.assertTrue(self.page.goToLiveByCsaCategory(csaCat=ParentalControl.CssClassCsa3))
            self.rc.sendKeys(["KEY_INFO"])
            currentProgramInfo = self.page.getInfoFromLiveBanner()
            self.assertTrue(type(currentProgramInfo) is ProgramInfoItem, "  >>   ERR: wrong record data")
            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(10)
            self.page.actionInstantRecord(recordLength) #record length in DataSet configuration
            time.sleep(10)
            self.logStepResults("STEP - start recording CSA3")
            
            time.sleep(int(recordLength*60))
            
            ''' step '''
            self.logStepBeginning("STEP - check my records mosaic and details of the record after recording CSA3")
            #step logic
            self.assertTrue(self.page.goToPvrMyRecords())
            self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock()))
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.verifyPvrOnRecordScreen(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock(), recordLength, currentProgramInfo.getCsaClass()))
            self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=10))
            self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=recordLength*60/2))
            self.logStepResults("STEP - check my records mosaic and details of the record after recording CSA3")
            
            ''' step '''
            self.logStepBeginning("STEP - start recording CSA4")
            #step logic
            self.assertTrue(self.page.goToLiveByCsaCategory(csaCat=ParentalControl.CssClassCsa4))
            self.rc.sendKeys(["KEY_INFO"])
            currentProgramInfo = self.page.getInfoFromLiveBanner()
            self.assertTrue(type(currentProgramInfo) is ProgramInfoItem, "  >>   ERR: wrong record data")
            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(10)
            self.page.actionInstantRecord(recordLength) #record length in DataSet configuration
            time.sleep(10)
            self.logStepResults("STEP - start recording CSA4")
            
            time.sleep(int(recordLength*60))
            
            ''' step '''
            self.logStepBeginning("STEP - check my records mosaic and details of the record after recording CSA4")
            #step logic
            self.assertTrue(self.page.goToPvrMyRecords())
            self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock()))
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.verifyPvrOnRecordScreen(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock(), recordLength, currentProgramInfo.getCsaClass()))
            self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=10))
            self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=recordLength*60/2))
            self.logStepResults("STEP - check my records mosaic and details of the record after recording CSA4")
            
            ''' step '''
            self.logStepBeginning("STEP - start recording CSA5")
            #step logic
            self.assertTrue(self.page.goToLiveByCsaCategory(csaCat=ParentalControl.CssClassCsa5))
            self.rc.sendKeys(["KEY_INFO"])
            currentProgramInfo = self.page.getInfoFromLiveBanner()
            self.assertTrue(type(currentProgramInfo) is ProgramInfoItem, "  >>   ERR: wrong record data")
            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(10)
            self.page.actionInstantRecord(recordLength) #record length in DataSet configuration
            time.sleep(10)
            self.logStepResults("STEP - start recording CSA5")
            
            time.sleep(int(recordLength*60))
            
            ''' step '''
            self.logStepBeginning("STEP - check my records mosaic and details of the record after recording CSA5")
            #step logic
            self.assertTrue(self.page.goToPvrMyRecords(inAdults = True))
            self.assertTrue(self.page.verifyPvrOnMyRecordsMosaic(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock()))
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.verifyPvrOnRecordScreen(currentProgramInfo.getProgram(), currentProgramInfo.getChannelName(), False, currentProgramInfo.getClock(), recordLength, currentProgramInfo.getCsaClass()))
            self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=10))
            self.assertTrue(self.page.playPvrThenBackToPvrScreen(playDuration=recordLength*60/2))
            self.logStepResults("STEP - check my records mosaic and details of the record after recording CSA5")
            
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise

        finally:
            if not self.test_passed:
                self.logger.info("----------- cleaning -----------")
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                # clean logic
                if not self.page.cleanDeleteAllRecordings():
                    self.page.cleanDeleteAllRecordings()
