# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.StbtIntegration import motionDetection
from time import sleep

class TC_2951_T014369_zap_to_mosaic (TC_OPL_template):
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
        
        self.logStepBeginning("STEP - go to mosaic")
        self.rc.sendKeys(["KEY_0"])
        self.logStepResults("STEP - go to mosaic")
    
        time.sleep(3)
        
        self.logStepBeginning("STEP - menu")
        self.rc.sendKeys(["KEY_MENU"])
        self.logStepResults("STEP - menu")
        
        self.logStepBeginning("STEP - back live")
        self.rc.sendKeys(["KEY_CHANNELUP"])
        self.logStepResults("STEP - back live")
        
        self.logStepBeginning("STEP - check live")
        time.sleep(5)
        self.assertTrue(self.page.checkLive(), "  >>  No video stream")
        self.logStepResults("STEP - check live")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")