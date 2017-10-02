# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time

class TC_3709_T015722_watch_one_shot_vod_at_the_end_of_rent_process(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3709 - watch_one_shot_vod_at_the_end_of_rent_process
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            if not self.page.cleanCodeParentalToDefault():
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                self.page.cleanCodeParentalToDefault()

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")

            self.logStepBeginning("step 1")

            self.assertTrue(self.page.goToVodCatalog(Menu.vodPolishMovies), "   ERR   cannot go to vod catalog")
            self.assertTrue(self.page.actionSelect(Menu.film), "   ERR   cannot find vod to rent: " + Menu.film)
            self.assertTrue(self.page.findInPage(Menu.vodRent), "   ERR   video is currently already rented. Aborting...")
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(5)
            self.rc.sendKeys(["KEY_PLAY"])
            time.sleep(15)
            self.assertTrue(self.rent(False), "   ERR   cannot play rented vod")
            self.page.sleep(300)
            self.assertTrue(self.page.checkLive(True), "   ERR   motion not detected")

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

        time.sleep(10)

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
