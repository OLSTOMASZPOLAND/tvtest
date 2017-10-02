# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3335_T014464_Modify_adult_code(TC_OPL_template):
    '''
    Coverage: HP QC test ID - 3335 - T014464_Modify adult code
    
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
            self.logStepBeginning("Initial State - User is in menu My Codes")
            
            status=True
            
            self.page.setParentalControl(ParentalControl.SetDeactive)
            time.sleep(2)
            self.rc.sendKeys(["KEY_MENU"])
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "ERR: Entering My Account")
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myCodes), "ERR: Entering My Codes")
            time.sleep(2)
            
            self.logStepResults("Initial State - User is in menu My Codes")
     
            ''' Step 3 '''
            self.logStepBeginning("STEP 3 - User selects adult code and validate")
            
            self.rc.sendKeys(["KEY_OK"]) 
            time.sleep(2)
            
            self.logStepResults("STEP 3 - User selects adult code and validate")
            
            ''' Step 4 '''
            self.logStepBeginning("STEP 4 - Enter the correct adult code")
            
            self.rc.sendNumberSequence(Env.CONFIDENTIAL_CODE)
            time.sleep(2)
            
            self.logStepResults("STEP 4 - Enter the correct adult code")
            
            ''' Step 5 '''
            self.logStepBeginning("STEP 5 - Enter the new adult code")
            
            self.rc.sendNumberSequence("1234")
            time.sleep(2)
            
            self.logStepResults("STEP 5 - Enter the new adult code")
            
            ''' Step 6 '''
            self.logStepBeginning("STEP 6 - Enter again the new adult code and validate")
            
            self.rc.sendNumberSequence("1234")
            time.sleep(2)           
            self.rc.sendKeys(["KEY_OK"])
                                 
            self.logStepResults("STEP 6 - Enter again the new adult code and validate")
            
            status=False
            
            ''' Step 7 '''
            self.logStepBeginning("STEP 7 - Access to area requesting adult code and enter old adult code")
            
            time.sleep(6)
            self.rc.sendKeys(["KEY_VIDEO"])
            time.sleep(5)
            self.assertTrue(self.page.actionSelect(Menu.vodAdults), "ERR: Entering Adult VOD Catalog")
            time.sleep(2)
            self.rc.sendNumberSequence(Env.CONFIDENTIAL_CODE)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            self.assertTrue(self.page.findInPage('Błędny'), "ERR: Problem verifying if code is wrong")
            time.sleep(2)
            
            self.logStepResults("STEP 7 - Access to area requesting adult code and enter old adult code")
            
            ''' Step 8 '''
            self.logStepBeginning("STEP 8 - Access to area requesting adult code and enter new adult code")
            
            self.rc.sendNumberSequence("1234")
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            self.assertTrue(self.page.findInList(Menu.vodAdultCatalogWithTestContent), "ERR: Problem verifying if entered code is correct")
                
            self.logStepResults("STEP 8 - Access to area requesting adult code and enter new adult code")
    
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")
            
            if status == False:
                self.page.checkStbStatusIfKoReboot()
            if not self.page.cleanCodeAdultToDefault():
                self.page.cleanCodeAdultToDefault()
            if not self.page.setParentalControl(ParentalControl.SetDeactive):
                self.page.setParentalControl(ParentalControl.SetDeactive)
                                