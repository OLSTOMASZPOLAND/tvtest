# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3348_T014479_PVR (TC_OPL_template):
    """Implementation of the HP QC test ID - 3348 - T014479_Set payment-parental control to activated - parental level is no control - steps regarding PVR
    
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
            self.logStepBeginning("STEP - watch PVR CSA2")
            if(not self.page.goToPvrByCsaCategory(ParentalControl.CssClassCsa2)):
                self.assertTrue(False, InfoMessages.CsaContentNotFound)
            self.assertTrue(self.page.playPvrThenBackToPvrScreen())
            self.logStepResults("STEP - watch PVR CSA2")
            
            ''' step '''
            self.logStepBeginning("STEP - watch PVR CSA4")
            if(not self.page.goToPvrByCsaCategory(ParentalControl.CssClassCsa4)):
                self.assertTrue(False, InfoMessages.CsaContentNotFound)
            self.assertTrue(self.page.playPvrThenBackToPvrScreen())
            self.logStepResults("STEP - watch PVR CSA4")
            
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
