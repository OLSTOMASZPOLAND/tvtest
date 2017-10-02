# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import motionDetection
from OPL_Testing.TC_8912_T016328_display_information_of_recording_updated import *


class TC_3624_T015987_Stop_and_resume_a_VOD_several_successive_resume(TC_OPL_template):

    """Implementation of the HP QC test ID TC_3624_T015987_Stop_and_resume_a_VOD_several_successive_resume
 
    @author: Tomasz Stasiuk
    """

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):


        self.logger.info("----- " + self.__class__.__name__ + " START -----")


        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING - delete all future and ongoing record in My Records")
        
        if not self.page.cleanCodeParentalToDefault():
            self.page.cleanCodeParentalToDefault()

        if not self.page.setParentalControl(ParentalControl.SetDeactive):
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            self.page.setParentalControl(ParentalControl.SetDeactive)    
        
        '''step'''
        self.logStepBeginning("STEP 1 - Go to VOD")
        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent),"ERR: Go to VOD Catalog")
        self.logStepResults("STEP 1 - Go to VOD")
              
        '''step'''
        self.logStepBeginning("STEP 2 - rent and play vod")
        time.sleep(5)
        self.rc.sendKeys(["KEY_OK"])
        n=False
        i=0
        while n!=True:
            title = self.page.getInfoFromVodPage().title
            print title
            if "1h" in title:
                n=True
            else:
                time.sleep(2)
                self.rc.sendKeys(["KEY_RIGHT"])
            time.sleep(10)
            i=i+1
            if i==30:
                self.assertTrue(False, '  >>  no VOD with 1h')
        time.sleep(8)
        self.assertTrue(self.page.rentAndPlayOrPlayRentedVod(),"ERR: play vod")
        time.sleep(10)
        self.logStepResults("STEP 2 - rent and play vod")
      
        '''step'''
        self.logStepBeginning("STEP 3 - watch vod after 5 min load time")
        time.sleep(300)
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(5)
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            vodTime = self.page.driver.find_element_by_css_selector(".time").text
        except:
            self.fail("   ERR   cannot get time info")
        print "load time"
        print vodTime
            
        self.logStepResults("STEP 3 - watch vod after 5 min load time")

        '''step'''
        self.logStepBeginning("STEP 4 - exit vod to vps")
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(11)
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(11)
        self.assertFalse(self.page.actionSelect(Menu.vodStopWatching),"ERR: check pop-up not appear")
        self.logStepResults("STEP 4 - exit vod to vps")

        '''step'''
        self.logStepBeginning("STEP 5 - check no video and title")
        time.sleep(11)
        self.assertFalse(self.page.checkLive(pvrAndVod=True),"ERR: not exit from  vod to VPS")
        time.sleep(3)
        title2 = self.page.getInfoFromVodPage().title
        if not title2==title:
            self.fail("   ERR   not the same title")
        time.sleep(3)
        self.logStepResults("STEP 5 - check no video")
        
        
        '''step'''
        self.logStepBeginning("STEP 6 - check if vod start from last end position")
        time.sleep(5)
        self.assertTrue(self.page.actionSelect(Menu.vodResume),"ERR: check if vod have status to rent")
        time.sleep(5)
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(5)        
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            vodTime2 = self.page.driver.find_element_by_css_selector(".time").text
        except:
            self.fail("   ERR   cannot get time info")
            
        if not vodTime==vodTime2:
            self.fail("   ERR   start position is not the same from last end vod ")
        
        self.logStepResults("STEP 6 - check if vod start from last end position")         
        
        '''step'''
        self.logStepBeginning("STEP 7 - watch vod after 10 min load time")
        time.sleep(300)
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(5)
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            vodTime = self.page.driver.find_element_by_css_selector(".time").text
        except:
            self.fail("   ERR   cannot get time info")
        print "load time"
        print vodTime
            
        self.logStepResults("STEP 7 - watch vod after 10 min load time") 
               
        '''step'''
        self.logStepBeginning("STEP 8 - exit vod to vps")
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(3)
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(8)
        self.assertFalse(self.page.actionSelect(Menu.vodStopWatching),"ERR: check pop-up not appear")

        self.logStepResults("STEP 8 - exit vod to vps")               
               
        '''step'''
        self.logStepBeginning("STEP 9 - check no video and title")
        time.sleep(3)
        self.assertFalse(self.page.checkLive(pvrAndVod=True),"ERR: not exit from  vod to VPS")
        time.sleep(3)
        title2 = self.page.getInfoFromVodPage().title
        if not title2==title:
            self.fail("   ERR   not the same title")
        time.sleep(3)
        self.logStepResults("STEP 9 - check no video") 
        
        
        '''step'''
        self.logStepBeginning("STEP 10 - check if vod start from last end position")
        time.sleep(5)
        self.assertTrue(self.page.actionSelect(Menu.vodResume),"ERR: check if vod have status to rent")
        time.sleep(5)
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(5)        
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            vodTime2 = self.page.driver.find_element_by_css_selector(".time").text
        except:
            self.fail("   ERR   cannot get time info")
            
        if not vodTime==vodTime2:
            self.fail("   ERR   start position is not the same from last end vod ")
        
        self.logStepResults("STEP 10 - check if vod start from last end position")              
        
        '''step'''
        self.logStepBeginning("STEP 11 - watch vod after 5 min load time")
        time.sleep(300)
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(5)
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            vodTime = self.page.driver.find_element_by_css_selector(".time").text
        except:
            self.fail("   ERR   cannot get time info")
        print "load time"
        print vodTime
            
        self.logStepResults("STEP 11 - watch vod after 5 min load time") 
               
        '''step'''
        self.logStepBeginning("STEP 12 - exit vod to vps")
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(3)
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(8)
        self.assertFalse(self.page.actionSelect(Menu.vodStopWatching),"ERR: check pop-up not appear")

        self.logStepResults("STEP 12 - exit vod to vps")               
               
        '''step'''
        self.logStepBeginning("STEP 13 - check no video and title")
        time.sleep(3)
        self.assertFalse(self.page.checkLive(pvrAndVod=True),"ERR: not exit from  vod to VPS")
        time.sleep(3)
        title2 = self.page.getInfoFromVodPage().title
        if not title2==title:
            self.fail("   ERR   not the same title")
        time.sleep(3)
        self.logStepResults("STEP 13 - check no video") 
        
        
        '''step'''
        self.logStepBeginning("STEP 14 - check if vod start from last end position")
        time.sleep(5)
        self.assertTrue(self.page.actionSelect(Menu.vodResume),"ERR: check if vod have status to rent")
        time.sleep(5)
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(5)        
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)
            vodTime2 = self.page.driver.find_element_by_css_selector(".time").text
        except:
            self.fail("   ERR   cannot get time info")
            
        if not vodTime==vodTime2:
            self.fail("   ERR   start position is not the same from last end vod ")
        time.sleep(5)
        self.rc.sendKeys(["KEY_PLAY"])
        time.sleep(5)  
        self.logStepResults("STEP 14 - check if vod start from last end position")                 
               

               
               
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

