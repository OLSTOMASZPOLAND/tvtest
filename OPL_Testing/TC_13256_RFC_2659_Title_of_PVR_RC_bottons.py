# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData

 

 

class TC_13256_RFC_2659_Title_of_PVR_RC_bottons(TC_OPL_template):

    """Implementation of the HP QC test ID - TC_13256_RFC_2659_Title_of_PVR_RC_bottons
    @author: Tomasz Stasiuk
    """

       

    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)

   

    def test(self):
        
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

       

        ''' prestep '''

        self.logStepResults("AT_THE_BEGINNING")
        time.sleep(3)  # wait a while, let the EPG load
        
        ''' step '''
        self.logStepBeginning("STEP 1 - Go To Scheduled recordings")     
        time.sleep(4)
        self.assertTrue(self.page.goToMenu(), "ERR: Entering  Menu")
        time.sleep(2)
        self.assertTrue(self.page.actionSelect(Menu.pvr), "ERROR IN GO TO EPG(GREEN_BUTTON)")
        time.sleep(2)
        self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "ERROR IN GO TO EPG(GREEN_BUTTON)")
        time.sleep(2)
        self.logStepResults("STEP 1 - Go To Scheduled recordings")
        
        ''' step '''
        self.logStepBeginning("STEP 2 -check empty recording name ")
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(3)
            title = self.page.driver.find_element_by_xpath(".//*[@id='nameTB']/div[2]/div/div/div[1]")
            title = title.text.encode('utf-8')
            if (len(title)!=0):
                self.assertTrue(False, "ERR: titile is not empty")
        except:
            self.assertTrue(False, "ERR: we are not in Scheduled recordings")
        self.logStepResults("STEP 2 - check empty recording name")
        
        
        ''' step '''
        self.logStepBeginning("STEP 3 -write name and check ")
        self.rc.sendKeys(["KEY_2"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_3"])
        time.sleep(2)        
        self.rc.sendKeys(["KEY_4"])
        time.sleep(5)        
        self.logStepResults("STEP 3 - write name and check")
                
        ''' step '''
        self.logStepBeginning("STEP 4 -check  recording name ")
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(3)
            title = self.page.driver.find_element_by_xpath(".//*[@id='nameTB']/div[2]/div/div/div[1]")
            title = title.text.encode('utf-8')
            print title
            if (title!="adg" or len(title)==3):
                self.assertFalse(False, "ERR: titile is not empty")
        except:
            self.assertTrue(False, "ERR: we are not in Scheduled recordings")
        self.logStepResults("STEP 4 - check  recording name")
        
        ''' step '''
        self.logStepBeginning("STEP 5 -delete the letter  ")
        self.rc.sendKeys(["KEY_LEFT"])
        time.sleep(5)        
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(3)
            title = self.page.driver.find_element_by_xpath(".//*[@id='nameTB']/div[2]/div/div/div[1]")
            title = title.text.encode('utf-8')
            print title
            if (title!="ad" or len(title)!=2):
                self.assertTrue(False, "ERR: titile is not empty")
        except:
            self.assertTrue(False, "ERR: we are not in Scheduled recordings")
        self.logStepResults("STEP 5 - delete the letter")
        
        
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        