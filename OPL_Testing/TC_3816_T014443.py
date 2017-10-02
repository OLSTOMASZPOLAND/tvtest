# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3816_T014443(TC_OPL_template):
    """Implementation of the HP QC test ID - 3816 - T014443_Browse In private-Adult catalog
    
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
            self.logStepBeginning("STEP - go to VOD adults")
            self.assertTrue(self.page.goToVodAdults())
            self.logStepResults("STEP - go to VOD adults")
            
            ''' step '''
            self.logStepBeginning("STEP - check adults menu content")
            #step logic
            self.assertTrue(self.page.findInList(Menu.vodMyFavorites, onlyActive = True))
            self.assertTrue(self.page.findInList(Menu.vodMyFavorites, onlyActive = True))
            self.assertTrue(self.page.findInList(Menu.vodAdultCatalogWithTestContent, onlyActive = True)) #'several Genre items' - only one is checked
            self.logStepResults("STEP - check adults menu content")
            
            ''' step '''
            self.logStepBeginning("STEP - go to VOD adults catalog and check the VOD list")
            #step logic
            self.assertTrue(self.page.actionSelect(Menu.vodAdultCatalogWithTestContent))
            time.sleep(3)
            self.assertTrue(self.page.loadPageList())
            self.assertTrue(len(self.page.activeItems)>1) #loaded list has at least 2 elements
            self.logStepResults("STEP - go to VOD adults catalog and check the VOD list")
            
            ''' step '''
            self.logStepBeginning("STEP - check the VPS screen for the first VOD on the list")
            #step logic
            self.rc.sendKeys(["KEY_OK"]) #choose the first VoD on the list
            time.sleep(3)
            #verify the VPS screen
            if not (self.page.verifyVodVpsScreen(csaCat = ParentalControl.CssClassCsa5, trailerNotActive = True)):
                self.assertTrue(False, InfoMessages.VodErrorMenu)
            self.logStepResults("STEP - check the VPS screen for the first VOD on the list")
            
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
