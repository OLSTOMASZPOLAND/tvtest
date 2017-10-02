# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3339_T014470_Modify_confidential_code(TC_OPL_template):
    '''
    Coverage: HP QC test ID - 3339 - T014470_Modify confidential code
    
    Added to Config.py:
    prepaidAccount = u"konto prepaid".encode('utf-8')
    
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

            status = True

            self.page.setParentalControl(ParentalControl.SetActiveCsa2)
            time.sleep(2)
            self.rc.sendKeys(["KEY_MENU"])
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "ERR: Entering My Account")
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myCodes), "ERR: Entering My Codes")
            time.sleep(2)

            self.logStepResults("Initial State - User is in menu My Codes")

            ''' Step 3 '''
            self.logStepBeginning("STEP 3 - User selects confidential code and validate")

            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)

            self.logStepResults("STEP 3 - User selects confidential code and validate")

            ''' Step 4 '''
            self.logStepBeginning("STEP 4 - Enter the correct confidential code")

            self.rc.sendNumberSequence(Env.PARENTAL_CODE)
            time.sleep(2)

            self.logStepResults("STEP 4 - Enter the correct confidential code")

            ''' Step 5 '''
            self.logStepBeginning("STEP 5 - Enter the new confidential code")

            self.rc.sendNumberSequence("4321")
            time.sleep(2)

            self.logStepResults("STEP 5 - Enter the new confidential code")

            ''' Step 6 '''
            self.logStepBeginning("STEP 6 - Enter again the new confidential code and validate")

            self.rc.sendNumberSequence("4321")
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])

            self.logStepResults("STEP 6 - Enter again the new confidential code and validate")

            status = False

            ''' Step 7 '''
            self.logStepBeginning("STEP 7 - Access to area requesting confidential code and enter old confidential code")

            time.sleep(7)
            self.rc.sendKeys(["KEY_MENU"])
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "ERR: Entering My Account")
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myPurchases), "ERR: Entering My Purchases")
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.prepaidAccount), "ERR: Entering Prepaid Account")
            time.sleep(2)

            self.rc.sendNumberSequence(Env.PARENTAL_CODE)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            self.assertTrue(self.page.findInPage('Błędny'), "ERR: Problem verifying if code is wrong")
            time.sleep(2)

            self.logStepResults("STEP 7 - Access to area requesting confidential code and enter old confidential code")

            ''' Step 8 '''
            self.logStepBeginning("STEP 8 - Access to area requesting confidential code and enter new confidential code")

            self.rc.sendNumberSequence("4321")
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            self.assertTrue(self.page.findInPage(u'doładowanie'.encode('utf-8')), "ERR: Problem verifying if code is correct")

            self.logStepResults("STEP 8 - Access to area requesting confidential code and enter new confidential code")

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
            if not self.page.cleanCodeParentalToDefault():
                self.page.cleanCodeParentalToDefault()
            if not self.page.setParentalControl(ParentalControl.SetDeactive):
                self.page.setParentalControl(ParentalControl.SetDeactive)
