# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.StbtIntegration import *
from NewTvTesting.Config import *

class TC_18499_T999999_004(TC_OPL_template):
    '''Implementation of the HP QC test ID - 23098 - T999999_Najpierw_live_na_kanale_1_instant_pvr_na_kanale_2
    
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

            firstChannel = self.rc.getChannelTVPPolonia
            secondChannel = self.rc.getChannelBBCHD

            ''' step '''
            self.logStepBeginning("zap to channel {} and instant record on channel {}".format(firstChannel, secondChannel))

            self.assertTrue(self.page.zapToChannel(firstChannel), "   ERR   cannot zap to {}".format(firstChannel))

            self.assertTrue(self.page.checkLive(), "   ERR   motion detection failed")

            self.assertTrue(self.page.zapToChannel(secondChannel), "   ERR   cannot zap to {}".format(secondChannel))

            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(25)
            self.assertTrue(self.page.actionInstantRecord(10), "   ERR:   cannot set instant record")

            self.rc.sendKeys(["KEY_INFO"])
            item = self.page.getInfoFromLiveBanner()
            self.assertIsNotNone(item, "   ERR   cannot get info from live banner")

            self.logStepResults("zap to channel {} and instant record on channel {}".format(firstChannel, secondChannel))

            ''' step '''
            self.logStepBeginning("wait until record finish")

            self.assertTrue(self.page.checkLive(), "   ERR   motion detection failed")

            self.page.sleep(120)

            self.assertTrue(self.page.checkLive(), "   ERR   motion detection failed")

            self.page.sleep(140)

            self.assertTrue(self.page.checkLive(), "   ERR   motion detection failed")

            self.page.sleep(400)

            self.logStepResults("wait until record finish")

            '''step'''
            self.logStepBeginning("after record is made go and play it")
            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records")

            self.rc.sendKeys(["KEY_OK"])
            self.page.sleep(5)
            title = self.page.getInfoFromRecordPage()
            self.assertIsNotNone(title, "   ERR   cannot get info from record page")

            title1 = self.page.simplifyProgramTitle(title.getTitle())
            title2 = self.page.simplifyProgramTitle(item.getProgram())

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
                self.page.cleanDeleteAllRecordings()
