# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta

 

 

class TC_9472_T014341_Zap_to__basic_channel_infobanner(TC_OPL_template):

    """             
    Implementation of the HP QC test ID - 9472_T014341_Zap_to__basic_channel_infobanner
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
        self.logStepBeginning("STEP 1 - Check infobanner")
        
        self.assertTrue(self.page.zapToChannel(2))
        time.sleep(2)
        self.rc.sendKeys(["KEY_CHANNELUP"])
        time.sleep(1)
        self.rc.sendKeys(["KEY_INFO"])
        time.sleep(1)
        infobaner = self.page.getInfoFromLiveBanner()
        time.sleep(1)
        if not (type(infobaner) is ProgramInfoItem):
            self.assertTrue(False, "  >>   ERR: Wrong type program")
        self.logger.debug("  >>  type program ->OK")
        infobaner = str(infobaner.lcn)
        if not (infobaner=='3'):
            self.assertTrue(False, "  >>   ERR: Wrong channel")
        self.logger.debug("  >>  program number ->OK")
        self.logStepResults("STEP 1 - Check infobanner")
        
        ''' step '''
        self.logStepBeginning("STEP 2 - Check live")
        
        self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVP1HD), " >> ERR in Zap to TVP1 HD")
        time.sleep(3)
        self.assertTrue(self.page.checkLive(), '>> Err: Lack of live')
        self.logStepResults("STEP 2 - Check live")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        