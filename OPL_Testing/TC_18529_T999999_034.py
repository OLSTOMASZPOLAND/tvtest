# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import datetime
import time

class TC_18529_T999999_034(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18529 - T999999 _W_and_R_bez_TS_najpierw_live_na_kanale_1_instant_na_kanale_2
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")


            time.sleep(90)
            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            if not self.page.cleanDeleteAllRecordings():
                self.page.cleanDeleteAllRecordings()
            if not self.page.setSatVectors(2):
                if not self.page.setSatVectors(2):
                    self.fail("   ERR   SAT cables connected incorrectly")

            ''' step '''
            self.logStepBeginning("instant recording on channel 1, live on channel 2")

            self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVPPolonia), "   ERR   cannot zap to " + self.rc.getChannelTVPPolonia)

            time.sleep(30)

            self.assertTrue(self.page.checkLive(), "   ERR   live not detected")

            self.rc.sendKeys(["KEY_INFO"])
            time.sleep(2)

            item = self.page.getInfoFromLiveBanner()

            if not item:
                self.fail("   ERR   cannot get info from live banner")

            self.rc.sendKeys(["KEY_RECORD"])

            time.sleep(25)

            self.assertTrue(self.page.actionInstantRecord(10), "   ERR   cannot instant record")

            self.assertTrue(self.page.checkLive(), "   ERR   live not detected")

            self.assertFalse(self.page.zapToChannel(self.rc.getChannelBBCHD), "   ERR   cannot zap to " + self.rc.getChannelBBCHD)

            self.assertFalse(self.page.checkLive(), "   ERR   channel displays correctly")

            self.logStepResults("instant recording on channel 1, live on channel 2")

            self.page.sleep(660)

            self.logStepBeginning("after record is made go and play it")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records")
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            title = self.page.getInfoFromRecordPage()
            self.assertIsNotNone(title, "   ERR   cannot get info from record page")
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
