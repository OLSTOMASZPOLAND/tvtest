# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta

 

 

class TC_9474_T014343_Zap_to__basic_channel_mosaic(TC_OPL_template):

    """        
    Implementation of the HP QC test ID - 9474_T014343_Zap_to__basic_channel_mosaic
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
        self.logStepBeginning("STEP 1 - Check focus channel in mosaic")
        
        self.rc.sendKeys(["KEY_0"])
        time.sleep(6)
        self.rc.sendKeys(["KEY_RIGHT", "KEY_RIGHT"])
        time.sleep(4)
        mosaicAll = self.page.getInfoFromMosaicFocus()
        if not (type(mosaicAll) is ProgramInfoItem):
            self.assertTrue(False, "  >>   ERR: Wrong type mosaic program")
        mosaicLcn =str(mosaicAll.lcn)
        self.logger.debug("  >>  type program ->OK")
        if (mosaicLcn != '3'):
            self.assertTrue(False, "  >>   ERR: Wrong number in focus channel")
        mosaicProgram = str(mosaicAll.program)
        self.logger.debug("  >>  channel number ->OK")
        if (mosaicProgram == None):
            self.assertTrue(False, "  >>   ERR: None program title in focus channel")
        self.logger.debug("  >>  title program ->OK")
        self.logStepResults("STEP 1 - Check focus channel in mosaic")
        
        ''' step '''
        self.logStepBeginning("STEP 2 - Check go to channel in mosaic and front panel")
        
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(4)
        frontpanel = self.rc.getFrontPanel()
        time.sleep(1)
        if frontpanel!="WHD80":
            if (frontpanel != '3'):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
        self.logger.debug("  >>  frontpanel number ->OK")
        self.rc.sendKeys(["KEY_INFO"])
        channel = self.page.getInfoFromLiveBanner().lcn
        time.sleep(10)
        if (frontpanel==channel):
            self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
        self.logger.debug("  >>  channel number in infobaner ->OK")
        self.logStepResults("STEP 2 - Check go to channel in mosaic and front panel")
        
        
        ''' step '''
        self.logStepBeginning("STEP 3 - Check live")
        
        self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVP1HD), " >> ERR in Zap to TVP1 HD")
        time.sleep(3)
        self.assertTrue(self.page.checkLive(), '>> Err: Lack of live')
        self.logStepResults("STEP 3 - Check live")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        