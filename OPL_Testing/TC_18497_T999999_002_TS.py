# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import time

class TC_18497_T999999_002_TS(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18497 - _TC_T099999 - W&R z TS. najpierw live na kanale 1, instant PVR na kanale 2
    
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
            self.logStepBeginning("set instant record and choose no in conflict popup")

            self.rc.sendKeys(["KEY_RECORD"])
            self.page.sleep(30)

            self.assertTrue(self.page.findInDialogBox(Menu.conflictAttention), "   ERR   no conflict attention popup")
            self.assertTrue(self.page.actionSelect(Menu.pvrNo), "   ERR   cannot select {}".format(Menu.pvrNo))

            self.logStepResults("set instant record and choose no in conflict popup")

            self.logStepBeginning("check if TS session works correctly")

            self.page.sleep(60)

            trickBar = self.page.getInfoFromTrickBar()
            self.assertIsNotNone(trickBar, "   ERR   cannot get info from a trick bar")
            trickBar = trickBar.getTrickIcon()
            self.assertEqual(trickBar, "Pause", "   ERR   can't find pause symbol")

            self.rc.sendKeys(["KEY_PLAY"])

            self.page.sleep(30)
            self.assertTrue(self.page.checkLive(), "   ERR   motion detection failed")
            self.page.sleep(180)
            self.assertTrue(self.page.checkLive(), "   ERR   motion detection failed")

            self.rc.sendKeys(["KEY_PLAY"])
            recordTime = self.getRecordTime()
            self.assertNotEqual(recordTime, 0, "   ERR   time shifting is not working")

            self.logStepResults("check if TS session works correctly")

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

    def getRecordTime(self):
        foo = self.page.getInfoFromTrickBar()
        if foo is not None:
            foo = foo.getMinutesInSecondRow()
        if type(foo) == int:
            return foo
        else:
            self.fail("   ERR   cannot get time from a trickbar")
