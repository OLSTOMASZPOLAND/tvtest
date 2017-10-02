# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import datetime
import time

class TC_18536_T999999_041_PVR(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18536 - T999999
    
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
            self.logStepBeginning("Set TS session on channel " + str(self.rc.getChannelBBCHD))

            self.assertTrue(self.page.zapToChannel(self.rc.getChannelBBCHD), "   ERR   cannot zap to " + str(self.rc.getChannelBBCHD))

            self.rc.sendKeys(["KEY_PLAY"])

            self.page.sleep(90)

            self.assertTrue(self.getRecordTime() != 0, "   ERR   TS time equals zero")

            self.rc.sendKeys(["KEY_PLAY"])

            time.sleep(10)

            self.logStepResults("Set TS session on channel " + str(self.rc.getChannelBBCHD))

            self.logStepBeginning("start instant recording on channel " + str(self.rc.getChannelBBCHD))

            self.rc.sendKeys(["KEY_INFO"])
            item = self.page.getInfoFromLiveBanner()
            self.assertIsNotNone(item, "   ERR   cannot get info from live banner")

            self.rc.sendKeys(["KEY_RECORD"])

            time.sleep(20)

            self.assertTrue(self.page.findInDialogBox(Menu.conflictAttention), "   ERR   workaround is not displaying")
            self.assertTrue(self.page.actionSelect(Menu.pvrYes), "   ERR   cannot select " + Menu.pvrYes)

            time.sleep(20)

            self.assertTrue(self.page.actionInstantRecord(10), "   ERR   cannot set instant record")

            time.sleep(340)

            self.assertTrue(self.page.checkLive(), "   ERR    live not detected")

            time.sleep(120)

            self.rc.sendKeys(["KEY_PLAY"])
            time.sleep(10)
            self.assertTrue(self.page.getInfoFromTrickBar() == None, "   ERR   TS session in progress")


            self.assertTrue(self.page.checkLive(), "   ERR    live not detected")

            self.rc.sendKeys(["KEY_INFO"])

            self.logStepResults("start instant recording on channel " + self.rc.getChannelBBCHD)

            self.page.sleep(200)

            self.logStepBeginning("after record is made go and play it")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records")
            time.sleep(10)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            title = self.page.getInfoFromRecordPage()
            if not title:
                self.fail("   ERR   cannot get info from record page")
            title1 = title.getTitle().upper()
            title2 = item.getProgram().upper()
            import string
            title1 = ''.join([str(char) for char in title1 if char in string.printable])
            title2 = ''.join([str(char) for char in title2 if char in string.printable])

            self.assertTrue(title1.find(title2) != -1 or title2.find(title1) != -1, "   ERR   title mismatch, record is not made")
            self.rc.sendKeys(["KEY_OK"])

            self.page.sleep(100)

            self.assertTrue(self.page.checkLive(True), "   ERR   motion not detected")

            self.page.sleep(100)

            self.assertTrue(self.page.checkLive(True), "   ERR   motion not detected")

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

    def getRecordTime(self):
        a = self.page.getInfoFromTrickBar()
        if a != None:
            a = a.getMinutesInSecondRow()
            if type(a) == int:
                return a
        else:
            self.fail("   ERR   cannot get time")
