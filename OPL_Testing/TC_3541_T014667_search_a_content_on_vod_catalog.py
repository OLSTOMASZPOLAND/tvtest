# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time
from wheel.signatures import assertTrue

class TC_3541_T014667_search_a_content_on_vod_catalog(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3541 - search_a_content_on_vod_catalog
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):

        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("go to search page")

        self.page.goToMenu()
        self.assertTrue(self.page.actionSelect(Menu.vodSearch), "   ERR    cannot select " + Menu.vodSearch)
        self.assertTrue(self.page.actionSelect(Menu.videoOnDemand), "   ERR    cannot select " + Menu.videoOnDemand)

        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            self.page.driver.find_element_by_css_selector(".keybAndMessage")
        except:
            self.fail("   ERR   cannot find virtual keyboard")

        self.logStepResults("go to search page")

        self.logStepBeginning("check if user can input words by SMS input and virtual keyboard")

        self.rc.sendKeys(["KEY_DOWN"])
        time.sleep(1)

        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            letter = self.page.driver.find_elements_by_css_selector(".virtualKeyboard .highlight")
        except:
            self.fail("   ERR   cannot find focused letter on keyboard")

        self.assertTrue(len(letter) == 1, "   ERR   only one letter should be highlighted")
        self.rc.sendKeys(["KEY_OK"])
        self.page.findInCssSelectorElement("a", "#searchInput .inputText")
        self.rc.sendKeys(["KEY_UP", "KEY_LEFT"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_3"])
        self.page.findInCssSelectorElement("d", "#searchInput .inputText")

        self.logStepResults("check if user can input words by SMS input and virtual keyboard")

        self.logStepBeginning("search for videos")

        self.rc.sendKeys(["KEY_LEFT"])
        self.rc.sendWord("csa")

        time.sleep(5)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(2)

        items = self.page.getList()
        if not items:
            self.fail("   ERR   list not found")

        for i in items:
            self.assertTrue(i.text.lower().find("csa"))

        for i in range(0, len(items)):
            if i != 0:
                self.rc.sendKeys(["KEY_DOWN"] * i)
            time.sleep(3)
            self.rc.sendKeys(["KEY_OK"])

            time.sleep(5)

            vps = self.page.getInfoFromVodPage()

            if not vps:
                if self.page.findInList(Menu.vodPackageOffer):
                    self.rc.sendKeys(["KEY_BACK"])
                    continue
                self.fail("   ERR   not on vps page")

            self.assertTrue(items[i].text.encode('utf-8') == vps.getTitle().encode('utf-8'), "   ERR   incorrect vps")

            self.rc.sendKeys(["KEY_BACK"])

        self.rc.sendKeys(["KEY_BACK"])
        self.rc.sendKeys(["KEY_LEFT"] * 3)

        self.rc.sendWord("zdzira")

        items = self.page.getList()
        if not items:
            self.fail("   ERR   list not found")

        self.assertTrue(len(items) == 1, "   ERR   more than one result")

        self.rc.sendKeys(["KEY_OK"])

        time.sleep(5)

        vps = self.page.getInfoFromVodPage()
        if not vps:
            self.fail("   ERR   not on vps page")

        self.assertTrue(items[0].text.lower().encode('utf-8') == vps.getTitle().lower().encode('utf-8'), "   ERR   incorrect vps")

        self.logStepResults("search for videos")


        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
