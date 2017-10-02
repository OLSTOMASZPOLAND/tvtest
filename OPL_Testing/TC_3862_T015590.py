# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3862_T015590(TC_OPL_template):
    """Implementation of the HP QC test ID - 3862 - T015590_Access Adult section_with parental control
    
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
            self.logStepBeginning("STEP - set parental control CSA2")
            self.assertTrue(self.page.setParentalControl(ParentalControl.SetActiveCsa2))
            self.logStepResults("STEP - set parental control CSA2")
            
            ''' step '''
            self.logStepBeginning("STEP - go to VOD adults")
            self.assertTrue(self.page.goToVodAdults())
            self.logStepResults("STEP - go to VOD adults")
            
            ''' step '''
            self.logStepBeginning("STEP - set parental control CSA3")
            self.assertTrue(self.page.setParentalControl(ParentalControl.SetActiveCsa3))
            self.logStepResults("STEP - set parental control CSA3")
            
            ''' step '''
            self.logStepBeginning("STEP - go to VOD adults")
            self.assertTrue(self.page.goToVodAdults())
            self.logStepResults("STEP - go to VOD adults")
            
            ''' step '''
            self.logStepBeginning("STEP - set parental control CSA4")
            self.assertTrue(self.page.setParentalControl(ParentalControl.SetActiveCsa4))
            self.logStepResults("STEP - set parental control CSA4")
            
            ''' step '''
            self.logStepBeginning("STEP - go to VOD adults")
            self.assertTrue(self.page.goToVodAdults())
            self.logStepResults("STEP - go to VOD adults")
            
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise

        finally:
            self.logger.info("----------- cleaning -----------")
            try:            
                if not self.page.setParentalControl(ParentalControl.SetDeactive):
                    self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                    self.page.setParentalControl(ParentalControl.SetDeactive)
            except:
                pass
