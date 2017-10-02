# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import motionDetection

class TC_8912_T016328_display_information_of_recording_updated(TC_OPL_template):
    '''Implementation of the HP QC test ID - 8912 - _T016328_Display information of recording_updated
    
        Purpose: User can displays information about the recorded program and control a viewed/paused PVR record (subtitles, additional audio)
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            self.page.cleanDeleteAllRecordings()

            '''step'''
            self.logStepBeginning("STEP 0 - record channel")

            start = False

            if self.recordChannel(self.rc.getChannelHBOHD):
                start = True
            elif self.recordChannel(self.rc.getChannelHBO2HD):
                start = True
            elif self.recordChannel(self.rc.getChannelHBOComedyHD):
                start = True

            if start:
                self.page.sleep(300)
            else:
                self.page.sleep(600)
                if self.recordChannel(self.rc.getChannelHBOHD):
                    start = True
                elif self.recordChannel(self.rc.getChannelHBO2HD):
                    start = True
                elif self.recordChannel(self.rc.getChannelHBOComedyHD):
                    start = True
                if start:
                    self.page.sleep(300)

            if not start:
                self.fail("   ERR   cannot find channel to record")

            self.logStepResults("STEP 0 - record channel")

            '''step'''
            self.logStepBeginning("watch recorded pvr and validate toolbox")

            self.assertTrue(self.page.goToPvrMyRecords(shouldBeEmpty=False), "   ERR   cannot find recorded channel")
            self.rc.sendKeys(["KEY_OK"])

            time.sleep(5)

            self.rc.sendKeys(["KEY_OK"])

            time.sleep(30)

            self.assertTrue(self.page.checkLive(True), "   ERR   motion not detected")

            self.rc.sendKeys(["KEY_OK"])

            self.assertTrue(self.page.actionSelect(Menu.toolboxSummary), "   ERR   cannot find %s button" % Menu.toolboxSummary)
            time.sleep(2)
            self.assertTrue(self.page.findInXPathElementStyle("", "//div[@class='recordInfo']"), "   ERR   'streszczenie' is not available")

            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(2)

            self.assertTrue(self.page.findInXPathElementStyle("display: none;", "//div[@class='recordInfo']"), "   ERR   'streszczenie' is still visible on screen")

            self.assertTrue(self.page.actionSelect(Menu.toolboxNativeSoundtrack), "   ERR   cannot find %s button" % Menu.toolboxNativeSoundtrack)
            self.assertTrue(self.page.actionSelect(Menu.toolbox_2_englishSoundtrack), "   ERR   cannot find %s button" % Menu.toolbox_2_englishSoundtrack)

            self.rc.sendKeys(["KEY_OK"])

            self.assertTrue(self.page.actionSelect(Menu.toolboxNoSubtitleLong), "   ERR   cannot find %s button" % Menu.toolboxNoSubtitleLong)
            self.assertTrue(self.page.actionSelect(Menu.toolbox_2_nativeSubtitle), "   ERR   cannot find %s button" % Menu.toolboxNoSubtitle)

            self.rc.sendKeys(["KEY_OK"])

            self.assertTrue(self.page.actionSelect(Menu.toolboxImageSizeOriginal), "   ERR   cannot find %s button" % Menu.toolboxImageSizeOriginal)
            self.assertTrue(self.page.actionSelect(Menu.toolbox_2_imageSizeZoom), "   ERR   cannot find %s button" % Menu.toolbox_2_imageSizeZoom)

            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)

            items = self.page.getList()
            if items == None:
                self.fail("   ERR   cannot get list of toolbox items")

            self.assertTrue(items[0].text.encode('utf-8') == Menu.toolboxSummary, "   ERR   %s mismatch" % Menu.toolboxSummary)
            self.assertTrue(items[1].text.encode('utf-8') == Menu.toolboxOriginalSoundtrack, "   ERR   %s mismatch" % Menu.toolboxOriginalSoundtrack)
            self.assertTrue(items[2].text.encode('utf-8') == Menu.toolboxNativeSubtitle, "   ERR   %s mismatch" % Menu.toolboxNativeSubtitle)
            self.assertTrue(items[3].text.encode('utf-8') == Menu.toolboxImageSizeZoom, "   ERR   %s mismatch" % Menu.toolboxImageSizeZoom)

            self.logStepResults("watch recorded pvr and validate toolbox")
            self.rc.sendKeys(["KEY_BACK"])
            self.page.deletePvrRecord()

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("error occurred - %s" % e)
            self.logger.info("error occurred - %s - cleaning" % e)
            raise

        finally:
            if not self.test_passed:
                self.logger.info("----------- cleaning -----------")
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                self.page.cleanDeleteAllRecordings()


    def recordChannel(self, channel):
        if not self.page.zapToChannel(channel):
            return False
        time.sleep(5)
        if self.page.findInDialogBox(Menu.channelNotInSubscription):
            self.page.actionSelect(u"tak".encode('utf-8'))
        if not self.page.checkLive():
            return False
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(5)

        hasSubtitles = False
        hasLanguages = False

        if (self.page.findInList(Menu.toolboxNativeSoundtrack, True)):
            if self.page.actionSelect(Menu.toolboxNativeSoundtrack):
                if len(self.page.getList()) > 1:
                    hasSubtitles = True

        self.rc.sendKeys(["KEY_BACK", "KEY_BACK"])
        time.sleep(5)

        self.rc.sendKeys(["KEY_OK"])

        time.sleep(5)

        if (self.page.findInList(Menu.toolboxNoSubtitleLong, True)):
            if self.page.actionSelect(Menu.toolboxNoSubtitleLong):
                if len(self.page.getList()) > 1:
                    hasLanguages = True
        
        
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK"])
        time.sleep(5)            
        
        if hasLanguages and hasSubtitles:
            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(20)
            if self.page.actionInstantRecord():
                return True
            else:
                return False
        else:
            return False
