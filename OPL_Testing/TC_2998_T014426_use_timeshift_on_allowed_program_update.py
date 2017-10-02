# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time
from NewTvTesting.StbtIntegration import motionDetection

class TC_2998_T014426_use_timeshift_on_allowed_program_update(TC_OPL_template):
    '''Implementation of the HP QC test ID - 2998 - use_timeshift_on_allowed_program_update
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' step '''
        self.logStepBeginning("zap to channel and start timeshift tests")
	'''
	time.sleep(5)
        aa = motionDetection()
	print aa
        self.assertFalse(motionDetection(), "   ERR   channel is not paused")
	time.sleep(1000)
	'''
        self.page.zapToChannel(self.rc.getChannelBBCHD)
        self.assertTrue(self.page.checkLive(), "   ERR   live not detected")       
        if not self.page.zapToChannel(self.rc.getChannelTVPPolonia):
            self.page.zapToChannel(self.rc.getChannelTVPPolonia)
            
        time.sleep(15)
        
        #=======================================================================
        # for num in self.rc.getChannelBBCHD:
        #     self.rc.zap(channel)
        #=======================================================================

        self.rc.sendUrl(Rpi.URL_RPI_ZAP + self.rc.getChannelBBCHD)

        time.sleep(3)
        self.rc.sendKeys(["KEY_REWIND"])

        item = self.page.getInfoFromTrickBar()
        if not item:
            self.fail("   ERR   cannot get info from a trick bar")

        self.assertTrue(item.getTrickIcon() == "Forbidden", "   ERR   forbidden icon is not displaying")

        time.sleep(10)

        self.rc.sendKeys(["KEY_PLAY"])

	time.sleep(10)

        self.assertFalse(motionDetection(), "   ERR   channel is not paused")
        item = self.page.getInfoFromTrickBar()
        if not item:
            self.fail("   ERR   cannot get info from a trick bar (pause)")
        self.assertTrue(item.getTrickIcon() == "Pause", "   ERR   pause icon is not displaying")

        time.sleep(30 * 60)


        self.rc.sendUrl(Rpi.URL_RPI_KEY + "KEY_PLAY")
        time.sleep(3)
        item = self.page.getInfoFromTrickBar()
        if not item:
            self.fail("   ERR   cannot get info from a trick bar (play)")
        self.assertTrue(item.getTrickIcon() == "Play", "   ERR   play icon is not displaying")
        self.assertTrue(motionDetection(), "   ERR   channel is still paused")

        self.rc.sendKeys(["KEY_FORWARD"])
        time.sleep(3)
        item = self.page.getInfoFromTrickBar()
        if not item:
            self.fail("   ERR   cannot get info from a trick bar (forward4)")
        self.assertTrue(item.getTrickIcon() == "Forward4", "   ERR   forward4 icon is not displaying")

        self.rc.sendKeys(["KEY_FORWARD"])
        time.sleep(3)
        item = self.page.getInfoFromTrickBar()
        if not item:
            self.fail("   ERR   cannot get info from a trick bar (forward16)")
        self.assertTrue(item.getTrickIcon() == "Forward16", "   ERR   forward16 icon is not displaying")

        self.rc.sendKeys(["KEY_FORWARD"])
        time.sleep(3)
        item = self.page.getInfoFromTrickBar()
        if not item:
            self.fail("   ERR   cannot get info from a trick bar (forward32)")
        self.assertTrue(item.getTrickIcon() == "Forward32", "   ERR   forward32 icon is not displaying")

        self.rc.sendKeys(["KEY_FORWARD"])
        time.sleep(3)
        item = self.page.getInfoFromTrickBar()
        if not item:
            self.fail("   ERR   cannot get info from a trick bar (forward64)")
        self.assertTrue(item.getTrickIcon() == "Forward64", "   ERR   forward64 icon is not displaying")

        self.rc.sendKeys(["KEY_REWIND"])
        time.sleep(3)
        item = self.page.getInfoFromTrickBar()
        if not item:
            self.fail("   ERR   cannot get info from a trick bar (rewind4)")
        self.assertTrue(item.getTrickIcon() == "Rewind4", "   ERR   rewind4 icon is not displaying")

        self.rc.sendKeys(["KEY_REWIND"])
        time.sleep(3)
        item = self.page.getInfoFromTrickBar()
        if not item:
            self.fail("   ERR   cannot get info from a trick bar (rewind16)")
        self.assertTrue(item.getTrickIcon() == "Rewind16", "   ERR   rewind16 icon is not displaying")

        self.rc.sendKeys(["KEY_REWIND"])
        time.sleep(3)
        item = self.page.getInfoFromTrickBar()
        if not item:
            self.fail("   ERR   cannot get info from a trick bar (rewind32)")
        self.assertTrue(item.getTrickIcon() == "Rewind32", "   ERR   rewind32 icon is not displaying")

        self.rc.sendKeys(["KEY_REWIND"])
        time.sleep(3)
        item = self.page.getInfoFromTrickBar()
        if not item:
            self.fail("   ERR   cannot get info from a trick bar (rewind64)")
        self.assertTrue(item.getTrickIcon() == "Rewind64", "   ERR   rewind64 icon is not displaying")

        self.logStepResults("zap to channel and start timeshift tests")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
