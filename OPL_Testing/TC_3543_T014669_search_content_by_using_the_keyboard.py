# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import Menu, Rpi
import time

class TC_3543_T014669_search_content_by_using_the_keyboard(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3543 - search_content_by_using_the_keyboard
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

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

        self.logStepBeginning("check if user can input words virtual keyboard")

        self.rc.sendKeys(["KEY_DOWN"])
        time.sleep(1)

        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            letter = self.page.driver.find_elements_by_css_selector(".virtualKeyboard .highlight")
        except:
            self.fail("   ERR   cannot find focused letter on keyboard")

        self.assertTrue(self.page.findInXPathElementClass("highlight", "//div[@class = 'virtualKeyboard']/div[1]"), "   ERR   letter 'a' is not highlighted")
        self.assertTrue(len(letter) == 1, "   ERR   only one letter should be highlighted")

        self.rc.sendKeys(["KEY_OK"])

        for j in range(26):
            self.rc.sendKeys(["KEY_RIGHT", "KEY_OK"])

        self.rc.sendKeys(["KEY_DOWN", "KEY_OK"])
        
        self.assertTrue(self.page.findInXPathElement("1", "//div[@class = 'virtualKeyboard']/div[1]"), "   ERR   special character keyboard is not opened")

        self.rc.sendKeys(["KEY_LEFT", "KEY_OK"])
        self.rc.sendKeys(["KEY_LEFT", "KEY_UP", "KEY_UP", "KEY_OK"])
        self.rc.sendKeys(["KEY_DOWN"] * 2)


        self.assertTrue(self.page.findInXPathElementClass("highlight", "//div[contains(@class, 'validateButton')]"), "   ERR   search button not highlighted")
        text = u"abcdefghijklmnopqrsuvwxyz ć".encode('utf-8')
        self.assertTrue(self.page.findInCssSelectorElement(text, "#searchInput .inputText"), "   ERR   incorrect text in search bar")

        self.logStepResults("check if user can input words by virtual keyboard")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
