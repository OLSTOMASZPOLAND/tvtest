# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
import datetime
import time

class TC_3220_T016764_Ongoing_record_zap_to_program_on_different_channel(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3220 - T016764_Ongoing record IP or DTT _zap to program on DTT or IP on different channel-V1

        Purpose:    Ongoing_record_IP_or_DTT_zap_to_program_on_DTT_or_IP_on_different_channel
                In this case, W&R conflict is NOT detected
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        if not (Env.ZONE == "DTH" or Env.ZONE == "IPTV" or Env.ZONE == "FTTH"):
            self.fail("   ERR   cannot run test on current technology: " + Env.ZONE)
            
        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''''''''''''''
        '''SETTINGS'''
        ''''''''''''''
        firstRunChannelOnIPTV = self.rc.getChannelTVP1HD  
        firstRunChannelOnDTT = self.rc.getChannelTVP1HD_dtt
        secondRunChannelOnIPTV = self.rc.getChannelTVP2HD
        secondRunChannelOnDTT = self.rc.getChannelTVP2HD_dtt

        ''' step '''
        self.logStepBeginning("PRESTEP - enable and search for DTT channels")

        self.assertTrue(self.page.setDTTChannels(True), "   ERR   cannot turn on DTT channels")
        self.page.cleanDeleteAllRecordings()

        self.logStepResults("PRESTEP - enable and search for DTT channels")

        self.runTest(firstRunChannelOnIPTV, firstRunChannelOnDTT)
        self.runTest(secondRunChannelOnDTT, secondRunChannelOnIPTV)

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

    def runTest(self, firstChannel, secondChannel):
        try:
            self.logger.info("###########   runTest  firstChannel>%s<   secondChannel>%s<    ########### " % (firstChannel, secondChannel))
            
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            time.sleep(2)

            ''' step '''
            self.logStepBeginning("STEP - start recording first channel and zap to second channel")
            
            self.assertTrue(self.page.zapToChannel(firstChannel), "   ERR   cannot zap to first channel")

            if Env.VIDEO:
                self.assertTrue(self.page.checkLive(), "   ERR   motion not detected")

            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(25)
            self.assertTrue(self.page.actionInstantRecord(), "   ERR   cannot set instant record")
            time.sleep(20)
            self.assertTrue(self.page.zapToChannel(secondChannel), "   ERR   cannot zap to second channel")

            if Env.VIDEO:
                self.assertTrue(self.page.checkLive(), "   ERR   motion not detected")

            self.logStepResults("STEP - start recording first channel and zap to second channel")

            ''' step '''
            self.logStepBeginning("STEP - stop recording of first channel, start recording on second channel and go back to watch first channel")

            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(5)
            
            currTime = datetime.datetime.now()
            
            while not self.page.findInDialogBox(Menu.vodInfo):  
                if ((datetime.datetime.now() - currTime).seconds > 300):
                    self.fail("   ERR   cannot stop recording")
                    
            self.assertTrue(self.page.actionSelect(Menu.pvrStopRecord), "   ERR   cannot stop recording")

            time.sleep(30)

            if(self.page.findInDialogBox(Menu.pvrStopRecordConfirm)):
                self.rc.sendKeys(["KEY_OK"])
            else:
                self.assertTrue(False, "   ERR   cannot stop recording")

            time.sleep(5)

            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(15)

            self.assertTrue(self.page.actionInstantRecord(), "   ERR   cannot instant record")

            time.sleep(15)

            self.assertTrue(self.page.zapToChannel(firstChannel), "   ERR   cannot zap to first channel")

            if Env.VIDEO:
                self.assertTrue(self.page.checkLive(), "   ERR   motion not detected")

            self.logStepResults("STEP - stop recording of first channel, start recording on second channel and go back to watch first channel")

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
