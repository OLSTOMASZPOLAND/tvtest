# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData
from _ast import Return
from datetime import datetime, timedelta
from NewTvTesting.StbtIntegration import *

 

 

class TC_18491_18494_OgladajIpTvNagrywajDttZPlanowaniemNagran(TC_OPL_template):

    """Implementation of the HP QC test ID 18491_18494_OgladajIpTvNagrywajDttZPlanowaniemNagran
 
    @author: Tomasz Stasiuk
    """


       

    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)

   

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")
    
           
    
            ''' prestep '''
    
            self.logStepResults("AT_THE_BEGINNING")
            if (Env.ZONE=="RFTV"):
                self.assertTrue(False, 'ERR: test DTT on RFTV')
            time.sleep(4)
            self.assertTrue(self.page.cleanDeleteAllRecordings(),'ERR:  cleanDeleteAllRecordings')
    
    
            ''' step '''
            self.logStepBeginning("step 1 - do DTT scan and ParentalControl set none ")
            
            self.assertTrue(self.page.setDTTChannels(True),'ERR:  Set DTT Channels')
            self.rc.sendKeys(["KEY_BACK"])
            self.rc.sendKeys(["KEY_BACK"])
            self.rc.sendKeys(["KEY_TV"])
            self.assertTrue(self.page.setParentalControl(ParentalControl.SetDeactive),'ERR: SET ParentalControl')
            self.rc.sendKeys(["KEY_BACK"])
            self.rc.sendKeys(["KEY_BACK"])
            self.rc.sendKeys(["KEY_TV"])
            
            self.logStepResults("step 1 - do DTT scan and ParentalControl set none ")
    
    
            ''' step '''
            
            self.logStepBeginning("step 2 - set record DTT")
            recordLength = 10
            self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVP1HD_dtt), " >> ERR in Zap to TVP1 DTT")
            startTimeDelay = 10
            start = datetime.now() + timedelta(minutes=startTimeDelay)
            sleep = datetime.now() + timedelta(minutes=25)
            self.rc.sendKeys(["KEY_MENU"])
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.pvr),'   ERR   cannot go pvr')
            time.sleep(1)
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord),'   ERR   cannot go to Manual Record')
            self.assertTrue(self.page.actionScheduleRecord(self.rc.getChannelTVP1HD_dtt, start, recordLength, 0, 'test'), "   ERR   cannot set a record")
            self.rc.sendKeys(["KEY_BACK","KEY_BACK","KEY_TV"])
            sleep = datetime.now() + timedelta(minutes=15)
            self.logStepResults("step 2 - set record DTT")
        
            ''' step '''
            self.logStepBeginning('STEP 2 -Go to IP channel live and check')
            self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVP1HD), " >> ERR in Zap to TVP1 HD")
            time.sleep(3)
            self.assertTrue(self.page.checkLive(), '>> Err: Lack of live')
            time.sleep(5)
            self.logStepResults('STEP 2 - Go to IP channel live and check')
            
            ''' step '''
            self.logStepBeginning('STEP 3 -Go to DTT channel and check')
            self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVP1HD_dtt), " >> ERR in Zap to TVP1 DTT")
            time.sleep(3)
            self.assertTrue(self.page.checkLive(), '>> Err: Lack of live')
            time.sleep(5)
            self.logStepResults('STEP 3 -Go to DTT channel and check')
     
            ''' step '''
            self.logStepBeginning('STEP 4 -Wait to end record')
            i=0
            start = datetime.now() 
            while (start<sleep and i<100):
                i=i+1
                time.sleep(10)
                start = datetime.now() 
            time.sleep(600)
            self.assertTrue(self.page.cleanDeleteAllRecordings(),'ERR:  cleanDeleteAllRecordings')
            self.rc.sendKeys(["KEY_BACK","KEY_BACK","KEY_TV"])
            self.logStepResults('STEP 4 -Wait to end record')
            
            ''' step '''
            self.logStepBeginning('STEP 5 -check record')
            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   in goToPvrMyRecords")
            
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(15)            
            self.assertTrue(self.page.checkPvrRecord(), "   ERR   in check PVR record")
            time.sleep(10)
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(10)
            self.assertTrue(self.page.deletePvrRecord(), "   ERR   in deletePvrRecord")
            self.logStepResults('STEP 5 -check record')
                
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")
            time.sleep(5)
            self.page.checkStbStatusIfKoReboot()
            self.page.cleanDeleteAllRecordings()
            self.page.checkStbStatusIfKoReboot()
            self.page.setDTTChannels(False)

            