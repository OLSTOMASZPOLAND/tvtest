# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import time

class TC_18500_T999999_005(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18500 - _TC_T099999 - W&R z TS. najpierw live na kanale 1, instant PVR na kanale 1
    
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
            if not self.page.setSatVectors(3):
                if not self.page.setSatVectors(3):
                    self.fail("   ERR   SAT cables connected incorrectly")

            ''' step '''
            self.logStepBeginning("zap to channel {} and start TS".format(firstChannel))
            self.assertTrue(self.page.zapToChannel(firstChannel), "   ERR   cannot zap to channel {}".format(firstChannel))
            self.rc.sendKeys(["KEY_PLAY"])

            time.sleep(10)

            trickBar = self.page.getInfoFromTrickBar()
            self.assertIsNotNone(trickBar, "   ERR   cannot get info from a trick bar")
            trickBar = trickBar.getTrickIcon()
            self.assertEqual(trickBar, "Pause", "   ERR   can't find pause symbol")
            self.logStepBeginning("zap to channel {} and start TS".format(firstChannel))

            ''' step '''
            self.logStepBeginning("set instant record on channel {}".format(firstChannel))

            self.rc.sendKeys(["KEY_RECORD"])

            time.sleep(20)

            self.assertTrue(self.page.findInDialogBox(Menu.conflictAttention), "   ERR   no conflict attention popup")
            self.assertTrue(self.page.actionSelect(Menu.pvrYes), "   ERR   cannot select " + Menu.pvrYes)

            time.sleep(20)

            self.assertTrue(self.page.actionInstantRecord(10), "   ERR   cannot set instant record")

            self.rc.sendKeys(["KEY_INFO"])
            item = self.page.getInfoFromLiveBanner()
            self.assertIsNotNone(item, "   ERR   cannot get info from live banner")
            trickBar = self.page.getInfoFromTrickBar()
            self.assertIsNone(trickBar, "   ERR   workaround is not working, TS session is still up")
            time.sleep(10)
            self.assertTrue(self.page.checkLive(False), "   ERR   live is not playing")
            self.page.sleep(160)
            self.assertTrue(self.page.checkLive(False), "   ERR   live is not playing")

            self.logStepResults("set instant record on channel {}".format(firstChannel))

            self.page.sleep(500)

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
