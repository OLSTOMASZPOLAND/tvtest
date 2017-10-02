# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import datetime
import time

class TC_18513_T999999_018(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18513 - T999999 W&R bez TS na kanale 1 LIVE - UHD86
    
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
            if not self.page.setSatVectors(1):
                if not self.page.setSatVectors(1):
                    self.fail("   ERR   SAT cables connected incorrectly")

            ''' step '''
            self.logStepBeginning("Set instant record on channel {}".format(self.rc.getChannelBBCHD))

            self.assertTrue(self.page.zapToChannel(self.rc.getChannelBBCHD), "   ERR   cannot zap to " + self.rc.getChannelBBCHD)
            time.sleep(10)
            self.rc.sendKeys(["KEY_RECORD"])

            time.sleep(25)
            self.assertTrue(self.page.actionInstantRecord(10), "   ERR   cannot set instant record")
            self.rc.sendKeys(["KEY_INFO"])
            time.sleep(5)
            item = self.page.getInfoFromLiveBanner()
            self.assertIsNotNone(item, "   ERR   cannot get info from live banner")
            item.display()
            
            self.logStepResults("Set instant record on channel {}".format(self.rc.getChannelBBCHD))
            
            self.logStepBeginning("Wait until record is finished and check if live channel displays correctly")

            self.page.sleep(120)

            self.assertTrue(self.page.checkLive(), "   ERR   live not detected")

            self.page.sleep(140)

            self.assertTrue(self.page.checkLive(), "   ERR   live not detected")
            
            self.page.sleep(400)

            self.logStepResults(("Wait until record is finished and check if live channel displays correctly"))

            self.logStepBeginning("When record is finished, go and watch it")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records")
            time.sleep(10)

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

            self.page.sleep(120)

            self.assertTrue(self.page.checkLive(True), "   ERR   motion not detected")

            self.page.sleep(120)

            self.assertTrue(self.page.checkLive(True), "   ERR   motion not detected")

            self.rc.sendKeys(["KEY_BACK"])

            self.page.deletePvrRecord()

            self.logStepResults("When record is finished, go and watch it")

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
