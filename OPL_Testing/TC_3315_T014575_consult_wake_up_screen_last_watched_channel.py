# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import datetime
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
from NewTvTesting.Utils import *

class TC_3315_T014575_consult_wake_up_screen_last_watched_channel(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3315 - _T014575_Consult Wake-up screen - last watched channel
    
    Purpose: the wake up screen is displayed with the last watched channel
    @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("prerequisites")
        self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVPPolonia), "   ERR:   cannot zap to channel " + self.rc.getChannelTVPPolonia)
        self.logStepResults("prerequisites")
        
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(30)

        ''' step '''
        self.logStepBeginning("STEP 3 - power on STB and wait for wake up screen")
        self.rc.sendKeys(["KEY_POWER"])

        time.sleep(3)

        currTime = datetime.datetime.now()

        while not self.page.findInCssSelectorElement("TVP Polonia", ".bannerFlux .channel"):
            time.sleep(3)
            self.assertTrue((datetime.datetime.now() - currTime).seconds < 300, "   ERR   cannot find wake up screen with channel " + self.rc.getChannelTVPPolonia)

        time.sleep(5)

        self.logStepResults("STEP 3 - power on STB and wait for wake up screen")
        
        ''' step '''
        self.logStepBeginning("STEP 4,5,6 - check the last watched channel zone, press OK and check if channel displays in fullscreen")

        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        time.sleep(5)
        self.assertTrue(self.page.checkLive(), "   ERR:   Fullscreen live is not displaying")

        self.logStepResults("STEP 4,5,6 - check the last watched channel zone, press OK and check if channel displays in fullscreen")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
