# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.Config import *

class TC_18704_RFC_2904_interactive_banners_going_to_next_page_when_banner_is_selected(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18684 - RFC_2904_interactive_banners_fast_shifting_mosaic_pages
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("step 1")
        self.rc.zap(0)

        self.page.driver.get(Rpi.DUMP)
        time.sleep(1)

        elements = self.page.driver.find_elements_by_xpath("//div[@class='focusLabel']")
        
        for el in elements:
            if "1. TVP 1" in el.text or "1. TVP1" in el.text:
                break
        else:
            self.fail("   ERR   cannot find TVP1 on mosaic")
            
        self.rc.sendKeys(["KEY_RIGHT"] * 4)
        self.rc.sendKeys(["KEY_DOWN"])
        
        time.sleep(3)
        
        self.page.driver.get(Rpi.DUMP)
        time.sleep(1)

        elements = self.page.driver.find_elements_by_xpath("//div[@class='focusLabel']")
        
        for el in elements:
            if "1. TVP 1" in el.text or "1. TVP1" in el.text:
                self.fail("   ERR   I've found TVP1 on mosaic")                   

        self.logStepResults("step 1")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
