# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3609_T014596_Stop_and_resume_rental_VOD_within_VOD_viewing_period(TC_OPL_template):
    '''
    Coverage: HP QC test ID - 3609 - T014596_Stop and resume rental VOD - within VOD viewing period
    
    @author: Tomasz Stasiuk
    

    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        try:
            
            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            
            ''' Initial State '''
            self.logStepBeginning("Initial State - User is in My account - My preferences screen")
            
            time.sleep(4)
            self.assertTrue(self.page.goToVodMenu(), "ERR: Entering VOD Meu")
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(Menu.vodAutomation), "ERR: Entering VOD Catalog")
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(Menu.film_csa1), "ERR: Entering VPS of Not One-Shot VOD") 
            time.sleep(10)
            self.assertTrue(self.page.rentAndPlayOrPlayRentedVod(), "ERR: Renting VOD") 
            time.sleep(10)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(70)
            
            self.logStepResults("Initial State - User is in My account - My preferences screen")
            
            ''' Step 3 '''
            self.logStepBeginning("Step 3 - Select Language item")
            
            self.rc.sendKeys(["KEY_STOP"])
            time.sleep(2)
            self.assertTrue(self.page.findInList(Menu.vodSummary), "ERR: Checking if we're back in VPS")
            time.sleep(2)
            self.assertTrue(self.page.findInList(Menu.vodTrailer), "ERR: Checking if we're back in VPS")
            time.sleep(2)
            
            self.logStepResults("STEP 3 - Select Language item")
            
            ''' Step 4 '''
            self.logStepBeginning("STEP 4 - Choose Z Lektorem option and validate")
            
            self.assertTrue(self.page.actionSelect(Menu.vodResume), "ERR: Problem with VOD Resume - wznow ogladanie")
            time.sleep(6)
            self.rc.sendKeys(["KEY_PLAY"])
            self.assertTrue(self.page.findInPage('00:01'), "Checking if VOD is resumed from stopped position")
            self.rc.sendKeys(["KEY_PLAY"])
            time.sleep(65)
                 
            self.logStepResults("STEP 4 - Choose Z Lektorem option and validate")
     
            ''' Step 5 '''
            self.logStepBeginning("STEP 5 - Watch a VOD and check the language")
            
            self.rc.sendKeys(["KEY_STOP"])
            time.sleep(2)
            self.assertTrue(self.page.findInList(Menu.vodSummary), "ERR: Checking if we're back in VPS")
            time.sleep(2)
            self.assertTrue(self.page.findInList(Menu.vodTrailer), "ERR: Checking if we're back in VPS")
            time.sleep(2)
            
            self.logStepResults("STEP 5 - Watch a VOD and check the language")
     
            ''' Step 6 '''
            self.logStepBeginning("STEP 6 - Reaccess My account/My preferences/Language and check language")
            
            self.assertTrue(self.page.actionSelect(Menu.vodResume), "ERR: Problem with VOD Resume - wznow ogladanie")
            time.sleep(6)
            self.rc.sendKeys(["KEY_PLAY"])
            self.assertTrue(self.page.findInPage('00:02'), "Checking if VOD is resumed from stopped position")
            self.rc.sendKeys(["KEY_PLAY"])
            time.sleep(1)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(1)
            self.assertTrue(self.page.actionSelect(Menu.VodBeginning), "Choose 'Od Poczatku' option")
            time.sleep(2)
            self.rc.sendKeys(["KEY_PLAY"])
            self.assertTrue(self.page.findInPage('00:00'), "Checking if VOD is played from the beginning")
            self.rc.sendKeys(["KEY_PLAY"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_STOP"])
                 
            self.logStepResults("Reaccess My account/My preferences/Language and check the language")
     
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")