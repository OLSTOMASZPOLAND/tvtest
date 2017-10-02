# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import datetime
import time

class TC_18518_T999999_023_PVR(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18517 - T999999  
    
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
            if not self.page.setSatVectors(1):
                if not self.page.setSatVectors(1):
                    self.fail("   ERR   SAT cables connected incorrectly")

            ''' step '''
            self.logStepBeginning("zap to {} and schedule future recording on channel {}".format(firstChannel, firstChannel))

            self.page.goToPvrMenu()
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "   ERR   cannot go to " + Menu.pvrManualRecord)

            start = datetime.datetime.now() + datetime.timedelta(minutes=5)
            item = self.page.actionScheduleRecord(firstChannel, start, 10, 0)
            self.assertTrue(item, "   ERR   cannot schedule a record")

            self.rc.sendKeys(["KEY_TV"])

            self.logStepBeginning("zap to {} and schedule future recording on channel {}".format(firstChannel, firstChannel))
            
            self.assertTrue(self.page.checkLive(), "   ERR   motion not detected")
            self.page.sleep(360)
            
            self.logStepBeginning("try starting TS session, it shouldnt work")

            self.rc.sendKeys(["KEY_PLAY"])
            
            time.sleep(10)
            
            trickBar = self.page.getInfoFromTrickBar()
            self.assertIsNone(trickBar, "   ERR   workaround is not working")
            
            self.logStepResults("try starting TS session, it shouldnt work")
            
            self.page.sleep(6000)

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
