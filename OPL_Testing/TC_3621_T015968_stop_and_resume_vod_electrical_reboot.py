# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time
import datetime

class TC_3621_T015968_stop_and_resume_vod_electrical_reboot(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3621 - T015968_stop_and_resume_vod_electrical_reboot
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        if not self.page.cleanCodeParentalToDefault():
            self.page.cleanCodeParentalToDefault()

        if not self.page.setParentalControl(ParentalControl.SetDeactive):
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            self.page.setParentalControl(ParentalControl.SetDeactive)

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("find suitable VOD and start playing, then reset STB")

        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot go to vod menu")
        self.assertTrue(self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa2, ParentalControl.CssClassCsa3, ParentalControl.CssClassCsa4]), "   ERR   cannot find vod to rent")
        item = self.page.getInfoFromVodPage()
        if not item:
            self.fail("   ERR   cannot get info from VPS page")
        self.assertTrue(self.page.rentVodThenPlay(), "   ERR  cannot rent and play vod")

        self.page.sleep(180)

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

        self.rc.sendKeys(["KEY_PLAY"])

        self.resetSTB()

        self.logStepResults("find suitable VOD and start playing, then reset STB")

        self.logStepBeginning("start the same VOD again")

        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot go to vod menu")
        self.assertTrue(self.page.actionSelect(item.getTitle()), "   ERR   cannot find previous video")
        self.assertTrue(self.page.playRentedVod(), "   ERR   cannot play VOD")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(5)

        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            vodTime = self.page.driver.find_element_by_css_selector(".time").text
        except:
            self.fail("   ERR   cannot get time info")

        self.assertTrue(vodTime == "00:00", "   ERR   video not started from the begining")

        self.rc.sendKeys(["KEY_PLAY"])

        self.logStepResults("start the same VOD again")

        self.page.sleep(160)

        self.logStepBeginning("after 3 min exit video and start it again")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(5)
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            vodTime = self.page.driver.find_element_by_css_selector(".time").text
        except:
            self.fail("   ERR   cannot get time info")

        self.rc.sendKeys(["KEY_BACK", "KEY_BACK"])
        time.sleep(20)
        self.assertTrue(self.page.playRentedVod(), "   ERR   cannot play video")
        
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(5)
        
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            vodTime2 = self.page.driver.find_element_by_css_selector(".time").text
        except:
            self.fail("   ERR   cannot get time info")

        self.assertTrue(vodTime == vodTime2, "   ERR   video started from different position")

        self.rc.sendKeys(["KEY_PLAY"])

        self.logStepResults("after 3 min exit video and start it again")

        self.page.sleep(180)

        self.logStepBeginning("reset STB and start the same video again")

        self.resetSTB()
        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot go to vod menu")
        self.assertTrue(self.page.actionSelect(item.getTitle()), "   ERR   cannot find previous video")
        self.assertTrue(self.page.playRentedVod(), "   ERR   cannot play VOD")

        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(5)

        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            vodTime = self.page.driver.find_element_by_css_selector(".time").text
        except:
            self.fail("   ERR   cannot get time info")

        self.assertTrue(vodTime == vodTime2, "   ERR   video not started from previous position")

        self.logStepResults("reset STB and start the same video again")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

    def resetSTB(self):
        self.logger.warning("Hard Reset")
        self.rc.hardReset()
        time.sleep(2)
        try:
            currTime = datetime.datetime.now()
            status = False
            moje = None
            time.sleep(15)
            while (status == False):
                datanow = datetime.datetime.now()
                calc = datanow - currTime
                calc = calc.seconds
                if (calc > 240):
                    status = True
                self.rc.sendKeys(["KEY_INFO"])
                time.sleep(2)
                moje = self.page.getInfoFromLiveBanner()
                time.sleep(3)
                if moje != None:
                    status = True
            time.sleep(3)
            self.rc.sendKeys(["KEY_BACK"])
        except:
            time.sleep(240)
            pass


