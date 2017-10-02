# -*- coding: utf-8 -*-


import unittest
import time

from NewTvTesting.ResidentAppPage import *
from NewTvTesting.RemoteControl import *
from NewTvTesting.StbtIntegration import *
from NewTvTesting.DataSet import *
from NewTvTesting.Config import *


class TestVodBasics(unittest.TestCase):


    def setUp(self):

        self.logger = logging.getLogger('NewTvTesting')
        self.handler = logging.StreamHandler()
        self.logger.addHandler(self.handler)
        formatter = logging.Formatter('%(levelname)s :: %(message)s')
        self.handler.setFormatter(formatter)
        self.logger.setLevel(logging.DEBUG)

        self.page = WebKitPage()
        rc = RpiRemoteControl()

        status = self.page.getStatus()
        if status.getStbStatus() == "KO":
            self.logger.warning("Hard Reset")
            rc.hardReset()
            time.sleep(180)
            status = self.page.getStatus()
        scene = status.getScene()
        if scene == "TOOLBOX" or scene == "ZAPPING_BANNER":
            rc.sendKeys(["KEY_BACK"])
        elif scene == "PORTAL" or scene == "UNKNOWN":
            rc.sendKeys(["KEY_BACK","KEY_BACK","KEY_CHANNELUP"])
        if status.findDialogBox():
            rc.sendKeys(["KEY_BACK","KEY_BACK","KEY_CHANNELUP"])

        self.test_passed = False

    def tearDown(self):
        self.logger.info(self.shortDescription())
        self.page.close()
        self.logger.removeHandler(self.handler)
        self.handler.close()

        if not self.test_passed:
            print("Error " + self.id())
            output = self.id() + time.strftime("%c")
            if Env.VIDEO:
                screenshot(Env.SCREENSHOTS_DIR + output + ".png")

    def test_a_Init(self):
        ''' Hard reset '''
        self.logger.info(" ")
        self.logger.info("  ***************")
        self.logger.info("      Init ")
        self.logger.info("  ***************")
        self.logger.info(" ")

        rc = RpiRemoteControl()
        rc.hardReset()
        time.sleep(180)

        self.test_passed = True

    def test_b_Trailer(self):

        '''Vod selecting and trailer playing'''
        self.logger.info(" ")
        self.logger.info("  *****************************************")
        self.logger.info("      Vod selecting and trailer playing")
        self.logger.info("  *****************************************")
        self.logger.info(" ")

        rc = RpiRemoteControl()

        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_videoOnDemand)
        else:
            self.assertTrue(self.page.actionSelect(Menu.videoOnDemand))

        for text in VodData.TRAILER_1:
            self.page.actionSelect(text)
        self.page.actionSelect(Menu.vodTrailer)
        time.sleep(20)
        rc.sendKeys(["KEY_INFO"])
        self.assertTrue(self.page.findInPage(VodData.TRAILER_1[-1]), "Title not found in Vod banner")

        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"Record play expected")

        rc.sendKeys(["KEY_STOP", "KEY_CHANNELUP"])

        self.test_passed = True

    def test_c_Favorites(self):
        '''Vod favorites'''

        self.logger.info(" ")
        self.logger.info("  *****************************************")
        self.logger.info("      Vod favorites")
        self.logger.info("  *****************************************")
        self.logger.info(" ")


        rc = RpiRemoteControl()

        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_videoOnDemand)
        else:
            self.assertTrue(self.page.actionSelect(Menu.videoOnDemand))
        for text in VodData.FAVORITE_1:
            self.page.actionSelect(text)
        self.assertTrue(self.page.actionSelect(Menu.vodAddToFavorites))
        self.assertTrue(self.page.findInList(Menu.vodRemoveFromFavorites))

        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_videoOnDemand)
        else:
            self.assertTrue(self.page.actionSelect(Menu.videoOnDemand))
        self.assertTrue(self.page.actionSelect(Menu.vodMyFavorites))

        self.assertTrue(self.page.actionSelect(VodData.FAVORITE_1[-1]))
        self.assertTrue(self.page.actionSelect(Menu.vodRemoveFromFavorites))
        self.assertTrue(self.page.findInList(Menu.vodAddToFavorites))

        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_videoOnDemand)
        else:
            self.assertTrue(self.page.actionSelect(Menu.videoOnDemand))
        self.assertTrue(self.page.actionSelect(Menu.vodMyFavorites))

        self.assertFalse(self.page.actionSelect(VodData.FAVORITE_1[-1]))
        rc.sendKeys(["KEY_CHANNELUP"])

        self.test_passed = True

    def test_d_VodRental(self):
        '''
        Vod rental
        '''
        self.logger.info(" ")
        self.logger.info("  *****************************************")
        self.logger.info("      Vod rental")
        self.logger.info("  *****************************************")
        self.logger.info(" ")
        rc = RpiRemoteControl()

        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_videoOnDemand)
        else:
            self.assertTrue(self.page.actionSelect(Menu.videoOnDemand))
        for text in VodData.VOD_1:
            self.page.actionSelect(text)

        ''' vod buying and watching '''
        rentalDate = datetime.now()
        self.assertTrue(self.page.actionSelect(Menu.vodRent))
        self.assertTrue(self.page.actionSelect(Menu.vodPayment))
        self.assertTrue(self.page.actionSelect(Menu.vodConfirm))
        time.sleep(20)
        if self.page.findInDialogBox(DialogBox.VodError):
            rc.sendKeys(["KEY_OK", "KEY_CHANNELUP"])
            self.assertTrue(False, u"VOD technical problem")
        rc.sendKeys(["KEY_INFO"])
        self.assertTrue(self.page.findInPage(VodData.VOD_1[-1]), "Title not found in Vod banner")
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"Record play expected")
        time.sleep(30)
        rc.sendKeys(["KEY_STOP"])

        "checking availability -> console"

        vodDetails = self.page.getInfoFromVodPage()
        self.logger.info("rental date : "+str(rentalDate))
        vodDetails.display()

        "checking myVod list"

        rc.sendKeys(["KEY_MENU"])
        if Env.STB == "NEWBOX":
            rc.sendKeys(Menu.tab_videoOnDemand)
        else:
            self.assertTrue(self.page.actionSelect(Menu.videoOnDemand))
        self.assertTrue(self.page.actionSelect(Menu.vodMyVod))
        self.assertTrue(self.page.actionSelect(VodData.VOD_1[-1]))

        "Vod resuming"

        self.assertTrue(self.page.actionSelect(Menu.vodResume))
        time.sleep(30)
        if Env.VIDEO:
            self.assertTrue(motionDetection(),u"Record play expected")
        time.sleep(30)
        rc.sendKeys(["KEY_STOP", "KEY_CHANNELUP"])


        self.test_passed = True