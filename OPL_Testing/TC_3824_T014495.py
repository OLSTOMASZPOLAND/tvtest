# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3824_T014495(TC_OPL_template):
    """Implementation of the HP QC test ID - 3824 - T014495_Access-Exit Adult section_without parental control
    
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
            self.logStepBeginning("STEP - set no parental control")
            self.assertTrue(self.page.setParentalControl(ParentalControl.SetDeactive))
            self.logStepResults("STEP - set no parental control")
            
            ''' step '''
            self.logStepBeginning("STEP - go to VOD adults")
            self.assertTrue(self.page.goToVodAdults())
            self.logStepResults("STEP - go to VOD adults")
            
            ''' step '''
            self.logStepBeginning("STEP - go back with BACK key and go to the VOD adults once again")
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(2)
            self.assertTrue(self.page.goToVodAdults(fromVodMenu = True))
            self.logStepResults("STEP - go back with BACK key and go to the VOD adults once again")
            
            ''' step '''
            self.logStepBeginning("STEP - go back with EXIT key and go to the VOD adults once again")
            self.rc.sendKeys(["KEY_EXIT"])
            self.assertTrue(self.page.goToVodAdults())
            self.logStepResults("STEP - go back with EXIT key and go to the VOD adults once again")
            
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
