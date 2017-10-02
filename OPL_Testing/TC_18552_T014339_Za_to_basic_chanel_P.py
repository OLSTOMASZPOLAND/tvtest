# -*- coding: utf-8 -*-

import time
from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta





class TC_18552_T014339_Za_to_basic_chanel_P(TC_OPL_template):

    """     
    Implementation of the HP QC test ID - 18552_T014339_Za_to_basic_chanel_P
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
        self.logStepBeginning("STEP 1 - Channel 1")
        numberchannel = u"1".encode('utf-8')
        self.page.zapToChannel(1)
        frontpanel = self.rc.getFrontPanel()
        time.sleep(3)
        if frontpanel != "WHD80":
            if (frontpanel != str(numberchannel)):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel + " <")

        self.logStepResults("STEP 1 - Channel 1")

        ''' step '''
        self.logStepBeginning("STEP 2 - P+(1)")
        time.sleep(2)
        self.rc.sendKeys(["KEY_CHANNELUP"])
        time.sleep(2)
        numberchannel = u"2".encode('utf-8')
        frontpanel = self.rc.getFrontPanel()
        time.sleep(3)
        if frontpanel != "WHD80":
            if (frontpanel != str(numberchannel)):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel + " <")
        self.logStepResults("STEP 2 - P+(1)")

        ''' step '''
        self.logStepBeginning("STEP 3 - P+(2)")
        time.sleep(2)
        self.rc.sendKeys(["KEY_CHANNELUP"])
        time.sleep(2)
        numberchannel = u"3".encode('utf-8')
        frontpanel = self.rc.getFrontPanel()
        time.sleep(3)
        if frontpanel != "WHD80":
            if (frontpanel != str(numberchannel)):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel + " <")
        self.logStepResults("STEP 3 - P+(2)")

        ''' step '''
        self.logStepBeginning("STEP 4 - P-(1)")
        time.sleep(2)
        self.rc.sendKeys(["KEY_CHANNELDOWN"])
        time.sleep(2)
        numberchannel = u"2".encode('utf-8')
        frontpanel = self.rc.getFrontPanel()
        time.sleep(3)
        if frontpanel != "WHD80":
            if (frontpanel != str(numberchannel)):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel + " <")
        self.logStepResults(" STEP 4 - P-(1)")

        ''' step '''
        self.logStepBeginning("STEP 5 - P-(2)")
        time.sleep(2)
        self.rc.sendKeys(["KEY_CHANNELDOWN"])
        time.sleep(2)
        numberchannel = u"1".encode('utf-8')
        frontpanel = self.rc.getFrontPanel()
        time.sleep(3)
        if frontpanel != "WHD80":
            if (frontpanel != str(numberchannel)):
                self.assertTrue(False, "  >>   ERR: Wrong number in front panel, shows " + frontpanel + " <")
        self.logStepResults("STEP 5 - P-(2)")

        ''' step '''
        self.logStepBeginning("STEP 6 - Check live")
        self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVP1HD), " >> ERR in Zap to TVP1 HD")
        time.sleep(3)
        self.assertTrue(self.page.checkLive(), '>>   ERR: None fullscreen')
        self.rc.sendKeys(["KEY_BACK"])
        self.logStepResults("STEP 6 - Check live")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
