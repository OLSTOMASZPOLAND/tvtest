# -*- coding: utf-8 -*-
import unittest
import time
import logging
from fuzzywuzzy import fuzz
  
from NewTvTesting.ResidentAppPage import *
from NewTvTesting.RemoteControl import *
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
from NewTvTesting.DataSet import *
from time import sleep


class TestTC(unittest.TestCase):


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
            #rc.hardReset()
            #time.sleep(180)
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

    def test_a_t016944(self):
        '''Navigate in TC session unavailable HDD'''
  
        self.logger.info(" ")
        self.logger.info("  ***************")
        self.logger.info("      T016944    ")
        self.logger.info("  ***************")
        self.logger.info(" ")
  
  
        rc = RpiRemoteControl()
        page = WebKitPage()
        time.sleep(5)
        rc.sendKeys(['KEY_TV'])
        #rc.sendKeys(['1'])
        #time.sleep(15)
        rc.sendKeys(['KEY_REWIND'])
        self.assertTrue(self.page.findInPage("body > div.live.scene > div.trick"), "No x icon")
        #if page.findInPage("div.trick.dupa"):
        #    self.test_passed = False
        #else:
        #    self.test_passed = True
        #
        # body > div.live.scene > div.trick.hidden
        page.capturePage()
        page.close()
