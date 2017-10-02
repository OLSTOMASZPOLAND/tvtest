# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import time

class TC_18501_T999999_006_PVR(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18501 - _TC_T099999 - W_and_R_z_TS_najpierw_instant_na_kanale_1_live_na_kanale_2_i_TS
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:

            firstChannel = self.rc.getChannelBBCHD
            secondChannel = self.rc.getChannelTVPPolonia

            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            if not self.page.cleanDeleteAllRecordings():
                self.page.cleanDeleteAllRecordings()
            if not self.page.setSatVectors(3):
                if not self.page.setSatVectors(3):
                    self.fail("   ERR   SAT cables connected incorrectly")

            ''' step '''
            self.logStepBeginning("set instant record")
            self.assertTrue(self.page.zapToChannel(firstChannel), "   ERR   cannot zap to {}".format(firstChannel))
            self.rc.sendKeys(["KEY_INFO"])
            item = self.page.getInfoFromLiveBanner()
            self.assertIsNotNone(item, "   ERR   cannot get info from live banner")
            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(20)
            self.assertTrue(self.page.actionInstantRecord(10), "   ERR   cannot set instant record")
            self.logStepResults("set instant record")

            ''' step '''
            self.logStepBeginning("zap to channel {} and start TS, shouldnt work".format(secondChannel))
            self.assertTrue(self.page.zapToChannel(secondChannel), "   ERR   cannot zap to " + str(secondChannel))

            time.sleep(10)

            self.rc.sendKeys(["KEY_PLAY"])

            time.sleep(10)

            trickBar = self.page.getInfoFromTrickBar()
            self.assertIsNone(trickBar)  # RA workaround

            self.logStepResults("zap to channel {} and start TS, shouldnt work".format(secondChannel))

            self.page.sleep(660)

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
                if not self.page.cleanDeleteAllRecordings():
                    self.page.cleanDeleteAllRecordings()
