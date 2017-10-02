# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import datetime
import time
from __builtin__ import str

class TC_18506_T999999_011(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18506 - T999999 scheduled z pokrywaniem sie nagran
    
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
            if not self.page.setSatVectors(3):
                if not self.page.setSatVectors(3):
                    self.fail("   ERR   SAT cables connected incorrectly")
            ''' step '''
            self.logStepBeginning("Set future record on channel 1")

            self.assertTrue(self.page.goToPvrMenu(), "   ERR   cannot go to future records menu")
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "   ERR   cannot select " + Menu.pvrManualRecord)
            start = datetime.datetime.now() + datetime.timedelta(minutes=5)
            time.sleep(5)
            title1 = self.page.actionScheduleRecord(1, start, 10)
            self.assertIsNotNone(title1, "   ERR   cannot schedule a record")

            self.logStepResults("Set future record on channel 1")

            ''' step '''
            self.logStepBeginning("Set conflicting future record on the same channel")

            self.assertTrue(self.page.goToPvrMenu(), "   ERR   cannot go to future records menu")
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "   ERR   cannot select " + Menu.pvrManualRecord)
            time.sleep(5)
            self.assertFalse(self.page.actionScheduleRecord(2, start, 10, 0), "   ERR   I was able to make conflict schedule")
            self.assertTrue(self.page.findInDialogBox(DialogBox.PvrScheduleError), "   ERR   no conflict popup")
            self.rc.sendKeys(["KEY_OK", "KEY_TV"])

            self.logStepResults("Set conflicting future record on the same channel")

            self.page.sleep(960)

            ''' step '''
            self.logStepBeginning("after record is made go and play it")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records")

            self.rc.sendKeys(["KEY_OK"])
            time.sleep(10)
            title2 = self.page.getInfoFromRecordPage()

            self.assertIsNotNone(title2, "   ERR   cannot get info from record page")
            title2 = self.page.simplifyProgramTitle(title2.getTitle())
            title1 = self.page.simplifyProgramTitle(title1)

            self.assertTrue(title1 == title2, "   ERR   title mismatch, record is not made")

            self.rc.sendKeys(["KEY_OK"])
            self.page.sleep(100)
            self.assertTrue(self.page.checkLive(True), "   ERR   pvr is not playing")
            self.page.sleep(100)
            self.assertTrue(self.page.checkLive(True), "   ERR   pvr is not playing")
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
