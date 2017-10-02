# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3191_T016094_search_results_is_empty (TC_OPL_template):
    '''
    
        @author: Arek Kępka
    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)
    def test(self):
        self.logger.info('----- ' + self.__class__.__name__ + ' START -----')
        self.logStepResults('AT_THE_BEGINNING')
        self.logStepBeginning('STEP - Go to search')
        self.rc.sendKeys(['KEY_MENU'])
        self.assertTrue(self.page.actionSelect(u'wyszukiwarka'.encode('utf-8')))
        self.assertTrue(self.page.actionSelect(Menu.videoOnDemand))
        self.logStepResults('STEP - Go to search')
        self.logStepBeginning('STEP - type xyz')
        self.rc.sendWord('xyz')
        self.logStepResults('STEP - type xyz')
        time.sleep(3)
        self.logStepBeginning('STEP - validate')
        self.rc.sendKeys(['KEY_OK'])
        self.logStepResults('STEP - validate')
        self.logStepBeginning('STEP - results displayed - empty')
        self.assertTrue(self.page.findInDialogBox('wyszukiwarki inne'), 'brak wynikow')
        self.logStepResults('STEP - results displayed - empty')
        self.test_passed = True
        self.logger.info('----- ' + self.__class__.__name__ + ' END -----')