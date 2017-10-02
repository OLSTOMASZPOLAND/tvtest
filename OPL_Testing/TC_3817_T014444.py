# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3817_T014444 (TC_OPL_template):
    """Implementation of the HP QC test ID - 3817 - T014444_Browse 24 24 catalog_categories&video list - without step 8, specification "FS_NewTV_Portal_VOD_SxFy.doc" check
    
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
            self.logStepBeginning("STEP - go to VOD catalog")
            self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent))
            self.logStepResults("STEP - go to VOD catalog")
            
            ''' step '''
            self.logStepBeginning("STEP - find VOD to rent and verify VPS")
            if(not self.page.goToVodToRentInCatalog()):
                self.assertTrue(False, InfoMessages.CsaContentNotFound)
            time.sleep(2)
            if not (self.page.verifyVodVpsScreen()):
                self.assertTrue(False, InfoMessages.VodErrorMenu)
            self.logStepResults("STEP - find VOD to rent and verify VPS")
            
            ''' step '''
            self.logStepBeginning("STEP - go to VOD adults, access check")
            self.assertTrue(self.page.goToVodAdults())
            self.logStepResults("STEP - go to VOD adults, access check")
            
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
