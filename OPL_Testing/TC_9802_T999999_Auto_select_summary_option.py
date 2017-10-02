# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time

class TC_9802_T999999_Auto_select_summary_option(TC_OPL_template):
    '''Implementation of the HP QC test ID - 9802 - T999999
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("zap to channel " + self.rc.getChannelTVPPolonia)

        self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVPPolonia), "   ERR   cannot zap to channel " + self.rc.getChannelTVPPolonia)
        self.rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.actionSelect(Menu.toolboxSummary), "   ERR   cannot select " + Menu.toolboxSummary)
        time.sleep(3)
        self.page.driver.get(Rpi.DUMP)

        self.logStepBeginning("zap to channel " + self.rc.getChannelTVPPolonia)

        try:
            self.page.driver.find_element_by_css_selector(".cover")
        except:
            self.fail("   ERR   cannot find channel logo")

        try:
            self.page.driver.find_element_by_css_selector(".scrollarea")
        except:
            self.fail("   ERR   cannot find summary area")

        try:
            self.page.driver.find_element_by_css_selector(".name")
        except:
            self.fail("   ERR   cannot find title of a current program")

        try:
            self.page.driver.find_element_by_css_selector(".banner.zappingBanner.effect")
        except:
            self.fail("   ERR   cannot find zapping banner")

        self.rc.sendKeys(["KEY_CHANNELUP", "KEY_CHANNELDOWN"])

        time.sleep(3)

        self.rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.actionSelect(Menu.toolboxSummary), "   ERR   cannot select " + Menu.toolboxSummary)
        time.sleep(3)
        self.rc.sendKeys(["KEY_OK"])
        self.page.driver.get(Rpi.DUMP)
        time.sleep(1)
        element = None
        try:
            element = self.page.driver.find_element_by_css_selector(".scrollarea")
        except:
            pass
        if element:
            self.fail("   ERR   summary window does not disappear after pressing OK key")

        self.rc.sendKeys(["KEY_CHANNELUP", "KEY_CHANNELDOWN"])

        time.sleep(3)

        self.rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.actionSelect(Menu.toolboxSummary), "   ERR   cannot select " + Menu.toolboxSummary)
        time.sleep(3)
        self.rc.sendKeys(["KEY_BACK"])
        self.page.driver.get(Rpi.DUMP)
        time.sleep(1)
        element = None
        try:
            element = self.page.driver.find_element_by_css_selector(".scrollarea")
        except:
            pass
        if element:
            self.fail("   ERR   summary window does not disappear after pressing BACK key")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
