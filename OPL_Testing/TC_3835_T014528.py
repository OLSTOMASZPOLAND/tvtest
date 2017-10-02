# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3835_T014528(TC_OPL_template):
    """Implementation of the HP QC test ID - 3835 - T014528_Access the My Video list when the list is empty
    
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
            self.logStepBeginning("STEP - go to VOD my videos")
            #step logic - TODO - step could be done via stbt to check POPUP
            self.assertFalse(self.page.goToVodMyVideos())
            #TODO is POPUP displayed during 3 seconds
            self.logStepResults("STEP - go to VOD my videos")
            
            ''' step '''
            self.logStepBeginning("STEP - check if it is in VOD root menu")
            #step logic
            time.sleep(3)
            self.assertTrue(self.page.findInCssSelectorElement(Menu.videoOnDemand, ".breadcrumb .first"), "  >>   ERR: is not in the VoD menu") #is in the VoD menu
            self.assertTrue(self.page.findInList(Menu.vodMyVideos, onlyActive = True), "  >>   ERR: has not proper position on the list") # has proper position on the list
            self.logStepResults("STEP - check if it is in VOD root menu")
            
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
