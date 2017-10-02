# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import datetime
import time
from NewTvTesting.Config import *
from datetime import timedelta

class TC_8979_T016692_Modify_a_no_start_record_in_my_scheduled_recordings_mosaic(TC_OPL_template):
    '''Implementation of the HP QC test ID - 8979 - T016692_Modify a no start record-V1
        
        Purpose: Modify_a_no_start_record_in_my_scheduled_recordings_mosaic
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        try:
            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            self.page.cleanDeleteAllRecordings()

            ''' step '''
            self.logStepBeginning("set record in future")
            self.page.zapToChannel(self.rc.getChannelTVPPolonia)

            self.assertTrue(self.page.goToPvrMenu(), "   ERR   not in pvr menu")
            time.sleep(5)
            self.page.actionSelect(Menu.pvrManualRecord)
            time.sleep(5)

            startTime = datetime.datetime.now() + timedelta(minutes=30)

            self.assertTrue(self.page.actionScheduleRecord(self.rc.getChannelTVPPolonia, startTime, 15, 0, "test"), "   ERR   cannot set record in future")
            self.assertTrue(self.page.goToPvrMyScheduled(shouldBeEmpty=False), "   ERR   cannot go to my scheduled recordings mosaic")
            time.sleep(5)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            item = self.page.getInfoFromRecordPage()

            # check item
            self.assertTrue(item.getTitle() == "test", "   ERR   title mismatch")
            self.assertTrue(str(item.getDate()).rsplit(':', 1)[0] == str(startTime).rsplit(':', 1)[0], "   ERR   start date mismatch")
            self.assertTrue(item.getLength().seconds / 60 == 15, "   ERR   length mismatch")

            time.sleep(10)
            self.logStepResults("set record in future")

            ''' step '''
            self.logStepBeginning("STEP - 3,4 select MODIFIER, change record information and validate it")

            self.assertTrue(self.page.actionSelect(Menu.pvrChange), "   ERR   cannot find modify button")
            time.sleep(10)
            self.rc.sendKeys(["KEY_LEFT", "KEY_LEFT" , "KEY_LEFT", "KEY_LEFT", "KEY_LEFT"])  # delete previous name

            startTime = datetime.datetime.now() + timedelta(minutes=8)

            self.assertTrue(self.page.actionScheduleRecord(self.rc.getChannelTVPPolonia, startTime, 10, 0, "aaa"), "   ERR   cannot modify record details")

            time.sleep(5)

            item = self.page.getInfoFromRecordPage()
            if not item:
                self.fail("   ERR   cannot get info from record focus")
            # check item
            self.assertTrue(item.getTitle() == "aaa", "   ERR   title mismatch")
            self.assertTrue(str(item.getDate()).rsplit(':', 1)[0] == str(startTime).rsplit(':', 1)[0], "   ERR   start date mismatch")
            self.assertTrue(item.getLength().seconds / 60 == 10, "   ERR   length mismatch")

            time.sleep(5)

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

            self.logStepResults("STEP - 3,4 select MODIFIER, change record information and validate it")

            ''' step '''
            self.logStepBeginning("STEP - 5 when defined record start time is reached, check the record status")

            self.page.sleep(500)

            self.page.goToPvrMenu()

            time.sleep(5)

            self.assertTrue(self.page.actionSelect(Menu.pvrMyRecords), "   ERR   cannot go to my records")

            time.sleep(10)

            self.rc.sendKeys(["KEY_OK"])

            time.sleep(5)

            item = self.page.getInfoFromRecordPage()
            # check item
            self.assertTrue(item.getTitle() == "aaa", "   ERR   title mismatch")
            self.assertTrue(str(item.getDate()).rsplit(':', 1)[0] == str(startTime).rsplit(':', 1)[0], "   ERR   start date mismatch")
            self.assertTrue(item.getLength().seconds / 60 == 10, "   ERR   length mismatch")
            self.assertTrue(item.getRecording() == True, "   ERR   recording mismatch")

            time.sleep(5)

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

            self.logStepResults("STEP - 5 when defined record start time is reached, check the record status")

            ''' step '''
            self.logStepBeginning("STEP - 6 when record is finished check its status")

            self.page.sleep(660)

            self.page.goToPvrMenu()

            time.sleep(5)

            self.assertTrue(self.page.actionSelect(Menu.pvrMyRecords), "   ERR   cannot go to my records")

            time.sleep(5)

            self.rc.sendKeys(["KEY_OK"])

            time.sleep(5)

            item = self.page.getInfoFromRecordPage()

            # check item
            self.assertTrue(item.getTitle() == "aaa", "   ERR   title mismatch")
            self.assertTrue(str(item.getDate()).rsplit(':', 1)[0] == str(startTime).rsplit(':', 1)[0], "   ERR   start date mismatch")
            self.assertTrue(item.getLength().seconds / 60 == 10, "   ERR   length mismatch")
            self.assertTrue(item.getRecording() == False, "   ERR   recording mismatch")

            self.page.deletePvrRecord()
            self.logStepResults("STEP - 6 when record is finished check its status")

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
