# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import motionDetection
from OPL_Testing.TC_8912_T016328_display_information_of_recording_updated import *


class TC_3623_T015983_Stop_and_resume_a_rental_VOD_out_of_VOD_viewing_period2(TC_OPL_template):

    """Implementation of the HP QC test ID TC_3623_T015983_Stop_and_resume_a_rental_VOD_out_of_VOD_viewing_period2
 
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
        self.logStepBeginning("STEP 2 - rent and play vod")
        time.sleep(5)
        self.rc.sendKeys(["KEY_OK"])
        n=False
        i=0
        while n!=True:
            title = self.page.getInfoFromVodPage().title
            print title
            if "1h" in title:
                n=True
            else:
                time.sleep(2)
                self.rc.sendKeys(["KEY_RIGHT"])
            time.sleep(10)
            i=i+1
            if i==30:
                self.assertTrue(False, '  >>  no VOD with 1h')
        time.sleep(8)
        self.assertTrue(self.page.rentAndPlayOrPlayRentedVod(),"ERR: play vod")
        time.sleep(11)
        self.rc.sendKeys(["KEY_PLAY"])
        print "wait to end vod rent time"
        time.sleep(3700)
        self.rc.sendKeys(["KEY_PLAY"])
        self.logStepResults("STEP 2 - rent and play vod")
      
        '''step'''
        self.logStepBeginning("STEP 3 - try exit and check pop-up")
        time.sleep(10)
        self.assertTrue(self.page.checkLive(pvrAndVod=True),"ERR: no video on vod")
        time.sleep(11)
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(11)
        self.assertTrue(self.page.actionSelect(Menu.vodResume),"ERR: check pop-up appear")
        time.sleep(11)
        self.assertTrue(self.page.checkLive(pvrAndVod=True),"ERR: no video on vod")
        self.logStepResults("STEP 3 - try exit and check pop-up")

        '''step'''
        self.logStepBeginning("STEP 4 - exit and check pop-up")
        time.sleep(11)
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(11)
        self.assertTrue(self.page.actionSelect(Menu.vodStopWatching),"ERR: check pop-up appear")
        self.logStepResults("STEP 4 - exit and check pop-up")

        '''step'''
        self.logStepBeginning("STEP 5 - check no video")
        time.sleep(11)
        self.assertFalse(self.page.checkLive(pvrAndVod=True),"ERR: not exit from  vod to VPS")
        time.sleep(11)
        self.logStepResults("STEP 5 - check no video")

        '''step'''
        self.logStepBeginning("STEP 6 - check IF vod is not rent")
        self.assertTrue(self.page.actionSelect(Menu.vodRent),"ERR: check pop-up appear")
        time.sleep(5)
        self.logStepResults("STEP 6 - check IF vod is not rent")        
        
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

