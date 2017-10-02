# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import time
import datetime

class TC_18504_T999999_009_TS(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18504 - _TC_T099999 W_and_R_z_TS_scheduled_na_kanale_2_live_na_kanale_1_z_TS_zanim_wlaczy_sie_nagranie
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:

            firstChannel = self.rc.getChannelBBCHD
            secondChannel = self.rc.getChannelTVPPolonia

            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            if not self.page.cleanDeleteAllRecordings():
                self.page.cleanDeleteAllRecordings()
            if not self.page.setSatVectors(3):
                if not self.page.setSatVectors(3):
                    self.fail("   ERR   SAT cables connected incorrectly")
            ''' step '''
            self.logStepBeginning("zap to {} and schedule future recording on channel {}".format(secondChannel, firstChannel))

            self.assertTrue(self.page.zapToChannel(secondChannel), "   ERR   cannot zap to channel " + str(secondChannel))

            self.page.goToPvrMenu()
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "   ERR   cannot go to " + Menu.pvrManualRecord)

            start = datetime.datetime.now() + datetime.timedelta(minutes=8)

            self.assertTrue(self.page.actionScheduleRecord(firstChannel, start, 10, 0), "   ERR   cannot schedule a record")

            self.rc.sendKeys(["KEY_TV"])

            time.sleep(10)

            self.rc.sendKeys(["KEY_PLAY"])

            time.sleep(5)

            trickBar = self.page.getInfoFromTrickBar()
            self.assertIsNotNone(trickBar, "   ERR   cannot get info from a trick bar")
            trickBar = trickBar.getTrickIcon()
            self.assertEqual(trickBar, "Pause", "   ERR   can't find pause symbol")

            self.page.sleep(70)

            self.rc.sendKeys(["KEY_PLAY"])

            currTime = datetime.datetime.now()

            while not self.page.findInDialogBox(Menu.pvr):
                if (datetime.datetime.now() - currTime).seconds > 300:
                    self.fail("   ERR   timeout, conflict workaround is not present")
                time.sleep(10)

            self.assertTrue(self.page.actionSelect(Menu.pvrCancelRecord), "   ERR   cannot select " + Menu.pvrCancelRecord)
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.pvrCancelRecord), "   ERR   cannot select " + Menu.pvrCancelRecord)
            time.sleep(2)
            self.assertTrue(self.page.findInDialogBox(DialogBox.PvrConfirm), "   ERR   workaround is not displaying")
            self.assertTrue(self.page.actionSelect(Menu.pvrYes), "   ERR   cannot select " + Menu.pvrYes)

            self.page.sleep(300)

            self.logStepResults("zap to {} and schedule future recording on channel {}".format(secondChannel, firstChannel))

            self.logStepBeginning("check if TS session works correctly")

            self.rc.sendKeys(["KEY_PLAY"])

            time.sleep(10)

            trickBar = self.page.getInfoFromTrickBar()
            self.assertIsNotNone(trickBar, "   ERR   cannot get info from a trick bar")
            trickBar = trickBar.getTrickIcon()
            self.assertEqual(trickBar, "Pause", "   ERR   can't find pause symbol")

            self.rc.sendKeys(["KEY_PLAY"])
            self.page.sleep(30)

            self.assertTrue(self.page.checkLive(False), "   ERR   motion detection failed")
            self.page.sleep(180)
            self.assertTrue(self.page.checkLive(False), "   ERR   motion detection failed")

            self.rc.sendKeys(["KEY_PLAY"])

            recordTime = self.getRecordTime()
            self.assertNotEqual(recordTime, 0, "   ERR   time shifting is not working")

            self.logStepResults("check if TS session works correctly")

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
