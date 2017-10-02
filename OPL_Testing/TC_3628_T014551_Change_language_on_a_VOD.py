# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3628_T014551_Change_language_on_a_VOD(TC_OPL_template):
    '''
    Coverage: HP QC test ID - 3628 - T014551_Change language on a VOD
    
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
            self.logStepBeginning("Initial State - User is watching a VOD")
            
            status=True
            
            #self.page.setParentalControl(ParentalControl.SetDeactive)
            time.sleep(4)

            time.sleep(4)
            self.assertTrue(self.page.goToVodMenu(), "ERR: Entering VOD Meu")
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(Menu.vodAutomation), "ERR: Entering VOD Catalog")
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(Menu.film_csa1), "ERR: Entering VPS of Not One-Shot VOD") 
            time.sleep(10)
            self.assertTrue(self.page.rentAndPlayOrPlayRentedVod(), "ERR: Renting VOD") 
            time.sleep(7)
            
            status=False
            
            self.logStepResults("Initial State - User is watching a VOD")
            
            ''' Step 1 '''
            self.logStepBeginning("Step 1 - User press OK")
            
            self.rc.sendKeys(["KEY_OK"])
            
            self.logStepResults("Step 1 - User press OK")
            
            ''' Step 2 '''
            self.logStepBeginning("Step 2 - Select language item and validate")
            
            self.assertTrue(self.page.actionSelect(Menu.toolboxNativeSoundtrack), "ERR: Problem finding Soundtrack submenu on list") 
            
            self.logStepResults("Step 2 - Select language item and validate")
            
            ''' Step 3 '''
            self.logStepBeginning("Step 3 - Select language by pressing OK")
            
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(1)         
            self.rc.sendKeys(["KEY_OK"])
            
            self.logStepResults("Step 3 - Select language by pressing OK")
            
            ''' Step 4 '''
            self.logStepBeginning("Step 4 - Check if language is played")
            
            time.sleep(5)
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.findInList(Menu.toolboxOriginalSoundtrack), "ERR: Problem checking if Soundtrack have changed")
            
            self.logStepResults("Step 4 - Check if language is played")
                    
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")
            
            if status==False:
                
                self.rc.sendKeys(["KEY_STOP"])
