# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time

class TC_3699_T014566_watch_rental_vod_from_the_play_key(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3699 - watch_rental_vod_from_the_play_key
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")

            self.logStepBeginning("step 1")

            self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot go to vod catalog")
            self.assertTrue(self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa1, ParentalControl.CssClassCsa2 , ParentalControl.CssClassCsa3 , ParentalControl.CssClassCsa4]), "   ERR    cannot find vod to watch")

            time.sleep(3)
            vod = self.page.getInfoFromVodPage()
            if not vod:
                self.fail("cannot get info from vod page")

            self.assertTrue(self.page.rentVodThenPlayAndBackToVodScreen(), "   ERR   cannot play rented vod")

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

            self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot go to vod catalog")
            self.assertTrue(self.page.actionSelect(vod.getTitle()), "   ERR   cannot find vod")
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(5)
            self.rc.sendKeys(["KEY_PLAY"])
            self.assertTrue(self.page.startVodIfNotPlayed(), "   ERR   cannot play vod")
            self.page.sleep(vod.getLength().seconds / 2)
            self.assertTrue(self.page.checkLive(True), "   ERR   motion not detected")
            self.page.sleep(vod.getLength().seconds / 2 - 180)
            self.assertTrue(self.page.checkLive(True), "   ERR   motion not detected")
            self.page.sleep(240)

            self.assertTrue(self.page.findInCssSelectorElement(Menu.vodCatalogWithTestContent, ".breadcrumb .last"), "   ERR   not in previous menu")

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise

        finally:
            if not self.test_passed:
                self.logger.info("----------- cleaning -----------")
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])