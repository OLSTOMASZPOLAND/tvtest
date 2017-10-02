# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time

class TC_3338_T014467_modify_adult_code_error_with_new_code_confirmation(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3338 - T014467_Modify adult code - Error with new code confirmation
    
        Purpose: modify adult code, enter  check if new code is valid while watching adult content
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        try:
            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
    
            ''' step '''
            self.logStepBeginning("STEP 3,4,5,6,7 - go to my codes and set new adult code")

            self.assertTrue(self.page.goToMenu(), "   ERR   not in Menu")
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "   ERR   not in my account")
            self.assertTrue(self.page.actionSelect(Menu.myCodes), "   ERR   not in my codes")
            self.assertTrue(self.page.actionSelect(Menu.adultCode), "   ERR   cannot find adult codes")
            time.sleep(5)
            self.rc.sendNumberSequence(Env.CONFIDENTIAL_CODE)
            time.sleep(1)

            self.rc.sendNumberSequence("2222")

            time.sleep(1)

            self.rc.sendNumberSequence("3333")

            time.sleep(1)

            self.rc.sendKeys(["KEY_OK"])

            time.sleep(5)

            self.assertTrue(self.page.findInDialogBox(DialogBox.AdultCodeMismatch), "   ERR   no error message about codes mismatch")

            self.rc.sendNumberSequence("1234")

            time.sleep(1)

            self.rc.sendNumberSequence("1234")

            time.sleep(1)

            self.rc.sendKeys(["KEY_OK"]) 
            time.sleep(3)
            self.assertTrue(self.page.findInDialogBox(DialogBox.NewAdultCodeConfirmation), "   ERR   no new code confirmation popup")

            time.sleep(5)

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

            self.logStepResults("STEP 3,4,5,6,7 - go to my codes and set new adult code")

            ''' step '''
            self.logStepBeginning("STEP 8 - enter adult area and enter previous code")

            self.assertFalse(self.page.goToVodAdults(), "   ERR   adult content accessed with previous code")
            self.rc.sendKeys(["KEY_BACK"])

            self.logStepResults("STEP 8 - enter adult area and enter previous code")

            ''' step '''
            self.logStepBeginning("STEP 9 - enter adult area and enter new code")

            Env.CONFIDENTIAL_CODE = "1234"

            self.assertTrue(self.page.goToVodAdults(), "   ERR   cannot access adult content with a new code")

            self.logStepResults("STEP 9 - enter adult area and enter new code")

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("error occurred - %s" % e)
            self.logger.info("error occurred - %s - cleaning" % e)
            raise

        finally:
            if not self.page.cleanCodeAdultToDefault():
                self.page.cleanCodeAdultToDefault()