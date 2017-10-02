# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template
from datetime import date


class TC_9582_T017246_Awake_from_standby_mode (TC_OPL_template):
    '''
    Coverage: T017246 - Awake from standby mode
    @author: Mariusz Kolbus
    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")
        
        ''' time of to standby mode after which STB will be awake from standby mode'''
        t2=1000
        
        ''' time after awakening for catching Orange TV strip for checking state of STB'''
        t2Catch=240
        
        ''' step '''
        self.logStepBeginning("STEP 1 - set the stand by mode")
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(5) 
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(t2)
        self.logStepResults("STEP 1 - set the stand by mode")
        
        ''' step '''
        self.logStepBeginning("STEP 2 - awakening up from standby mode")
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(t2Catch)
        #self.assertTrue(self.page.findInPage('Orange TV'),'    >>ERR: Problem with awakening, lack of "Orange TV" logo')
        self.rc.sendKeys(["KEY_INFO"])
        LiveChannel =self.page.getInfoFromLiveBanner()
        time.sleep(3)
        self.rc.sendKeys(["KEY_BACK"])
        if LiveChannel==None:
            self.assertTrue(False, "  >>  ERR: Problem with awakening, getInfoFromLiveBanner=None")
        
        time.sleep(10)
        self.logStepResults("STEP 2 - awakening up from standby mode")

        
        
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")