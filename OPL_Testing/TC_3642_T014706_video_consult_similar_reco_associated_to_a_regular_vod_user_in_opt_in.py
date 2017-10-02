# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import Menu
import time

class TC_3642_T014706_video_consult_similar_reco_associated_to_a_regular_vod_user_in_opt_in(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3642 - video_consult_similar_reco_associated_to_a_regular_vod_user_in_opt_in
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("go to vod")

        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot go to vod")
        
        if not self.page.actionSelect(u"Słowo na M".encode('utf-8')):
            self.rc.sendKeys(["KEY_OK"])

        self.logStepResults("go to vod")

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

        text = self.page.driver.find_elements_by_css_selector(".recoItem.highlight .recoMovieTitle")
        self.assertGreater(len(text), 0, "   ERR   bottom contextual banner not found")
        text = text[0].text.encode('utf-8').upper()

        self.rc.sendKeys(["KEY_OK"])
        time.sleep(15)
            
        isVod = self.page.getInfoFromVodPage()
        isPackage = self.page.driver.find_elements_by_css_selector("#packRent")
        if isVod:
            self.assertTrue(isVod.getTitle() in text, "    ERR   vod title not found in contextual banner")
        elif isPackage:
            title = self.page.driver.find_element_by_css_selector("#breadCrumb .first").text.encode('utf-8').upper()
            self.assertTrue(title in text or title.replace(" ", "") in text, "   ERR   title of package not found in contextual banner")
        else:
            self.fail("   ERR   not in VPS or package screen after entering see also item")            

        self.logStepResults("consult see also zone")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
