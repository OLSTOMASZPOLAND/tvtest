# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import motionDetection
from OPL_Testing.TC_8912_T016328_display_information_of_recording_updated import *


class TC_3627_T016713_Stop_and_resume_a_oneshot_VOD_stop_when_VOD_viewing_period_is_about_to_end(TC_OPL_template):

    """Implementation of the HP QC test ID TC_3627_T016713_Stop_and_resume_a_oneshot_VOD_stop_when_VOD_viewing_period_is_about_to_end
 
    @author: Tomasz Stasiuk
    """

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):


        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING - delete all future and ongoing record in My Records")
        
        if not self.page.cleanCodeParentalToDefault():
            self.page.cleanCodeParentalToDefault()

        if not self.page.setParentalControl(ParentalControl.SetDeactive):
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            self.page.setParentalControl(ParentalControl.SetDeactive)      
        
        '''step'''
        self.logStepBeginning("STEP 1 - Go to VOD")
        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent),"ERR: Go to VOD Catalog")
        self.logStepResults("STEP 1 - Go to VOD")
              
        '''step'''
        self.logStepBeginning("STEP 2 - rent and play one-shot")
        time.sleep(2)
        self.assertTrue(self.page.actionSelect(Menu.oneShotMovie),"ERR: go to one shot vod")
        time.sleep(8)
        self.assertTrue(self.page.rentAndPlayOrPlayRentedVod(),"ERR: play vod")
        self.logStepResults("STEP 2 - rent and play one-shot")
      
        '''step'''
        self.logStepBeginning("STEP 3 - try exit and check pop-up")
        time.sleep(10)
        self.assertTrue(self.page.checkLive(pvrAndVod=True),"ERR: no video on vod")
        time.sleep(3)
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(8)
        self.assertTrue(self.page.actionSelect(Menu.vodResume),"ERR: check pop-up appear")
        time.sleep(8)
        self.assertTrue(self.page.checkLive(pvrAndVod=True),"ERR: no video on vod")

        self.logStepResults("STEP 3 - try exit and check pop-up")

        '''step'''
        self.logStepBeginning("STEP 4 - exit and check pop-up")
        time.sleep(3)
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(8)
        self.assertTrue(self.page.actionSelect(Menu.vodStopWatching),"ERR: check pop-up appear")
        time.sleep(4)
        self.logStepResults("STEP 4 - exit and check pop-up")

        '''step'''
        self.logStepBeginning("STEP 5 - check no video")
        self.assertFalse(self.page.checkLive(pvrAndVod=True),"ERR: not exit from  vod to VPS")
        time.sleep(3)
        self.logStepResults("STEP 5 - check no video")

        '''step'''
        self.logStepBeginning("STEP 6 - check IF vod is rent and check after 15 min if status change")
        self.assertTrue(self.page.actionSelect(Menu.vodResume),"ERR: check pop-up appear")
        time.sleep(5)
        if not Env.ZONE=="IPTV" or Env.ZONE=="FTTH":
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.vodStartWatching),"ERR: check pop-up appear")
        time.sleep(15)
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(5)
        self.assertTrue(self.page.actionSelect(Menu.vodStopWatching),"ERR: check pop-up appear")
        time.sleep(10)
        self.rc.sendKeys(["KEY_BACK"])
        print "wait to end one-shot rent time"
        time.sleep(900)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(5)
        self.assertTrue(self.page.actionSelect(Menu.vodRent),"ERR: check pop-up appear")
        self.logStepResults("STEP 6 - check IF vod is rent and check after 15 min if status change") 
        
        
               
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

