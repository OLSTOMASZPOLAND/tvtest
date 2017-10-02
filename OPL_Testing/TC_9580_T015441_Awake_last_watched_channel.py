# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_9580_T015441_Awake_last_watched_channel (TC_OPL_template):
    '''
    Coverage: T015441_Awake - last watched channel
    @author: Mariusz Kolbus
    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")
        
        ''' step '''
        self.logStepBeginning("STEP 1 - set the standby mode")
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(5)
        frontPanelBeforeRestart=self.rc.getFrontPanel()
        if frontPanelBeforeRestart!="WHD80":
            if frontPanelBeforeRestart==False:
                self.assertTrue(False, "  >>  ERR FrontPanel")
        time.sleep(10)
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(15)
        self.logStepResults("STEP 1 - set the standby mode")
        
        ''' step '''
        self.logStepBeginning("STEP 2 - waking up the STB")
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(120)
        self.logStepResults("STEP 2- waking up the STB")
        
        ''' step '''
        self.logStepBeginning("STEP 3 - checking out the number of channel")
        frontPanelAfterRestart=self.rc.getFrontPanel()
        if frontPanelBeforeRestart!="WHD80":
            if frontPanelAfterRestart==False:
                self.assertTrue(False, "  >>  ERR FrontPanel")
            if not(frontPanelAfterRestart==frontPanelBeforeRestart):
                self.assertTrue(False, "ERR: Wrong number of channel after waking up")          
        self.logStepResults("STEP 3 - checking out the number of channel")

        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")