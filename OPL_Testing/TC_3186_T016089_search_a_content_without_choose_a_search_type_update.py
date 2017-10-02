# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time

class TC_3186_T016089_search_a_content_without_choose_a_search_type_update(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3186 - T016089_search_a_content_without_choose_a_search_type_update
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            searchedText = u"pogoda".encode('utf-8')
            self.logger.info("text for search>%s<" % searchedText)
            ''' step '''
            self.logStepBeginning("enter guide search and enter searched text")

            self.rc.zap(self.rc.getChannelTVPPolonia)
            self.rc.sendKeys(["KEY_GUIDE"])
            self.assertTrue(self.page.actionSelect(Menu.epgSearch), "   ERR   cannot find search button")

            time.sleep(10)

            self.rc.sendWord(searchedText)

            time.sleep(5)

            self.rc.sendKeys(["KEY_OK"])

            time.sleep(20)

            self.logStepResults("enter guide search and enter searched text")

            self.logStepBeginning("check search results")

            self.assertTrue(self.page.findInXPathElement(searchedText, "//div[id('breadCrumb')]/ul/li[3]"), "   ERR   cannot find searched text on top")
            items = self.page.getList()
            self.assertTrue(len(items) > 0, "   ERR   no search results are displaying")

            for item in items:
                self.assertTrue(item.text.encode('utf-8').lower().find(searchedText.lower()) > -1, "   ERR   result does not contains searched text, result is: " + item.text)

            self.logStepResults("check search results")

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
