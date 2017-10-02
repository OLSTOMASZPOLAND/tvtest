# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_9082_T014555_watch_the_trailers_of_a_VOD_IPTV_update(TC_OPL_template):
    '''
    C_9082_T014555_watch_the_trailers_of_a_VOD_IPTV_update
    @author: Tomasz Stasiuk
    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        ''' prestep '''

        self.logStepResults("AT_THE_BEGINNING")
        
        
        ''' step '''

        self.logStepBeginning("STEP 1 - go to current vps")
        time.sleep(2)
        self.assertTrue(self.page.goToVodMenu(), "ERR: Entering VOD menu")
        time.sleep(10)
        self.assertTrue(self.page.actionSelect(Menu.vodAutomation), "ERR: Entering VOD automate catalog") 
        time.sleep(10)
        self.assertTrue(self.page.actionSelect(Menu.VOD_oneshot_csa1v2), "ERR: Entering VOD -> VPS") 
        time.sleep(10)
        if (self.page.findInList(Menu.vodResume)):
            time.sleep(600)
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(5)
            self.rc.sendKeys(["KEY_OK"])
        self.logStepResults("STEP 1 - go to current vps")

        
        ''' step '''

        self.logStepBeginning("STEP 2- open trailer and check popup")
        self.assertTrue(self.page.actionSelect(Menu.vodTrailer), "ERR: Entering VOD -> VPS") 
        time.sleep(1)
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(3)
            popup = self.page.driver.find_element_by_xpath("html/body/div[7]/div[1]/div[4]")
            popup = popup.text.encode('utf-8')  
            if (popup!=Menu.VOD_oneshot_csa1v2 or len(popup)==0):
                self.assertTrue(False, "ERR: No popup encouraging to rent vod")       
        except:
            self.assertTrue(False, "ERR: No popup encouraging to rent vod")        
        time.sleep(14)
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(3)
            popup = self.page.driver.find_element_by_xpath("html/body/div[7]/div[1]/div[4]")
            popup = popup.text.encode('utf-8')  
            if (len(popup)!=0):
                self.assertTrue(False, "ERR:  popup not disappear ")       
        except:
            self.assertTrue(False, "ERR:  popup not disappear")  
        self.logStepResults("STEP 2-  open trailer and check popup")
        
        ''' step '''
        
        self.logStepBeginning("STEP 3- chcek exit by /exit/back/stop")
        self.rc.sendKeys(["KEY_back"])
        time.sleep(2)
        if (self.page.findInList(Menu.vodSummary)==False):
            self.assertTrue(False, "ERR: key back not stop trailer")  
        else:
            self.assertTrue(self.page.actionSelect(Menu.vodTrailer), "ERR: Entering VOD -> VPS") 
            time.sleep(15)
        self.rc.sendKeys(["KEY_exit"])
        time.sleep(2)
        if (self.page.findInList(Menu.vodSummary)==False):
            self.assertTrue(False, "ERR: key back not exit trailer")  
        else:
            self.assertTrue(self.page.actionSelect(Menu.vodTrailer), "ERR: Entering VOD -> VPS") 
            time.sleep(15)
        self.rc.sendKeys(["KEY_STOP"])
        time.sleep(2)
        if (self.page.findInList(Menu.vodSummary)==False):
            self.assertTrue(False, "ERR: key stop not stop trailer")  
        else:
            self.assertTrue(self.page.actionSelect(Menu.vodTrailer), "ERR: Entering VOD -> VPS") 
            time.sleep(60*2+25)
        self.logStepResults("STEP 3-  chcek exit by /exit/back/stop/return")   

        
        ''' step '''

        self.logStepBeginning("STEP 4- check if after end of trailer you go to menu and by focused on rent")
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(3)
            popup = self.page.driver.find_element_by_css_selector("html body div.scene.whiteBg.vpsMainWidget div.menuList.dockLeft div.list div.container div#vpsRent.listItem.highlight")
        except:
            time.sleep(1)
            self.assertTrue(False, "ERR: not focused on rent")       
        self.logStepResults("STEP 4-  check if after end of trailer you go to menu and by focused on rent")   


        ''' step '''

        self.logStepBeginning("STEP 5- check changing trailers by pressing left")
        self.assertTrue(self.page.actionSelect(Menu.vodTrailer), "ERR: Entering VOD -> VPS") 
        time.sleep(1)
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(3)
            popup = self.page.driver.find_element_by_xpath("html/body/div[7]/div[1]/div[4]")
            popup1 = popup.text.encode('utf-8')
        except:
            self.assertTrue(False, "ERR: with open trailer")  
        self.rc.sendKeys(["KEY_LEFT"])
        time.sleep(1)
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(3)
            popup = self.page.driver.find_element_by_xpath("html/body/div[7]/div[1]/div[4]")
            popup2 = popup.text.encode('utf-8')
        except:
            self.assertTrue(False, "ERR: with open trailer")   
        if (popup1==popup2):  
            self.assertTrue(False, "ERR: not change trailer after press right key")   
        time.sleep(2)
        self.rc.sendKeys(["KEY_Right"])
        self.logStepResults("STEP 5-  check changing trailers by pressing left")   


        ''' step '''
        
        self.logStepBeginning("STEP 6- rent vod by trailer")
        self.assertTrue(self.rentVodThenPlay(), "ERR: problem with rent vod") 
        time.sleep(10)
        self.rc.sendKeys(["KEY_ok"])
        time.sleep(1)
        self.assertTrue(self.page.findInPage(Menu.VodBeginning), "ERR: stb is not playing vod") 
        time.sleep(1)
        self.rc.sendKeys(["KEY_stop"])
        time.sleep(1)
        if (self.page.findInPage(Menu.pvrStop2)):
            self.assertTrue(self.page.actionSelect(Menu.pvrStop2), "ERR: with stoping vod") 
        self.logStepResults("STEP 6-  rent vod by trailer")                 
                   
        ''' step '''
        
        self.logStepBeginning("STEP 7- check if after rent vod trailer not show popup")
        time.sleep(1)
        self.assertTrue(self.page.actionSelect(Menu.vodTrailer), "ERR: Entering VOD -> VPS") 
        time.sleep(2)
        try:
            self.page.driver.get(Rpi.DUMP)
            time.sleep(3)
            popup = self.page.driver.find_element_by_xpath("html/body/div[7]/div[1]/div[4]")
            popup = popup.text.encode('utf-8')  
            if (len(popup)!=0):
                self.assertTrue(False, "ERR:  popup not disappear ")       
        except:
            self.assertTrue(False, "ERR:  popup not disappear")  
        self.logStepResults("STEP 7-  check if after rent vod trailer not show popup")  
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        
    def rentVodThenPlay(self, checkParentalControl=False, goBackToVodScreen=False):

        self.rc.sendKeys(["KEY_OK"])
        time.sleep(3)
        adultCodeTypedIn = False
        # purchase check (when no cash on the PREPAID account) - TODO to be sure if it should be check or not
        if self.page.findInDialogBox(Menu.vodAdultPopup):
            self.rc.sendNumberSequence(Env.CONFIDENTIAL_CODE)
            self.rc.sendKeys(["KEY_OK"])
            if self.page.findInDialogBox(DialogBox.WrongConfidentialCode):
                self.page.logger.info("  >>   ERR: wrong confidential code")
                return False
            adultCodeTypedIn = True

        # parental control check
        if checkParentalControl and not adultCodeTypedIn:
            if (not self.page.findInDialogBox(Menu.parentalControl)):
                self.page.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
                return False
            self.rc.sendNumberSequence(Env.PARENTAL_CODE)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(3)
            if self.page.findInDialogBox(DialogBox.WrongParentalCode):
                self.page.logger.info("  >>   ERR: wrong parental code")
                return False
        elif checkParentalControl and adultCodeTypedIn:
            pass
        else:
            if self.page.findInDialogBox(Menu.parentalControl):
                self.page.logger.info("  >>   ERR: problem finding >" + Menu.parentalControl + "<")
                return False

        time.sleep(10)

        # NPK
        if not self.page.findInDialogBox(Menu.vodNPK):
            self.page.logger.info("  >>   ERR: problem finding >" + Menu.vodNPK + "<")
            return False
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_DOWN"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(5)
        if self.page.findInDialogBox(Menu.vodNPKInfo):
            self.rc.sendKeys(["KEY_OK"])

        time.sleep(1)

        if self.page.findInDialogBox(DialogBox.VodError):  # TODO correct error description
            self.page.logger.info("  >>   ERR: problem finding >" + DialogBox.VodError + "<")
            return False
        if self.page.findInDialogBox(DialogBox.VodError2):
            self.logger.info("  >>   ERR: general error >" + DialogBox.VodError2 + "<")
            return False
        if self.page.findInDialogBox(DialogBox.VodError3):
            self.logger.info("  >>   ERR: problem finding >" + DialogBox.VodError3 + "<")
            return False
        if self.page.findInCssSelectorElement("menu", ".breadCrumb .path .first"):
            self.page.logger.info("  >>   ERR: problem with video playback, im back in main menu")
            return False

        time.sleep(10)

        if (self.page.startVodIfNotPlayed(goBackToVodScreen=goBackToVodScreen)):
            return True
        else:
            self.page.logger.info("  >>   ERR: problem in function >startVodIfNotPlayed<")
            return False

        return True        
        