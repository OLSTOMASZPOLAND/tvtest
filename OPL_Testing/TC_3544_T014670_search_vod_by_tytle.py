# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3544_T014670_search_vod_by_tytle (TC_OPL_template):
    '''
    
        @author: Arek Kępka
    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")
        
        ''' step '''
        
        self.logStepBeginning("STEP - Go to search")
        self.rc.sendKeys(["KEY_MENU"])
        self.assertTrue(self.page.actionSelect (Menu.vodSearch))
        self.assertTrue(self.page.actionSelect(Menu.videoOnDemand))
        self.logStepResults("STEP - Go to search")
        
        self.logStepBeginning("STEP - type csa")
        self.rc.sendWord("csa")
        self.logStepResults("STEP - type csa") 
        
        time.sleep(3)
        
        self.logStepBeginning("STEP - validate")
        self.rc.sendKeys(["KEY_OK"])
        self.logStepResults("STEP - validate")

        self.logStepBeginning("STEP - results displayed")
        self.assertTrue(len(self.page.getList()) > 0, "no results")
        self.logStepResults("STEP - results displayed")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
