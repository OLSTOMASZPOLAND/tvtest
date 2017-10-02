# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time

class TC_3696_T014562_watch_a_rental_vod_at_the_end_of_the_rent_process(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3696 - watch_a_rental_vod_at_the_end_of_the_rent_process
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")

            self.logStepBeginning("rent VOD, watch it and consult end screen")

            self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot go to vod catalog")
            self.assertTrue(self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa1, ParentalControl.CssClassCsa2, ParentalControl.CssClassCsa3, ParentalControl.CssClassCsa4]), "   ERR   cannot find vod to rent")
            vod = self.page.getInfoFromVodPage()
            if not vod:
                self.fail("   ERR   cannot get info from VPS")
            self.assertTrue(self.page.rentVodThenPlay(), "   ERR   cannot play rented vod")

            self.page.sleep(vod.getLength().seconds / 2)

            self.assertTrue(self.page.checkLive(True), "   ERR   motion not detected")

            self.page.sleep(vod.getLength().seconds / 2 - 120)

            self.assertTrue(self.page.checkLive(True), "   ERR   motion not detected")

            self.page.sleep(200)

            returnVod = self.page.getInfoFromVodPage()
            if not returnVod:
                self.fail("   ERR   when movie finished last page is not loaded")

            self.assertTrue(returnVod.getTitle() == vod.getTitle(), "   ERR   title incorrect")
            self.assertTrue(returnVod.getGenre() == vod.getGenre(), "   ERR   genre incorrect")
            self.assertTrue(returnVod.getLength() == vod.getLength(), "   ERR   length incorrect")

            if self.page.findInCssSelectorElement(Menu.alsoSee, ".seeAlsoLabel"):
                items = self.page.driver.find_elements_by_css_selector(".recoItemsArea > .recoItem")
                self.assertTrue(len(items) > 0, "   ERR   no recommendation items")

            self.logStepResults("rent VOD, watch it and consult end screen")

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

    def rent(self, back):
        if not self.page.findInDialogBox(Menu.vodNPK):
            self.logger.info("  >>   ERR: problem finding >" + Menu.vodNPK + "<")
            return False
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_DOWN"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(5)
        if self.page.findInDialogBox(Menu.vodNPKInfo):
            self.rc.sendKeys(["KEY_OK"])

        time.sleep(1)

        if self.page.findInDialogBox(DialogBox.VodError):  # TODO correct error description
            self.logger.info("  >>   ERR: problem finding >" + DialogBox.VodError + "<")
            return False
        if self.page.findInDialogBox(DialogBox.VodError2):
            self.logger.info("  >>   ERR: general error >" + DialogBox.VodError2 + "<")
            return False
        if self.page.findInDialogBox(DialogBox.VodError3):
            self.logger.info("  >>   ERR: problem finding >" + DialogBox.VodError3 + "<")
            return False
        if self.page.findInCssSelectorElement("menu", ".breadCrumb .path .first"):
            self.logger.info("  >>   ERR: problem with video playback, im back in main menu")
            return False

        time.sleep(10)

        if (self.page.startVodIfNotPlayed(goBackToVodScreen=back)):
            return True
        else:
            return False
