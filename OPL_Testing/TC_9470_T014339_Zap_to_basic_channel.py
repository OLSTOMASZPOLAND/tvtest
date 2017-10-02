# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Containers import *

class TC_9470_T014339_Zap_to_basic_channel (TC_OPL_template):
    '''
    Coverage: T014339 - Zap to basic channel -P +P
    @author: Mariusz Kolbus
    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):

        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("STEP 1 - channel is displayed")
        
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(5)
        self.assertTrue(self.page.zapToChannel(2))
        time.sleep(15)
        self.rc.sendKeys(["KEY_INFO"])
        time.sleep(5)
        LiveChannel1=self.page.getInfoFromLiveBanner()
        time.sleep(1)
        if not (type(LiveChannel1) is ProgramInfoItem):
            self.assertTrue(False, "  >>   ERR: Wrong type program")
        self.logger.debug("  >>  type program ->OK")
        LiveChannel2=self.page.getInfoFromLiveBanner().channelName
        if LiveChannel2==None:
            self.assertTrue(False, "  >>  ERR getInfoFromLiveBanner")
        time.sleep(5)
        self.rc.sendKeys(["KEY_BACK"])
        
        self.logStepResults("STEP 1 - channel is displayed")
        
        ''' step '''
        self.logStepBeginning("STEP 2 - pressing P+")
        
        self.rc.sendKeys(["KEY_CHANNELUP"])
        time.sleep(5)
        self.rc.sendKeys(["KEY_INFO"])
        time.sleep(5)
        LiveChannel2=self.page.getInfoFromLiveBanner()
        time.sleep(1)
        if not (type(LiveChannel2) is ProgramInfoItem):
            self.assertTrue(False, "  >>   ERR: Wrong type program")
        self.logger.debug("  >>  type program ->OK")
        LiveChannel2=self.page.getInfoFromLiveBanner().channelName
        if LiveChannel2==None:
            self.assertTrue(False, "  >>  ERR getInfoFromLiveBanner")
        self.rc.sendKeys(["KEY_BACK"])                                                     
        time.sleep(5)
        self.logStepResults("STEP 2 - pressing P+")
        
        ''' step '''
        self.logStepBeginning("STEP 3 - checking channel status")
        
        if (LiveChannel1==LiveChannel2):
            self.assertTrue(False, "    >>ERR: Problem with zapping up the channel")
        else:
            print "tutaj"
        self.logStepResults("STEP 3 - checking channel status")

        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")