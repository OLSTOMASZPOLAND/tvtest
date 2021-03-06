# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import datetime
import time

class TC_18530_T999999_035(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18530 - T999999 _W_and_R_bez_TS__scheduled_na_kanale_2_live_na_kanale_1
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            if not self.page.cleanDeleteAllRecordings():
                self.page.cleanDeleteAllRecordings()
            if not self.page.setSatVectors(2):
                if not self.page.setSatVectors(2):
                    self.fail("   ERR   SAT cables connected incorrectly")

            ''' step '''
            self.logStepBeginning("zap to channel 1, scheduled on channel 2")

            self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVPPolonia), "   ERR   cannot zap to channel " + str(self.rc.getChannelTVPPolonia))

            self.page.goToPvrMenu()
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "   ERR   cannot go to " + Menu.pvrManualRecord)

            start = datetime.datetime.now() + datetime.timedelta(minutes=8)
            rec = self.page.actionScheduleRecord(self.rc.getChannelBBCHD, start, 10)
            self.assertTrue(rec, "   ERR   cannot schedule a record")

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

            time.sleep(30)

            self.assertTrue(self.page.checkLive(), "   ERR   live not detected")

            currTime = datetime.datetime.now()

            while not self.page.findInDialogBox(Menu.pvr):
                if (datetime.datetime.now() - currTime).seconds > 300:
                    self.fail("   ERR   timeout, workaround pop-up is not present")
                time.sleep(10)

            self.assertTrue(self.page.actionSelect(Menu.pvrCancelRecord), "   ERR   cannot select " + Menu.pvrCancelRecord)
            time.sleep(10)

            self.assertTrue(self.page.findInDialogBox(DialogBox.PvrConfirm), "   ERR   workaround is not displaying")
            self.assertTrue(self.page.actionSelect(Menu.pvrYes), "   ERR   cannot select " + Menu.pvrYes)

            time.sleep(10)

            self.assertTrue(self.page.goToPvrMyScheduled(shouldBeEmpty=True), "   ERR   my scheduled are not empty")
            self.rc.sendKeys(["KEY_TV"])

            self.page.sleep(200)

            self.assertTrue(self.page.checkLive(), "   ERR   motion not detected")

            self.page.sleep(100)

            self.assertTrue(self.page.checkLive(), "   ERR   motion not detected")

            self.logStepBeginning("check if there is no recording in progress")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records")
            time.sleep(10)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            title = self.page.getInfoFromRecordPage()
            if not title:
                self.fail("   ERR   cannot get info from record page")

            self.assertFalse(title.getRecording(), "   ERR   channel is recording")

            self.logStepResults("check if there is no recording in progress")

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

    def getRecordTime(self):
        a = self.page.getInfoFromTrickBar()
        if a != None:
            a = a.getMinutesInSecondRow()
            if type(a) == int:
                return a
        else:
            self.fail("   ERR   cannot get time")
