# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta

 

 

class TC_2993_T01421_Change_channel_by_the_infobanner(TC_OPL_template):

    """             
    Implementation of the HP QC test ID - 2993 T01421_Change_channel_by_the_infobanner
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
        self.logStepBeginning("STEP 1 - Check infobanner on channel 3")
        
        self.assertTrue(self.page.zapToChannel(2))
        time.sleep(5)
        self.rc.sendKeys(["KEY_INFO"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_UP"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_INFO"])
        time.sleep(2)
        infobaner = self.page.getInfoFromLiveBanner()
        time.sleep(1)
        if not (type(infobaner) is ProgramInfoItem):
            self.assertTrue(False, "  >>   ERR: Wrong type program")
        self.logger.debug("  >>  type program ->OK")
        infobaner = str(infobaner.lcn)
        if not (infobaner=='3'):
            self.assertTrue(False, "  >>   ERR: Wrong channel")
        self.logger.debug("  >>  program number ->OK")
        self.logStepResults("STEP 1 - Check infobanner on channel 3")

        ''' step '''
        self.logStepBeginning("STEP 2 - Check info in infobanner ")
        infobaner = self.page.getInfoFromLiveBanner()
        if not (type(infobaner) is ProgramInfoItem):
            self.assertTrue(False, "  >>   ERR: Wrong type program")
        self.logger.debug("  >>  type program ->OK")
        infobanerlcn1 = str(infobaner.lcn)
        infobanerchannelName1 = str(infobaner.channelName)
        time.sleep(2)
        self.rc.sendKeys(["KEY_UP"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_UP"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_UP"])
        time.sleep(2)
        infobaner = self.page.getInfoFromLiveBanner()
        if not (type(infobaner) is ProgramInfoItem):
            self.assertTrue(False, "  >>   ERR: Wrong type program")
        self.logger.debug("  >>  type program ->OK")
        infobanerlcn2 = str(infobaner.lcn)
        infobanerchannelName2 = str(infobaner.channelName)
        time.sleep(2)
        if infobanerlcn2==infobanerlcn1:
            self.assertTrue(False, "  >>   ERR: WThis same lcn")
        if infobanerchannelName2==infobanerchannelName1:
            self.assertTrue(False, "  >>   ERR: WThis same lcn")
        self.logStepResults("STEP 2 - Check infobanner ")

        ''' step '''
        self.logStepBeginning("STEP 3 - Check live")
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(3)
        self.assertTrue(self.page.checkLive(), '>> Err: Lack of live')
        self.logStepResults("STEP 3 - Check live")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        