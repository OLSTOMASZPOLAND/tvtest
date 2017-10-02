# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import datetime
import time
from NewTvTesting.Config import *
from datetime import timedelta

class TC_3113_T016688__Delete_a_no_start_record_in_my_scheduled_rocordings_mosaic(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3113 - _T016688_Delete a no start record-V1
    
        Purpose: Delete_a_no_start_record_in_my_scheduled_recordings_mosaic
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")
        self.page.cleanDeleteAllRecordings()

        ''' step '''
        self.logStepBeginning("set record in future")
        try:
            self.page.zapToChannel(self.rc.getChannelTVPPolonia)
            self.rc.sendKeys(["KEY_GREEN"])
            time.sleep(5)
            self.page.actionSelect(Menu.pvrManualRecord)
            time.sleep(5)

            startTime = datetime.datetime.now() + timedelta(minutes=30)

            self.assertTrue(self.page.actionScheduleRecord(self.rc.getChannelTVPPolonia, startTime, 15, 0, "test"), "   ERR   cannot set record in future")
            self.assertTrue(self.page.goToPvrMyScheduled(shouldBeEmpty=False), "   ERR   cannot go to my scheduled recordings mosaic")
            self.rc.sendKeys(["KEY_OK"])
            item = self.page.getInfoFromRecordPage()

            # check item
            self.assertTrue(item.getTitle() == "test", "   ERR   title mismatch")
            self.assertTrue(str(item.getDate()).rsplit(':', 1)[0] == str(startTime).rsplit(':', 1)[0], "   ERR   start date mismatch")
            self.assertTrue(item.getLength().seconds / 60 == 15, "   ERR   length mismatch")

            time.sleep(10)

            self.logStepResults("set record in future")

            ''' step '''
            self.logStepBeginning("STEP - 3 delete a not yet started record and check if its actually deleted")

            self.assertTrue(self.page.actionSelect(Menu.pvrDelete), "   ERR   cannot find delete button")
            
            time.sleep(3)

            self.assertTrue(self.page.findInDialogBox(DialogBox.PvrDeleteRecord), "   ERR   cannot find confirmation popup")

            self.assertTrue(self.page.actionSelect(Menu.pvrYes), "   ERR   cannot find YES button")
            
            time.sleep(5)            

            self.assertTrue(self.page.goToPvrMyScheduled(shouldBeEmpty=True), "   ERR   item is still in planned records")

            self.logStepResults("STEP - 3 delete a not yet started record and check if its actually deleted")
            
        except Exception, e:
            self.logStepResults("error occurred - %s" % e)
            self.logger.info("error occurred - %s - cleaning" % e)
            if self.page.goToPvrMyScheduled():
                self.page.deletePvrRecord()
            raise
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
