# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import datetime
import time
from NewTvTesting.Config import *
from datetime import timedelta

class TC_3214_T016689_Delete_an_in_progress_record(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3214 - _T016689_Delete an in progress recording
    
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
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])                
                self.page.cleanDeleteAllRecordings()

            ''' step '''
            self.logStepBeginning("set record and wait until it starts")

            self.assertTrue(self.page.goToPvrMenu(), "   ERR   not in pvr menu")
            time.sleep(5)
            self.page.actionSelect(Menu.pvrManualRecord)
            time.sleep(5)

            startTime = datetime.datetime.now() + timedelta(minutes=6)

            self.assertTrue(self.page.actionScheduleRecord(self.rc.getChannelTVPPolonia, startTime, 15, 0, "test"), "   ERR   cannot set record in future")
            self.assertTrue(self.page.goToPvrMyScheduled(shouldBeEmpty=False), "   ERR   cannot go to my scheduled recordings mosaic")
            self.rc.sendKeys(["KEY_OK"])
            item = self.page.getInfoFromRecordPage()

            # check item
            self.assertTrue(item.getTitle() == "test", "   ERR   title mismatch")
            self.assertTrue(str(item.getDate()).rsplit(':', 1)[0] == str(startTime).rsplit(':', 1)[0], "   ERR   start date mismatch")
            self.assertTrue(item.getLength().seconds / 60 == 15, "   ERR   length mismatch")

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

            self.page.sleep(480)

            self.logStepResults("set record and wait until it starts")

            self.logStepBeginning("STEP 3,4,5 - stop a record")

            self.page.goToMenu()
            self.page.actionSelect(Menu.pvr)
            self.page.actionSelect(Menu.pvrMyRecords)
            time.sleep(15)
            item = self.page.getInfoFromRecordFocus()
            if not item:
                self.fail("   ERR   cannot get info about record")
            self.assertTrue(item.getRecording(), "   ERR   no record in progress")
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(10)
            item = self.page.getInfoFromRecordPage()
            if not item:
                self.fail("   ERR   cannot get info about record")
            self.assertTrue(item.getRecording(), "   ERR   no record in progress")
            self.assertTrue(self.page.deletePvrRecord(True), "   ERR   cannot delete running record")
            time.sleep(15)

            item = self.page.getInfoFromRecordFocus()
            if item != None:
                self.assertFalse(item.getRecording(), "   ERR   record is in progress ")
            else:
                if not self.page.goToPvrMyRecords(shouldBeEmpty=True):
                    self.fail("   ERR   cannot verify records")

            self.logStepResults("STEP 3,4,5 - stop a record")

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("error occurred - %s" % e)
            self.logger.info("error occurred - %s - cleaning" % e)
            raise

        finally:
            if not self.test_passed:
                self.logger.info("----------- cleaning -----------")
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                self.page.cleanDeleteAllRecordings()
