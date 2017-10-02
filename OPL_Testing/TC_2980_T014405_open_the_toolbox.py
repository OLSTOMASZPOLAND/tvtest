# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.StbtIntegration import motionDetection
from time import sleep

class TC_2980_T014405_open_the_toolbox (TC_OPL_template):
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
        
        self.logStepBeginning("STEP - go to channel")
        self.rc.sendKeys(["KEY_3"])
        time.sleep(3)
        self.logStepResults("STEP - go to channel")
        
        self.logStepBeginning("STEP - go to toolbox")
        self.rc.sendKeys(["KEY_OK"])
        self.logStepResults("STEP - go to toolbox")
    
        self.logStepBeginning('STEP - toolbox opened')
        self.assertTrue(len(self.page.getList())>0, "toolbox is not displaying")
        self.logStepResults('STEP - toolbox opened')        
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")