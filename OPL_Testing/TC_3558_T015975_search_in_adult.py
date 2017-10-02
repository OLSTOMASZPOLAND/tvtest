# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3558_T015975_search_in_adult (TC_OPL_template):
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
        self.assertTrue(self.page.actionSelect(Menu.videoOnDemand))
        time.sleep(10)
        self.assertTrue(self.page.actionSelect(Menu.vodAdults))

        self.logStepResults("STEP - Go to search")

        self.logStepBeginning("STEP - enter adult code")
        self.rc.sendNumberSequence(Env.CONFIDENTIAL_CODE)
        self.rc.sendKeys(["KEY_OK"])
        self.logStepResults("STEP - enter adult code")

        self.assertTrue(self.page.actionSelect (Menu.vodSearch))

        self.logStepBeginning("STEP - type bul")
        self.rc.sendWord("xxx")
        self.logStepResults("STEP - type bul")

        time.sleep(3)

        self.logStepBeginning("STEP - results displayed")
        self.assertIsNotNone(self.page.getList(), "   ERR   no results displaying")
        self.assertTrue(len(self.page.getList()) == 1, "   ERR   more than one result for xxx")
        self.logStepResults("STEP - results displayed")
        time.sleep(3)
        self.logStepBeginning("STEP - validate")
        self.rc.sendKeys(["KEY_DOWN", "KEY_OK"])
        self.assertIsNotNone(self.page.getInfoFromVodPage(), "   ERR   not on VPS page")
        self.logStepResults("STEP - validate")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
