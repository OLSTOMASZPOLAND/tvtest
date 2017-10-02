# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import Menu, ParentalControl
import time

class TC_3646_T015101_video_consult_similar_reco_associated_to_a_regular_vod_at_the_end_of_video(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3646 - video_consult_similar_reco_associated_to_a_regular_vod_at_the_end_of_video
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("go to vod, rent, play and wait until in finish")

        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot go to vod")
        if not self.page.actionSelect(u"Słowo na M".encode('utf-8')):
            self.rc.sendKeys(["KEY_OK"])
        item = self.page.getInfoFromVodPage()
        if not item:
            self.fail("   ERR   cannot get info from VPS page")
        self.assertTrue(self.page.rentVodThenPlay(), "   ERR  cannot rent and play vod")

        self.page.sleep(item.getLength().seconds / 2)

        self.assertTrue(self.page.checkLive(True), "   ERR   motion detection failed")

        self.page.sleep(item.getLength().seconds / 2 + 60)

        self.logStepResults("go to vod, rent, play and wait until in finish")

        self.logStepBeginning("consult see also zone")

        vod = self.page.getInfoFromVodPage()
        if not vod:
            self.fail("   ERR    not in vps")

        self.assertTrue(self.page.findInCssSelectorElement(Menu.alsoSee, ".recommendationList .seeAlsoLabel"), "   ERR   cannot find see also text")
        items = self.page.driver.find_elements_by_css_selector(".recoItemsArea .recoItem")
        self.assertTrue(len(items) > 0, "   ERR   recommended items are not displaying")
        while not self.page.findInXPathElementClass("highlight", "//div[@class='recoItemsArea']/div[1]"):
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(1)

        text = self.page.driver.find_elements_by_css_selector(".recoItemsArea .recoItem")
        if len(text) == 0:
            self.fail("   ERR   bottom contextual banner not found")
        text = text[0].text

        for i in range(1, len(items) + 1):
            self.assertTrue(self.page.findInXPathElementClass("highlight", "//div[@class='recoItemsArea']/div[%i]" % i), "   ERR   wrong item highlighted")
            self.rc.sendKeys(["KEY_RIGHT"])
            time.sleep(1)

        self.assertTrue(self.page.findInXPathElementClass("highlight", "//div[@class='recoItemsArea']/div[1]"), "   ERR   first recommendation is not highlighted")

        self.rc.sendKeys(["KEY_OK"])
        time.sleep(15)
        vod = self.page.getInfoFromVodPage()
        if not vod:
            self.fail("   ERR    canot load vod informations")

        self.assertTrue(vod.getTitle() in text, "    ERR   vod title not found in contextual banner")

        self.logStepResults("consult see also zone")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
