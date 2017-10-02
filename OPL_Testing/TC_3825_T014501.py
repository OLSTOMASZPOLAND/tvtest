# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3825_T014501(TC_OPL_template):
    """Implementation of the HP QC test ID - 3825 - T014501_Access Adult section - wrong adult code
    
    @author: Leszek Wawrzonkowski
    """
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")
            
            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            
            ''' step '''
            self.logStepBeginning("STEP - go to VodMenu")
            #step logic - go to 'my preferences'
            self.assertTrue(self.page.goToVodMenu())
            self.logStepResults("STEP - go to VodMenu")
            
            ''' step '''
            self.logStepBeginning("STEP - select vodAdults")
            #step logic - choose parental control
            self.assertTrue(self.page.actionSelect(Menu.vodAdults))
            time.sleep(2)
            self.assertTrue(self.page.findInDialogBox(Menu.parentalControl))
            self.logStepResults("STEP - select vodAdults")
            
            ''' step '''
            self.logStepBeginning("STEP - enter wrong code")
            #step logic - enter a code
            self.rc.sendNumberSequence("7654")
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            self.assertTrue(self.page.findInDialogBox(DialogBox.WrongConfidentialCode))
            self.logStepResults("STEP - enter wrong code")
            
            ''' step '''
            self.logStepBeginning("STEP - enter correct code")
            #step logic - enter a code
            self.rc.sendNumberSequence(Env.CONFIDENTIAL_CODE)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            self.assertTrue(self.page.findInCssSelectorElement(Menu.vodAdults, ".breadcrumb .last")) #check if it is in the adult menu
            self.logStepResults("STEP - enter correct code")
            
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
                # self.page.cleanFunction()
