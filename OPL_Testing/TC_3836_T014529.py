# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3836_T014529(TC_OPL_template):
    """Implementation of the HP QC test ID - 3836 - T014529_Access the My Video list when the package is rented - steps regarding VOD
    
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
            self.assertTrue(self.page.goToVodMyVideos())
            self.logStepResults("STEP - go to VOD my videos")
            
            ''' step '''
            self.logStepBeginning("STEP - check the VOD list")
            #step logic
            time.sleep(3)
            self.assertTrue(self.page.loadPageList())
            self.assertTrue(len(self.page.activeItems)>0, "  >>   ERR: loaded list is empty") #loaded list is not empty
            self.logStepResults("STEP - check the VOD list")
            
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
