# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import datetime
import time

class TC_18535_T999999_040_TS(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18535 - T999999
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:

            firstChannel = self.rc.getChannelTVPPolonia

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

            self.assertTrue(self.page.actionScheduleRecord(firstChannel, start, 10, 0, "test"), "   ERR   cannot schedule a record")

            self.rc.sendKeys(["KEY_TV"])

            time.sleep(5)

            self.rc.sendKeys(["KEY_PLAY"])

            time.sleep(5)

            trickBar = self.page.getInfoFromTrickBar()
            if not trickBar:
                self.fail("   ERR   cannot get info from a trick bar")
            trickBar = trickBar.getTrickIcon()
            self.assertTrue(trickBar == "Pause", "   >>   ERR: can't find pause symbol")

            self.page.sleep(70)

            self.rc.sendKeys(["KEY_PLAY"])

            currTime = datetime.datetime.now()

            while not self.page.findInDialogBox(Menu.pvr):
                if (datetime.datetime.now() - currTime).seconds > 300:
                    self.fail("   ERR   timeout")
                time.sleep(10)

            self.assertTrue(self.page.actionSelect(Menu.pvrCancelRecord), "   ERR   cannot select " + Menu.pvrCancelRecord)

            self.logStepResults("zap to {} and schedule future recording on channel {}".format(firstChannel, firstChannel))

            self.logStepBeginning("check if TS session works correctly")

            self.page.sleep(120)

            self.rc.sendKeys(["KEY_PLAY"])

            time.sleep(5)

            trickBar = self.page.getInfoFromTrickBar()
            if not trickBar:
                self.fail("   ERR   cannot get info from a trick bar")
            trickBar = trickBar.getTrickIcon()
            self.assertTrue(trickBar == "Pause", "   >>   ERR: can't find pause symbol")

            self.rc.sendKeys(["KEY_PLAY"])
            time.sleep(30)

            self.assertTrue(self.page.checkLive(), "   ERR   live not detected")

            time.sleep(180)

            self.assertTrue(self.page.checkLive(), "   ERR   live not detected")

            self.rc.sendKeys(["KEY_PLAY"])

            recordTime = self.getRecordTime()

            self.assertTrue(recordTime != 0, "   ERR   time shifting is not working")

            self.logStepResults("check if TS session works correctly")

            self.rc.sendKeys(["KEY_TV"])

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
