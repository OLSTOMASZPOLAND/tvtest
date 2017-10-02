# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3348_T014479_VOD (TC_OPL_template):
    """Implementation of the HP QC test ID - 3348 - T014479_Set payment-parental control to activated - parental level is no control - steps regarding VOD
    
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
            self.logStepBeginning("STEP - go to VOD catalog")
            self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent))
            self.logStepResults("STEP - go to VOD catalog")
            
            ''' step '''
            self.logStepBeginning("STEP - rent and play VOD CSA1")
            if(not self.page.goToVodToRentInCatalogByCsaCategory(ParentalControl.CssClassCsa1)):
                self.assertTrue(False, InfoMessages.CsaContentNotFound)
            time.sleep(2)
            vod_CSA1_title = self.page.getInfoFromVodPage().title
            self.assertTrue(self.page.rentVodThenPlayAndBackToVodScreen())
            self.logStepResults("STEP - rent and play VOD CSA1")
            
            self.rc.sendKeys(["KEY_BACK"])
            
            ''' step '''
            self.logStepBeginning("STEP - rent and play VOD CSA2")
            if(not self.page.goToVodToRentInCatalogByCsaCategory(ParentalControl.CssClassCsa2)):
                self.assertTrue(False, InfoMessages.CsaContentNotFound)
            time.sleep(2)
            vod_CSA2_title = self.page.getInfoFromVodPage().title
            self.assertTrue(self.page.rentVodThenPlayAndBackToVodScreen())
            self.logStepResults("STEP - rent and play VOD CSA2")
            
            self.rc.sendKeys(["KEY_BACK"])
            
            ''' step '''
            self.logStepBeginning("STEP - rent and play VOD CSA4")
            if(not self.page.goToVodToRentInCatalogByCsaCategory(ParentalControl.CssClassCsa4)):
                self.assertTrue(False, InfoMessages.CsaContentNotFound)
            time.sleep(2)
            vod_CSA4_title = self.page.getInfoFromVodPage().title
            self.assertTrue(self.page.rentVodThenPlayAndBackToVodScreen())
            self.logStepResults("STEP - rent and play VOD CSA4")
            
            self.rc.sendKeys(["KEY_BACK"])
            
            ''' step '''
            self.logStepBeginning("STEP - play rented before VOD CSA1")
            self.assertTrue(self.page.actionSelect(vod_CSA1_title))
            time.sleep(2)
            self.assertTrue(self.page.playRentedVodThenBackToVodScreen())
            self.logStepResults("STEP - play rented before VOD CSA1")
            
            self.rc.sendKeys(["KEY_BACK"])
            
            ''' step '''
            self.logStepBeginning("STEP - play rented before VOD CSA2")
            self.assertTrue(self.page.actionSelect(vod_CSA2_title))
            time.sleep(2)
            self.assertTrue(self.page.playRentedVodThenBackToVodScreen())
            self.logStepResults("STEP - play rented before VOD CSA2")
            
            self.rc.sendKeys(["KEY_BACK"])
            
            ''' step '''
            self.logStepBeginning("STEP - play rented before VOD CSA4")
            self.assertTrue(self.page.actionSelect(vod_CSA4_title))
            time.sleep(2)
            self.assertTrue(self.page.playRentedVodThenBackToVodScreen())
            self.logStepResults("STEP - play rented before VOD CSA4")
            
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
