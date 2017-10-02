# -*- coding: utf-8 -*-

import time
from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_T016944(TC_OPL_template):
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)
    
    def test(self):
        '''Navigate in TC session unavailable HDD'''
        self.logger.info("----- " + self.__class__.__name__ + " START-----")
        self.logStepResults("AT_THE_BEGINNING")
        self.rc.sendKeys(['KEY_TV'])
        time.sleep(3)
        self.rc.sendKeys(['KEY_REWIND'])
        trick = self.page.getInfoFromTrickBar()
        if trick.trickVisible and trick.trickIcon == "Forbidden":
            self.test_passed = True
        self.page.capturePage()
        self.logger.info("----- " + self.__class__.__name__ + " END-----")