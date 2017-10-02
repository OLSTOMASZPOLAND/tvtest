# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time

class TC_3682_T015948_delete_bookmark_on_vod_when_vps_reached_from_vod_catalog(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3682_ - _delete_bookmark_on_vod_when_vps_reached_from_vod_catalog
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")

            ''' step '''
            self.logStepBeginning("go to vod to bookmark and add it")

            self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot enter vod catalogue")
            self.rc.sendKeys(["KEY_DOWN"])
            self.assertTrue(self.page.goToVodToAddToFavoritesInCatalog(), "   ERR   cannot find vod to add bookmark")

            self.assertTrue(self.page.actionSelect(Menu.vodAddToFavorites), "   ERR   cannot select " + Menu.vodAddToFavorites)
            time.sleep(5)
            try:
                self.page.driver.get(Rpi.DUMP)
                time.sleep(1)
                self.page.driver.find_element_by_css_selector(".heart_w")
            except:
                self.fail("   ERR   cannot find Favorite (heart) icon")

            vod = self.page.getInfoFromVodPage()
            self.assertIsNotNone(vod, "   ERR   cannot get info from vod page")

            self.assertTrue(self.page.findInList(Menu.vodRemoveFromFavorites, True), "   ERR    cannot find " + Menu.vodRemoveFromFavorites)

            self.logStepResults("go to vod to bookmark and add it")

            self.logStepBeginning("check if bookmarked item displays in my selection, delete and check if its removed from my selection")

            self.assertTrue(self.page.goToVodMenu(), "   ERR   cannot enter vod menu")
            self.assertTrue(self.page.actionSelect(Menu.vodMyFavorites), "   ERR   cannot find " + Menu.vodMyFavorites)
            time.sleep(3)
            self.assertTrue(self.page.actionSelect(vod.getTitle()), "   ERR   vod is not displaying in my selection")

            self.assertTrue(self.page.actionSelect(Menu.vodRemoveFromFavorites), "   ERR   cannot find " + Menu.vodRemoveFromFavorites)

            self.rc.sendKeys(["KEY_BACK"])

            self.assertFalse(self.page.findInList(vod.getTitle(), True), "   ERR   vod is still visible in my selection")

            self.logStepResults("check if bookmarked item displays in my selection, delete and check if its removed from my selection")

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
