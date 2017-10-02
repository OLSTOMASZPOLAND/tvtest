# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta

 

 

class TC_9475_T014344_Zap_to__basic_channel_EPG(TC_OPL_template):

    """           
    Implementation of the HP QC test ID - 9475_T014344_Zap_to__basic_channel_EPG
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
        self.logStepBeginning("STEP 1 - Go To EPG all program channels")     
        self.rc.sendKeys(["KEY_BACK"]) 
        time.sleep(1)       
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(1)
        self.rc.sendKeys(["KEY_GREEN"]) 
        time.sleep(1) 
        self.assertTrue(self.page.actionSelect(Menu.epg), "ERROR IN GO TO EPG(GREEN_BUTTON)")
        self.assertTrue(self.page.actionSelect(Menu.epgWeek), 'ERRPR IN GO TO EPG  Channels') 
        time.sleep(1)
        self.rc.sendKeys(["KEY_3"]) 
        time.sleep(1) 
        self.logStepResults("STEP 1 - Go To EPG all program channels")
        
        ''' step '''
        self.logStepBeginning("STEP 2 -check program name")
        epg = self.page.getInfoFromEpgFocus()
        if not (type(epg) is ProgramInfoItem):
            self.assertTrue(False, "  >>   ERR: Wrong type mosaic program")
        self.logger.debug("  >>  type program ->OK")
        epgLcn = str(epg.lcn)
        epgprogram = str(epg.program)
        time.sleep(2)
        self.rc.sendKeys(["KEY_OK"])
        self.assertTrue(self.page.findInPage(epgprogram), "  >>   ERR: Wrong program name")
        self.logStepResults("STEP 2 -check program name")
        
        ''' step '''
        self.logStepBeginning("STEP 3 -check program name")
        self.assertTrue(self.page.actionSelect(Menu.epgPlay))
        time.sleep(2)
        frontpanel = self.rc.getFrontPanel()
        time.sleep(1)
        if frontpanel!="WHD80":
            if (frontpanel != '3'):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, showing " + frontpanel +" <")
        self.logger.debug("  >>  front-panel number ->OK")
        self.rc.sendKeys(["KEY_INFO"])
        channel = self.page.getInfoFromLiveBanner().lcn
        time.sleep(10)
        if (frontpanel==channel):
            self.assertTrue(False, "  >>   ERR: Wrong number in front panel, showing " + frontpanel +" <")
        self.logger.debug("  >>  channel number in info-banner ->OK")
        self.logStepResults("STEP 3 -check program name")
        
        ''' step '''
        self.logStepBeginning("STEP 4 - Check live")
        
        self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVP1HD), " >> ERR in Zap to TVP1 HD")
        time.sleep(3)
        self.assertTrue(self.page.checkLive(), '>> Err: Lack of live')
        self.logStepResults("STEP 4 - Check live")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        