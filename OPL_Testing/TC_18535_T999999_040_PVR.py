# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import datetime
import time

class TC_18535_T999999_040_PVR(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18535 - T999999_W_and_R_
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:

            firstChannel = self.rc.getChannelBBCHD

            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            if not self.page.cleanDeleteAllRecordings():
                self.page.cleanDeleteAllRecordings()
            if not self.page.setSatVectors(2):
                if not self.page.setSatVectors(2):
                    self.fail("   ERR   SAT cables connected incorrectly")

            ''' step '''
            self.logStepBeginning("zap to {} and schedule future recording on channel {}".format(firstChannel, firstChannel))

            self.assertTrue(self.page.zapToChannel(firstChannel), "   ERR   cannot zap to channel " + str(firstChannel))

            self.page.goToPvrMenu()
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "   ERR   cannot go to " + Menu.pvrManualRecord)

            start = datetime.datetime.now() + datetime.timedelta(minutes=8)

            item = self.page.actionScheduleRecord(self.rc.getChannelBBCHD, start, 10)
            self.assertTrue(item , "   ERR   cannot set scheduled record")

            self.rc.sendKeys(["KEY_TV"])

            time.sleep(5)

            self.rc.sendKeys(["KEY_PLAY"])

            time.sleep(5)

            trickBar = self.page.getInfoFromTrickBar()
            if not trickBar:
                self.fail("   ERR   cannot get info from a trick bar")
            trickBar = trickBar.getTrickIcon()
            self.assertTrue(trickBar == "Pause", "   >>   ERR: can't find pause symbol")

            time.sleep(30)

            self.rc.sendKeys(["KEY_PLAY"])

            currTime = datetime.datetime.now()

            while not self.page.findInDialogBox(Menu.pvr):
                if (datetime.datetime.now() - currTime).seconds > 300:
                    self.fail("   ERR   timeout")
                time.sleep(10)

            self.assertTrue(self.page.actionSelect(Menu.epgRecord), "   ERR   cannot select " + Menu.epgRecord)

            self.page.sleep(200)

            self.rc.sendKeys(["KEY_PLAY"])

            time.sleep(10)

            trickBar = self.page.getInfoFromTrickBar()
            if trickBar:
                self.fail("   ERR   workaround is not working")

            if Env.VIDEO:
                if not motionDetection():
                    time.sleep(15)
                    if not motionDetection():
                        self.fail("   ERR   motion detection failed")

            self.page.sleep(400)

            if Env.VIDEO:
                if not motionDetection():
                    time.sleep(15)
                    if not motionDetection():
                        self.fail("   ERR   motion detection failed")

            self.page.sleep(400)

            if Env.VIDEO:
                if not motionDetection():
                    time.sleep(15)
                    if not motionDetection():
                        self.fail("   ERR   motion detection failed")

            self.logStepResults("zap to {} and schedule future recording on channel {}".format(firstChannel, firstChannel))

            self.page.sleep(200)

            self.logStepBeginning("after record is made go and play it")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records")

            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            title = self.page.getInfoFromRecordPage()
            if not title:
                self.fail("   ERR   cannot get info from record page")
            self.assertTrue(title.getTitle() == item, "   ERR   title mismatch, record is not made")
            self.rc.sendKeys(["KEY_OK"])

            self.page.sleep(100)

            if Env.VIDEO:
                if not motionDetection():
                    time.sleep(15)
                    if not motionDetection():
                        self.fail("   ERR   motion detection failed")

            self.page.sleep(100)

            if Env.VIDEO:
                if not motionDetection():
                    time.sleep(15)
                    if not motionDetection():
                        self.fail("   ERR   motion detection failed")
            self.rc.sendKeys(["KEY_BACK"])
            self.page.deletePvrRecord()

            self.logStepResults("after record is made go and play it")

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
                if not self.page.cleanDeleteAllRecordings():
                    self.page.cleanDeleteAllRecordings()
