# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_9583_T017247_Awake_from_deep_standby_mode (TC_OPL_template):
    '''
    Coverage: T017247 - Awake from deep standby mode
    @author: Mariusz Kolbus
    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        ''' time of to standby mode after which STB will be awake from deep standby mode'''
        t3=1260
        
        ''' time after awakening for catching Orange TV strip for checking state of STB'''
        t3Catch=240
        
        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")
        
        ''' step '''
        self.logStepBeginning("STEP 1 - set the deep standby mode")
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(5)
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(t3)
        self.logStepResults("STEP 1 - set the deep standby mode")
        
        ''' step '''
        self.logStepBeginning("STEP 2 - awakening up from deep standby mode")
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(t3Catch)
        #self.assertTrue(self.page.findInPage('Orange TV'),'    >>ERR: Problem with awakening, lack of "Orange TV" logo')
        self.rc.sendKeys(["KEY_INFO"])
        LiveChannel =self.page.getInfoFromLiveBanner()
        time.sleep(3)
        self.rc.sendKeys(["KEY_BACK"])
        if LiveChannel==None:
            self.assertTrue(False, "  >>  ERR: Problem with awakening, getInfoFromLiveBanner=None")
        time.sleep(10)
        self.logStepResults("STEP 2 - awakening up from deep standby mode")

        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")