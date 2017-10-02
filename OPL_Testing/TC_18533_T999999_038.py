# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import datetime
import time

class TC_18533_T999999_038(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18533 - T999999 W&R bez TS na kanale 1 LIVE - UHD86
    
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
            self.logStepBeginning("Set schedule record on channel " + str(self.rc.getChannelTVPPolonia))

            self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVPPolonia), "   ERR   cannot zap to " + str(self.rc.getChannelTVPPolonia))

            self.assertTrue(self.page.goToPvrMenu(), "   ERR   cannot go to pvr menu")
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "   ERR   cannot select " + Menu.pvrManualRecord)
            start = datetime.datetime.now() + datetime.timedelta(minutes=5)
            
            time.sleep(5)
            item = self.page.actionScheduleRecord(self.rc.getChannelTVPPolonia, start, 10)
            self.assertTrue(item , "   ERR   cannot set scheduled record")
            
            self.rc.sendKeys(["KEY_TV"])

            self.page.sleep(200)

            self.assertTrue(self.page.checkLive(), "   ERR   live not detected")

            self.page.sleep(260)

            self.assertTrue(self.page.checkLive(), "   ERR   live not detected")

            self.logStepResults("Set schedule record on channel " + str(self.rc.getChannelTVPPolonia))

            self.page.sleep(500)

            self.logStepBeginning("after record is made go and play it")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records")
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            title = self.page.getInfoFromRecordPage()
            self.assertIsNotNone(title, "   ERR   cannot get info from record page")
            self.assertEqual(title.getTitle(), item, "   ERR   title mismatch, record is not made")

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
