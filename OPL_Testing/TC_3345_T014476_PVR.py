# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3345_T014476_PVR (TC_OPL_template):
    """Implementation of the HP QC test ID - 3345 - T014476_Set payment-parental control to activated with level equal -12 - steps regarding PVR
    
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
            self.logStepBeginning("STEP - set parental control CSA3")
            self.assertTrue(self.page.setParentalControl(ParentalControl.SetActiveCsa3))
            self.logStepResults("STEP - set parental control CSA3")
            
            ''' step '''
            self.logStepBeginning("STEP - watch PVR CSA2")
            if(not self.page.goToPvrByCsaCategory(ParentalControl.CssClassCsa2)):
                self.assertTrue(False, InfoMessages.CsaContentNotFound)
            self.assertTrue(self.page.playPvrThenBackToPvrScreen())
            self.logStepResults("STEP - watch PVR CSA2")
            
            ''' step '''
            self.logStepBeginning("STEP - watch PVR CSA3")
            if(not self.page.goToPvrByCsaCategory(ParentalControl.CssClassCsa3)):
                self.assertTrue(False, InfoMessages.CsaContentNotFound)
            self.assertTrue(self.page.playPvrThenBackToPvrScreen(checkParentalControl = True))
            self.logStepResults("STEP - watch PVR CSA3")
            
            ''' step '''
            self.logStepBeginning("STEP - watch PVR CSA4")
            if(not self.page.goToPvrByCsaCategory(ParentalControl.CssClassCsa4)):
                self.assertTrue(False, InfoMessages.CsaContentNotFound)
            self.assertTrue(self.page.playPvrThenBackToPvrScreen(checkParentalControl = True))
            self.logStepResults("STEP - watch PVR CSA4")
            
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
