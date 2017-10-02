# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time

class TC_9597_T000000_download_a_vod__immediately_playback_VPS(TC_OPL_template):
    '''Implementation of the HP QC test ID - 9597 - download_a_vod__immediately_playback_VPS
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        if Env.ZONE != 'DTH':
            if Env.ZONE != 'RFTV':
                self.fail("   ERR   test can only run on DTH or RFTV technologies")

        ''' step '''
        self.logStepBeginning("rent VOD")

        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot go to vod catalog")
        self.assertTrue(self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa1, ParentalControl.CssClassCsa2, ParentalControl.CssClassCsa3, ParentalControl.CssClassCsa4]), "   ERR   cannot find vod to rent")
        vod = self.page.getInfoFromVodPage()
        if not vod:
            self.fail("   ERR   cannot get info from VPS")

        self.assertTrue(self.page.actionSelect(Menu.vodRent), "   ERR   problem selecting: " + Menu.vodRent)
        
        time.sleep(10)

        if self.page.findInDialogBox(Menu.vodNPK):
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            if self.page.findInDialogBox(Menu.vodNPKInfo):
                self.rc.sendKeys(["KEY_OK"])
                time.sleep(2)
            else:
                self.fail("  >>   ERR: problem finding >" + Menu.vodNPKInfo + "<")

            time.sleep(10)

            if self.page.findInDialogBox(DialogBox.VodError):  # TODO correct error description
                self.fail("  >>   ERR: problem finding >" + DialogBox.VodError + "<")
            if self.page.findInDialogBox(DialogBox.VodError2):
                self.fail("  >>   ERR: general error >" + DialogBox.VodError2 + "<")

        for i in range(10):
            time.sleep(3)
            if self.page.findInDialogBox(Menu.vodDownloading):
                if self.page.findInDialogBox(Menu.vodStartWatching):
                    self.assertTrue(self.page.findInDialogBox(vod.getTitle()), "   ERR   cannot find vod title in popup")
                    self.assertTrue(self.page.findInDialogBox(Menu.vodMyVideos), "   ERR   cannot find '%s' in popup" % Menu.vodMyVideos)
                    self.assertTrue(self.page.findInDialogBox(DialogBox.Close), "   ERR   cannot find '%s' in popup" % DialogBox.Close)

                    if not self.page.actionSelect(Menu.vodStartWatching):
                        self.fail("  >>   ERR: problem selecting >" + Menu.vodStopWatching + "<")

                    time.sleep(20)

                    if self.page.findInDialogBox(DialogBox.VodError2):
                        self.fail("  >>   ERR: general error >" + DialogBox.VodError2 + "<")

                    break;

        else:
            self.fail("   ERR    cannot find downloading popup")

        time.sleep(180)

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(5)
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            vodTime = self.page.driver.find_element_by_css_selector(".time").text
            if vodTime == '00:00':
                self.fail("   ERR   time is 00:00")
        except:
            self.fail("   ERR   cannot get time info")

        self.rc.sendKeys(["KEY_STOP"])

        self.logStepResults("rent VOD")

        self.logStepBeginning("check if new item appears in my videos")

        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

        time.sleep(10)

        self.assertTrue(self.page.goToVodMenu(), "   ERR    cannot go to vod menu")
        self.assertTrue(self.page.actionSelect(Menu.vodMyVideos), "   ERR   cannot select: " + Menu.vodMyVideos)
        time.sleep(15)
        self.assertTrue(self.page.actionSelect(vod.getTitle()), "   ERR   cannot select video: " + vod.getTitle())
        self.assertTrue(self.page.findInPage(Menu.vodDownloadComplete) or \
                                             self.page.findInPage(Menu.vodDownloadInProgress) \
                                             or self.page.findInPage(Menu.vodDownloadSuspended), "   ERR   problem finding download message")

        self.logStepResults("check if new item appears in my videos")

        self.logStepBeginning("start video again")

        self.assertTrue(self.page.actionSelect(Menu.vodResume), "   ERR   cannot select: " + Menu.vodResume)

        time.sleep(10)

        self.assertTrue(self.page.actionSelect(Menu.vodStartWatching), "   ERR   cannnot select " + Menu.vodStartWatching)

        time.sleep(10)

        self.rc.sendKeys(["KEY_PLAY"])

        time.sleep(2)

        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            vodTime2 = self.page.driver.find_element_by_css_selector(".time").text
        except:
            self.fail("   ERR   cannot get time info")

        self.assertTrue(vodTime == vodTime2, "   ERR   video did not started from the previous position")

        self.logStepResults("start video again")


        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
