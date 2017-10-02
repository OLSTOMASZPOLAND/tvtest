# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3866_T015596 (TC_OPL_template):
    """Implementation of the HP QC test ID - 3866 - T015596_Access a content of the In private-Adult section_without parental control - steps regarding CSA3 and CSA5 (no trailer!!!)
    
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
            self.logStepBeginning("STEP - go to VOD adults catalog")
            self.assertTrue(self.page.goToVodAdults())
            self.assertTrue(self.page.actionSelect(Menu.vodAdultCatalogWithTestContent))
            self.logStepResults("STEP - go to VOD adults catalog")
            
            ''' step '''
            self.logStepBeginning("STEP - select, rent and play VOD CSA3")
            if(not self.page.goToVodToRentInCatalogByCsaCategory(ParentalControl.CssClassCsa3, count_vod_max_search = 5)):
                self.assertTrue(False, InfoMessages.CsaContentNotFound)
            time.sleep(2)
            self.assertTrue(self.page.verifyVodVpsScreen(csaCat = ParentalControl.CssClassCsa3, trailerNotActive = True))
            self.assertTrue(self.page.rentVodThenPlayAndBackToVodScreen())
            self.logStepResults("STEP - select, rent and play VOD CSA3")
            
            self.rc.sendKeys(["KEY_BACK"])
            
            ''' step '''
            self.logStepBeginning("STEP - select, rent and play VOD CSA5")
            if(not self.page.goToVodToRentInCatalogByCsaCategory(ParentalControl.CssClassCsa5, count_vod_max_search = 5)):
                self.assertTrue(False, InfoMessages.CsaContentNotFound)
            time.sleep(2)
            self.assertTrue(self.page.verifyVodVpsScreen(csaCat = ParentalControl.CssClassCsa5, trailerNotActive = True))
            self.assertTrue(self.page.rentVodThenPlayAndBackToVodScreen())
            self.logStepResults("STEP - select, rent and play VOD CSA5")
            
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
