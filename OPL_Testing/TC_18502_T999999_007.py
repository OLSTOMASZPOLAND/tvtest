# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import time
import datetime

class TC_18502_T999999_007(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18502 - _TC_T099999 - W_and_R_bez_TS_scheduled_na_kanale_2_live_na_kanale_1_zanim_wlaczy_sie_nagranie
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")
            
            firstChannel = self.rc.getChannelBBCHD
            secondChannel = self.rc.getChannelTVPPolonia

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            if not self.page.cleanDeleteAllRecordings():
                self.page.cleanDeleteAllRecordings()
            if not self.page.setSatVectors(3):
                if not self.page.setSatVectors(3):
                    self.fail("   ERR   SAT cables connected incorrectly")

            ''' step '''
            self.logStepBeginning("zap to {} and schedule future recording on channel {}".format(firstChannel, secondChannel))

            self.assertTrue(self.page.zapToChannel(firstChannel), "   ERR   cannot zap to channel {}".format(firstChannel))

            self.page.goToPvrMenu()
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "   ERR   cannot go to " + Menu.pvrManualRecord)

            start = datetime.datetime.now() + datetime.timedelta(minutes=8)
            
            time.sleep(5)
            item = self.page.actionScheduleRecord(secondChannel, start, 10, 0)
            self.assertTrue(item, "   ERR   cannot schedule a record")

            self.rc.sendKeys(["KEY_TV"])
            self.page.sleep(200)
            self.assertTrue(self.page.checkLive(), "   ERR   live is not playing")
            self.page.sleep(200)
            self.assertTrue(self.page.checkLive(), "   ERR   live is not playing")
            self.page.sleep(560)
            self.assertTrue(self.page.checkLive(), "   ERR   live is not playing")

            self.logStepResults("zap to {} and schedule future recording on channel {}".format(firstChannel, secondChannel))

            self.logStepBeginning("after record is made go and play it")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records")

            self.rc.sendKeys(["KEY_OK"])
            record = self.page.getInfoFromRecordPage()
            self.assertIsNotNone(record, "   ERR   cannot get info about record")
            self.assertEqual(item, record.getTitle(), "   ERR   title mismatch, record is not made")
            self.rc.sendKeys(["KEY_OK"])
            self.page.sleep(100)
            self.assertTrue(self.page.checkLive(), "   ERR   pvr is not playing")
            self.page.sleep(100)
            self.assertTrue(self.page.checkLive(), "   ERR   pvr is not playing")
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
