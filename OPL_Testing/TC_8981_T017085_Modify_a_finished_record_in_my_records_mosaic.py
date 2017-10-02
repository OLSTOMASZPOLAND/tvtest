# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import datetime
import time
from NewTvTesting.Config import *
from datetime import timedelta

class TC_8981_T017085_Modify_a_finished_record_in_my_records_mosaic(TC_OPL_template):
    '''Implementation of the HP QC test ID - 8981 - T017085_Modify_a_finished_record_in_my_records_mosaic
    
        Purpose: Modify_a_finished_record_in_my_records_mosaic
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
            self.logStepBeginning("set record and wait until it finish")

            self.page.zapToChannel(self.rc.getChannelTVPPolonia)
            self.page.goToPvrMenu()
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "   ERR    cannot select " + Menu.pvrManualRecord)
            time.sleep(5)

            startTime = datetime.datetime.now() + timedelta(minutes=8)

            self.assertTrue(self.page.actionScheduleRecord(self.rc.getChannelTVPPolonia, startTime, 10, 0, "test"), "   ERR   cannot set record in future")
            self.assertTrue(self.page.goToPvrMyScheduled(shouldBeEmpty=False), "   ERR   cannot go to my scheduled recordings mosaic")
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(3)
            item = self.page.getInfoFromRecordPage()
            if not item:
                self.fail("   ERR   cannot get info from record focus")
            # check item
            self.assertTrue(item.getTitle() == "test", "   ERR   title mismatch")
            self.assertTrue(str(item.getDate()).rsplit(':', 1)[0] == str(startTime).rsplit(':', 1)[0], "   ERR   start date mismatch")
            self.assertTrue(item.getLength().seconds / 60 == 10, "   ERR   length mismatch")

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

            self.logStepResults("set record and wait until it finish")

            self.page.sleep(1080)

            ''' step '''
            self.logStepBeginning("STEP - 3,4 select MODIFIER, change record title and validate it")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   not in my Records")
            time.sleep(5)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            self.assertTrue(self.page.actionSelect(Menu.pvrChange), "   ERR   cannot find modify button")
            time.sleep(10)

            self.assertTrue(self.page.findInCssSelectorElement(Menu.pvrManualRecord, ".breadcrumb .last"), "   ERR   not in record planning")

            self.rc.sendKeys(["KEY_LEFT", "KEY_LEFT" , "KEY_LEFT", "KEY_LEFT", "KEY_LEFT"])  # delete previous name

            self.rc.sendWord("abcd")

            self.rc.sendKeys(["KEY_DOWN", "KEY_OK"])

            time.sleep(5)

            self.assertTrue(self.page.findInDialogBox(Menu.pvrChangeConfirm), "   ERR   no confirmation popup")
            self.rc.sendKeys(["KEY_OK"])

            time.sleep(10)

            item = self.page.getInfoFromRecordPage()

            # check item
            self.assertTrue(item.getTitle() == "abcd", "   ERR   title mismatch")
            self.assertTrue(str(item.getDate()).rsplit(':', 1)[0] == str(startTime).rsplit(':', 1)[0], "   ERR   start date mismatch")
            self.assertTrue(item.getLength().seconds / 60 == 10, "   ERR   length mismatch")

            time.sleep(5)

            self.logStepResults("STEP - 3,4 select MODIFIER, change record title and validate it")

            ''' step '''
            self.logStepBeginning("STEP - 5 check if title in mosaic changed")

            self.rc.sendKeys(["KEY_BACK"])

            time.sleep(5)
            self.page.driver.refresh()

            item = self.page.getInfoFromRecordFocus()
            item = item.getTitle()
            self.assertTrue(item == "abcd", "   ERR   title mismatch")

            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)

            self.page.deletePvrRecord()

            self.logStepResults("STEP - 5 check if title in mosaic changed")

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
