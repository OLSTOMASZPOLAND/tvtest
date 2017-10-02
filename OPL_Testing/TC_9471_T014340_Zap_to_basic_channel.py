# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta

 

 

class TC_9471_T014340_Zap_to_basic_channel(TC_OPL_template):

    """             
    Implementation of the HP QC test ID - 9471 T014340_Zap_to_basic_channel
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
        self.logStepBeginning("STEP 1 - Check channel 1")     
        time.sleep(2)
        self.assertTrue(self.page.zapToChannel(1), '  >>   ERR: problem with zap to channels 1') 
        time.sleep(3)   
        frontpanel = self.rc.getFrontPanel()
        if frontpanel!="WHD80":
            if not (frontpanel=='1'):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows: " + frontpanel +" <")
        self.logger.debug("  >>  front panel number ->OK")
        self.logStepResults("STEP 1 - Check channel 1")
        
        
        ''' step '''
        self.logStepBeginning("STEP 2 - Check zap channel P+(1)")
        self.rc.sendKeys(["KEY_CHANNELUP"]) 
        time.sleep(3)       
        frontpanel = self.rc.getFrontPanel()
        if frontpanel!="WHD80":
            if not (frontpanel=='2'):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows: " + frontpanel +" <")
        self.logger.debug("  >>  front panel number ->OK")
        self.logStepResults("STEP 2 - Check zap channel P+(1)")

        ''' step '''
        self.logStepBeginning("STEP 3 - Check channel 2")     
        time.sleep(2)
        self.assertTrue(self.page.zapToChannel(2), '  >>   ERR: problem with zap to channels 2')   
        time.sleep(3) 
        frontpanel = self.rc.getFrontPanel()
        if frontpanel!="WHD80":
            if not (frontpanel=='2'):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
        self.logger.debug("  >>  front panel number ->OK")
        self.logStepResults("STEP 3 - Check channel 2")
        
        
        ''' step '''
        self.logStepBeginning("STEP 4 - Check zap channel P+(2)")
        self.rc.sendKeys(["KEY_CHANNELUP"]) 
        time.sleep(3)       
        frontpanel = self.rc.getFrontPanel()
        if frontpanel!="WHD80":
            if not (frontpanel=='3'):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
        self.logger.debug("  >>  front panel number ->OK")
        self.logStepResults("STEP 4 - Check zap channel P+(2)")
        
        ''' step '''
        self.logStepBeginning("STEP 5 - Check channel 3")     
        time.sleep(2)
        self.assertTrue(self.page.zapToChannel(3), '  >>   ERR: problem with zap to channels 3')    
        time.sleep(3)
        frontpanel = self.rc.getFrontPanel()
        if frontpanel!="WHD80":
            if not (frontpanel=='3'):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
        self.logger.debug("  >>  front panel number ->OK")
        self.logStepResults("STEP 5 - Check channel 3")

        
        ''' step '''
        self.logStepBeginning("STEP 6 - Check zap channel P+(3)")
        self.rc.sendKeys(["KEY_CHANNELUP"]) 
        time.sleep(3)       
        frontpanel = self.rc.getFrontPanel()
        if frontpanel!="WHD80":
            if not (frontpanel=='4'):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel +" <")
        self.logger.debug("  >>  front panel number ->OK")
        self.logStepResults("STEP 6 - Check zap channel P+(3)")
        
        ''' step '''
        self.logStepBeginning("STEP 7 - Check live")
        
        self.rc.sendKeys(["KEY_8"]) 
        time.sleep(3)
        self.assertTrue(self.page.checkLive(), '>> Err: Lack of live')
        self.logStepResults("STEP 7 - Check live")
            
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        