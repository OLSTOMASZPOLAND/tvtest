# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time
import datetime

class TC_3703_T014776_watch_a_no_rented_vod(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3703 - watch_a_no_rented_vod
    
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

            time.sleep(2)
            self.assertTrue(self.page.goToVodMenu(), "ERR: Entering VOD menu")
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(Menu.vodAutomation), "ERR: Entering VOD automate catalog") 
            time.sleep(10)
            self.assertTrue(self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa1, ParentalControl.CssClassCsa2, ParentalControl.CssClassCsa3, ParentalControl.CssClassCsa4]), "   ERR   cannot find video to rent")

            vod = self.page.getInfoFromVodPage()
            if not vod:
                self.fail("   ERR   cannot get info from VPS")

            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(5)
            self.rc.sendKeys(["KEY_PLAY"])
            time.sleep(5)
            self.assertTrue(self.rent(False), "   ERR   cannot play rented vod")

            self.page.sleep(vod.getLength().seconds / 2)

            self.assertTrue(self.page.checkLive(True), "   ERR   motion not detected")

            self.page.sleep(vod.getLength().seconds / 2 + 120)

            self.assertTrue(self.page.findInCssSelectorElement(Menu.vodAutomation, ".breadcrumb .last"), "   ERR   not in previous menu")

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
