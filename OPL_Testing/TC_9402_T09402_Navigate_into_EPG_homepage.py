# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_9402_T09402_Navigate_into_EPG_homepage (TC_OPL_template):
    '''
    Coverage: T09402 - Navigate into EPG Homepage
    @author: Mariusz Kolbus
    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")
        
        
        ''' step '''
        self.logStepBeginning("STEP 1 - going the EPG homepage from Menu and Program TV")
        self.assertTrue(self.page.goToMenu(), '    >>ERR: Problem with going to Menu ')
        time.sleep(5)
        self.assertTrue(self.page.actionSelect(Menu.epg), '    >>ERR: Problem with EPG selection ')
        time.sleep(5)
        self.assertTrue(self.page.actionSelect(Menu.epgWeek), '    >>ERR: Problem with "Teraz" selection')
        time.sleep(5)
        self.assertTrue(self.page.checkIfEpgIsAvalaible(),'    >>ERR: EPG problem')
        time.sleep(10)
        self.logStepResults("STEP 1 - going the EPG homepage from Menu and Program TV")
       
        
        ''' step '''
        self.logStepBeginning("STEP 2- going to program tv by pressing guide key")
        self.rc.sendKeys(["KEY_GUIDE"])
        time.sleep(5)
        self.rc.sendKeys(["KEY_DOWN"])
        time.sleep(5)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(5)
        self.assertTrue(self.page.checkIfEpgIsAvalaible(),'    >>ERR: EPG problem')
        self.logStepResults("STEP 2- going to program tv by pressing guide key")
        

        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")