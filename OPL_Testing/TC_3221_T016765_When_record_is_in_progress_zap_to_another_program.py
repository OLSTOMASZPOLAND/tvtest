# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import time

class TC_3221_T016765_When_record_is_in_progress_zap_to_another_program(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3221 - _T016765_Ongoing record_zap to program on different vector same channel

        Purpose:    When an ongoing record is in progress, zap to another program which is on different vector and on the same channel
                In this case, W&R conflict is NOT detected
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")
        
        if not (Env.ZONE == "DTH" or Env.ZONE == "IPTV" or Env.ZONE == "FTTH"):
            self.fail("   ERR   cannot run test on current technology: " + Env.ZONE)

        ''''''''''''''
        '''SETTINGS'''
        ''''''''''''''
        firstRunChannelOnIPTV = self.rc.getChannelTVP1HD  
        firstRunChannelOnDTT = self.rc.getChannelTVP1HD_dtt
        secondRunChannelOnIPTV = self.rc.getChannelTVP2HD
        secondRunChannelOnDTT = self.rc.getChannelTVP2HD_dtt

        ''' step '''
        self.logStepBeginning("PRESTEP - enable and search for DTT channels")

        self.assertTrue(self.page.setDTTChannels(True), "   ERR   cannot set DTT channel on")
        self.page.cleanDeleteAllRecordings()

        self.logStepResults("PRESTEP - enable and search for DTT channels")

        self.runTest(firstRunChannelOnIPTV, firstRunChannelOnDTT)
        self.page.cleanDeleteAllRecordings()
        self.runTest(secondRunChannelOnDTT, secondRunChannelOnIPTV)

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

    def runTest(self, firstChannel, secondChannel):
        try:
            self.logger.info("###########   runTest  firstChannel>%s<   secondChannel>%s<    ########### " % (firstChannel, secondChannel))

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            time.sleep(5)

            ''' step '''
            self.logStepBeginning("STEP - start recording first channel and zap to second channel")

            self.assertTrue(self.page.zapToChannel(firstChannel), "   ERR   cannot change to channel")

            if Env.VIDEO:
                self.assertTrue(self.page.checkLive(), "   ERR   motion not detected")

            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(25)
            self.assertTrue(self.page.actionInstantRecord(), "   ERR   cannot set instant record")
            time.sleep(20)
            self.assertTrue(self.page.zapToChannel(secondChannel), "   ERR   cannot change to channel")

            if Env.VIDEO:
                self.assertTrue(self.page.checkLive(), "   ERR   motion not detected")

            self.logStepResults("STEP - start recording first channel and zap to second channel")

            self.logger.info("##################################################################################################")

        except Exception, e:
            self.logStepResults("error occurred - %s" % e)
            self.logger.info("error occurred - %s - cleaning" % e)
            raise

        finally:
            if not self.test_passed:
                self.logger.info("----------- cleaning -----------")
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                self.page.cleanDeleteAllRecordings()
