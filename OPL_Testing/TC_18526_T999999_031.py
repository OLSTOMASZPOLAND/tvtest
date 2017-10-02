# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import time

class TC_18526_T999999_031(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18526 - T999999 _W_and_R_bez_TS_najpierw_live_na_kanale_1_instant_na_kanale_2
    
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
            if not self.page.setSatVectors(2):
                if not self.page.setSatVectors(2):
                    self.fail("   ERR   SAT cables connected incorrectly")

            ''' step '''
            self.logStepBeginning("live on channel {},start instant recording on channel {}".format(self.rc.getChannelTVPPolonia, self.rc.getChannelBBCHD))
            
            time.sleep(5)

            self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVPPolonia), "   ERR   cannot zap to {}".format(self.rc.getChannelTVPPolonia))

            time.sleep(30)

            self.assertTrue(self.page.checkLive(), "   ERR   live not detected")

            time.sleep(30)
            
            self.assertTrue(self.page.checkLive(), "   ERR   live not detected")
            
            self.assertTrue(self.page.zapToChannel(self.rc.getChannelBBCHD), "   ERR   cannot zap to {}".format(self.rc.getChannelBBCHD))
            
            time.sleep(10)
            
            self.rc.sendKeys(["KEY_INFO"])
            time.sleep(2)
            
            item = self.page.getInfoFromLiveBanner()
            
            if not item:
                self.fail("   ERR   cannot get info from live banner")
            
            self.rc.sendKeys(["KEY_RECORD"])
            
            time.sleep(25)
            
            self.assertTrue(self.page.actionInstantRecord(10), "   ERR   cannot instant record")
            
            self.logStepResults("live on channel {},start instant recording on channel {}".format(self.rc.getChannelTVPPolonia, self.rc.getChannelBBCHD))

            self.page.sleep(660)

            self.logStepBeginning("after record is made go and play it")

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records")
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            title = self.page.getInfoFromRecordPage()
            self.assertIsNotNone(title, "   ERR   cannot get info from record page")
            self.assertEqual(title.getTitle(), item.getProgram(), "   ERR   title mismatch, record is not made")

            self.rc.sendKeys(["KEY_OK"])

            self.page.sleep(100)

            self.assertTrue(self.page.checkLive(True), "   ERR   motion not detected")

            self.page.sleep(100)

            self.assertTrue(self.page.checkLive(True), "   ERR   motion not detected")
            
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

    def getRecordTime(self):
        a = self.page.getInfoFromTrickBar()
        if a != None:
            a = a.getMinutesInSecondRow()
            if type(a) == int:
                return a
        else:
            self.fail("   ERR   cannot get time")
