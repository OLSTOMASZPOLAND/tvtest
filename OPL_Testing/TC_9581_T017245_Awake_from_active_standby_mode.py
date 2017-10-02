# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_9581_T017245_Awake_from_active_standby_mode (TC_OPL_template):
    '''
    Coverage: T017245_Awake from active standby mode
 
    @author: Mariusz Kolbus
    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
       
        ''' time of to standby mode after which stb will be awoken from active standby mode'''
        t1=60
        
        ''' time after awoking for catching Orange TV strip for checking state of stb'''
        t1Catch=120
        
        
        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")
        
        ''' step '''
        self.logStepBeginning("STEP 1 - set the active stand by mode")
        self.assertTrue(self.page.goToMenu(),'    >>ERR: Problem with going to Menu')
        time.sleep(5)
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(t1)
        self.logStepResults("STEP 1 - set the active stand by mode")
        
        ''' step '''
        self.logStepBeginning("STEP 2 - awakening up from active standby mode")
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(t1Catch)
        self.rc.sendKeys(["KEY_INFO"])
        LiveChannel =self.page.getInfoFromLiveBanner()
        time.sleep(3)
        self.rc.sendKeys(["KEY_BACK"])
        if LiveChannel==None:
            self.assertTrue(False, "  >>  ERR: Problem with awakening, getInfoFromLiveBanner=None")
        
        #self.assertTrue(self.page.findInPage('Orange TV'),'    >>ERR: Problem with awakening, lack of "Orange TV" logo')
        time.sleep(10)
        self.logStepResults("STEP 2 - awakening up from active standby mode")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")