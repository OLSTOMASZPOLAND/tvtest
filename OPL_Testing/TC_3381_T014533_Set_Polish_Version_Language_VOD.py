# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3381_T014533_Set_Polish_Version_Language_VOD(TC_OPL_template):
    '''
    Coverage: HP QC test ID - 3381 - T014533_Set Polish Version Language - VOD
    
    @author: Kamil Kulinski
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
            
            self.page.setParentalControl(ParentalControl.SetDeactive)
            time.sleep(2)
            self.rc.sendKeys(["KEY_MENU"])
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "ERR: Entering My Account")
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.mySettings), "ERR: Entering My Settings")
            time.sleep(2)
            
            self.logStepResults("Initial State - User is in My account - My preferences screen")
            
            ''' Step 3 '''
            self.logStepBeginning("Step 3 - Select Language item")
            
            self.assertTrue(self.page.actionSelect(Menu.language), "ERR: Entering Language Menu") 
            time.sleep(2)
            
            self.logStepResults("STEP 3 - Select Language item")
            
            ''' Step 4 '''
            self.logStepBeginning("STEP 4 - Choose Z Lektorem option and validate")
            
            self.assertTrue(self.page.actionSelect(Menu.nativeSoundtrack), "ERR: Selecting 'Z lektorem' option") 
                 
            self.logStepResults("STEP 4 - Choose Z Lektorem option and validate")
     
            ''' Step 5 '''
            self.logStepBeginning("STEP 5 - Watch a VOD and check the language")
            
            time.sleep(2)

            self.assertTrue(self.page.goToVodCatalog(Menu.vodPolishMovies), "ERR: Entering VOD Catalog")
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(Menu.VOD_language), "ERR: Entering VOD VPS") 
            time.sleep(10)
            self.assertTrue(self.page.rentAndPlayOrPlayRentedVod(), "ERR: Renting VOD") 
            time.sleep(10)
            self.rc.sendKeys(["KEY_OK"])
            
            time.sleep(10)
    
            self.assertTrue(self.page.findInList(Menu.toolboxNativeSoundtrack), "ERR: Problem checking if language in VOD toolbox have changed")
            
            self.rc.sendKeys(["KEY_STOP"])
            self.rc.sendKeys(["KEY_DOWN"])
            self.rc.sendKeys(["KEY_OK"])
            
            '''back to Live'''
            self.rc.sendKeys(["KEY_BACK"])

            self.logStepResults("STEP 5 - Watch a VOD and check the language")
     
            ''' Step 6 '''
            self.logStepBeginning("STEP 6 - Reaccess My account/My preferences/Language and check language")
            
            '''back to Live'''
            self.rc.sendKeys(["KEY_BACK"])
            self.rc.sendKeys(["KEY_BACK"])
            self.rc.sendKeys(["KEY_TV"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_MENU"])
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "ERR: Entering My Account")
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.mySettings), "ERR: Entering My Settings")
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.language), "ERR: Entering Language Menu") 
            time.sleep(2)
            self.assertTrue(self.page.findInList(Menu.nativeSoundtrack), "ERR: Checking if language is set to Native") 
                 
            self.logStepResults("Reaccess My account/My preferences/Language and check the language")
     
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")