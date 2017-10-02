# -*- coding: utf-8 -*-

import time
from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta

 

 

class TC_9476_T014345_Zap_to__basic_channel_wake_up_screen(TC_OPL_template):

    """              
    Implementation of the HP QC test ID - 9476_T014345_Zap_to__basic_channel_wake_up_screen
    @author: Tomasz Stasiuk
    """

       

    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)

   

    def test(self):
        
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

       

        ''' prestep '''

        self.logStepResults("AT_THE_BEGINNING")
        time.sleep(3)
        
        
        
        ''' step '''
        self.logStepBeginning("STEP 1 - prerequisites -zap to channel 3 and turn off STB")
        self.page.zapToChannel(3)
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(5)
        self.logStepResults("STEP 1 - prerequisites -zap to channel 3 and turn off STB")
        
        ''' step '''
        self.logStepBeginning("STEP 2- power on STB and wait for wake up screen")
        self.rc.sendKeys(["KEY_POWER"])
        currTime = datetime.now()
        i=1
        while (i<3):
            if (self.page.findInPage("Orange TV")):
                time.sleep(3)
                i=3
            self.assertTrue((datetime.now() - currTime).seconds < 500, "   ERR   cannot find wake up screen with channel 2")
            time.sleep(2)
        time.sleep(3)
        self.logStepResults("STEP 2- power on STB and wait for wake up screen")
        
        self.logStepBeginning("STEP 3 - check front-panel number")
        time.sleep(100)
        frontpanel = self.rc.getFrontPanel()
        time.sleep(2)
        if frontpanel!="WHD80":
            if (frontpanel != '3'):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
        self.logStepResults("STEP 3 - power on STB and wait for wake up screen")

        ''' step '''
        self.logStepBeginning("STEP 4 - Check live")
        
        self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVP1HD), " >> ERR in Zap to TVP1 HD")
        time.sleep(3)
        self.assertTrue(self.page.checkLive(), '>> Err: Lack of live')
        self.logStepResults("STEP 4 - Check live")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")