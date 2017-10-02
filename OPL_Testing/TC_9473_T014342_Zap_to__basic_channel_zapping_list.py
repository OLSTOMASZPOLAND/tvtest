# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta

 

 

class TC_9473_T014342_Zap_to__basic_channel_zapping_list(TC_OPL_template):

    """             
    Implementation of the HP QC test ID - 9473_T014342_Zap_to__basic_channel_zapping_list
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
        self.logStepBeginning("STEP 1 - Check info-banner in channel 1")
        self.assertTrue(self.page.zapToChannel(1))
        time.sleep(4)
        self.rc.sendKeys(["KEY_INFO"])
        time.sleep(5)
        infobaner = self.page.getInfoFromLiveBanner()
        time.sleep(10)
        if not (type(infobaner) is ProgramInfoItem):
            self.assertTrue(False, "  >>   ERR: Wrong type program")
        self.logger.debug("  >>  type program ->OK")
        infobaner = str(infobaner.lcn)
        if not (infobaner=='1'):
            self.assertTrue(False, "  >>   ERR: Wrong channel")
        self.logger.debug("  >>  number channel ->OK")
        self.logStepResults("STEP 1 - Check info-banner in channel 1")
        
        ''' step '''
        self.logStepBeginning("STEP 2 - Check changing info-banner and front panel")
        i=1
        while(i<4):
            i=i+1
            self.rc.sendKeys(["KEY_UP"])
            infobaner = self.page.getInfoFromLiveBanner()
            time.sleep(2)
            if not (type(infobaner) is ProgramInfoItem):
                self.assertTrue(False, "  >>   ERR: Wrong type program")
            self.logger.debug("  >>  type program ->OK  >" + str(i) + "<")
            infobaner = int(infobaner.lcn)
            time.sleep(5)
            if not (infobaner==i):
                self.assertTrue(False, "  >>   ERR: Wrong channel")
            self.logger.debug("  >>  channel number ->OK  >" + str(i) + "<")
            frontpanel = self.rc.getFrontPanel()
            if frontpanel!="WHD80":
                if (frontpanel==i):
                    self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
            self.logger.debug("  >>  front panel number ->OK  >" + str(i) + "<")
        self.rc.sendKeys(["KEY_OK"])
        frontpanel = self.rc.getFrontPanel()
        self.rc.sendKeys(["KEY_INFO"])
        channel = self.page.getInfoFromLiveBanner().lcn
        time.sleep(10)
        if frontpanel!="WHD80":
            if (frontpanel==channel): # do sprawdzenia
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
        self.logger.debug("  >>  front panel number->OK ")
        self.logStepResults("STEP 2 - Check changing info-banner and front panel")
        
        ''' step '''
        self.logStepBeginning("STEP 3 - Check live")
        
        self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVP1HD), " >> ERR in Zap to TVP1 HD")
        time.sleep(3)
        self.assertTrue(self.page.checkLive(), '>> Err: Lack of live')
        self.logStepResults("STEP 3 - Check live")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        