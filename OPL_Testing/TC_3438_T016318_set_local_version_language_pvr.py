# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import motionDetection
from OPL_Testing.TC_8912_T016328_display_information_of_recording_updated import *


class TC_3438_T016318_set_local_version_language_pvr(TC_OPL_template):

    """Implementation of the HP QC test ID 3438 T016318_set_local_version_language_pvr
 
    @author: Tomasz Stasiuk
    """

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self): 
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")


            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING - delete all future and ongoing record in My Records")

            '''step'''
            self.logStepBeginning("STEP 1 - delete all my records ")
            self.assertTrue(self.page.cleanDeleteAllRecordings(), 'ERR: Don`t delete future records ')
            self.assertTrue(self.page.deleteAllPvr(),"ERR: Don`t delete  records")
            self.logStepResults("STEP 1 - delete all my records ")
       
          
            '''step'''
            self.logStepBeginning("STEP 2 - record with two  audio language ")
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(1)
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(1)
            self.rc.sendKeys(["KEY_TV"])
            time.sleep(3)
            self.assertTrue(self.page.zapToChannel(self.rc.getChannelHBOHD), " >> ERR in Zap to HBO HD")
            time.sleep(10)
            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(20)
            self.assertTrue(self.page.actionInstantRecord(5), 'ERR: Failed recording ')
            time.sleep(500)
            self.logStepResults("STEP 2 - record with two  audio language")
          
          
          
            '''step'''
            self.logStepBeginning("STEP 3 - record with one not local audio language ")
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(1)
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(1)
            self.rc.sendKeys(["KEY_TV"])
            time.sleep(3)
            self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVPPolonia), " >> ERR in Zap to TVP Polonia")
            time.sleep(10)
            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(20)
            self.assertTrue(self.page.actionInstantRecord(5), 'ERR: Failed recording ')
            time.sleep(500)
            self.logStepResults("STEP 3 - record with one not local audio language ")
            
          


            '''step'''
            self.logStepBeginning("STEP 4 - choose the language selection - witch reader (z lektorem) ")
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            time.sleep(4)
            self.page.goToMenu()
            time.sleep(4)
            self.assertTrue(self.page.actionSelect(Menu.myAccount), 'ERR: Not finding or no included in my account')
            time.sleep(4)
            self.assertTrue(self.page.actionSelect(Menu.mySettings), 'ERR: Not finding or no included in my settings')
            time.sleep(4)
            self.assertTrue(self.page.actionSelect(Menu.language), 'ERR: Not finding or no included in language settings')
            time.sleep(4)
            self.assertTrue(self.page.actionSelect(Menu.nativeSoundtrack), 'ERR: Not finding or no included in native sound track')
            time.sleep(4)
            self.assertTrue(self.page.findInPage("Obecnie: z lektorem"), 'ERR: Don`t changing in to (z lektorem) ')
            self.logStepResults("STEP 4 - choose the language selection - witch reader (z lektorem) ")
     
    
            '''step'''
            self.logStepBeginning("STEP 5 - watch a PVR record with only one not local audio language ")
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            self.assertTrue(self.page.goToMenu(), 'ERR: Don`t go to MENU ')
            time.sleep(6)
            self.assertTrue(self.page.actionSelect(Menu.pvr), 'ERR: Not finding or no included in pvr')
            time.sleep(6)
            self.assertTrue(self.page.actionSelect(Menu.pvrMyRecords), 'ERR: Not finding or no included in pvr my records')
            time.sleep(60)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(6)
            self.assertTrue(self.page.actionSelect(Menu.pvrPlay), 'ERR: Not finding pvr play')
            time.sleep(10)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(1)                             
            status = self.page.actionSelect(Menu.toolboxNativeSoundtrack)
            if (status==False):
                self.rc.sendKeys(["KEY_BACK"])
            else:
                self.assertTrue(False, "   ERR: find other language ")    
            time.sleep(20)
            self.logStepResults("STEP 5 - watch a PVR record with only one not local audio language ")
     
     
            '''step'''
            self.logStepBeginning("STEP 6 -watch a PVR record with at last two audio language ")
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(6)
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(60)
            self.rc.sendKeys(["KEY_RIGHT"])
            time.sleep(6)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(8)
            self.assertTrue(self.page.actionSelect(Menu.pvrPlay), 'ERR: Not finding pvr play')
            time.sleep(10)
            self.rc.sendKeys(["KEY_OK"])
            status2 = self.page.actionSelect(Menu.toolboxNativeSoundtrack)
            if (status2==False):
                self.assertTrue(False, "   ERR: find other language ")          
            status3 = self.page.actionSelect(Menu.toolbox_2_englishSoundtrack)
            if (status3==False):
                status3 = self.page.actionSelect("org")
            if (status3==False):
                self.assertTrue(False, '  >>  ERR  find a english language ')
            else:
                self.rc.sendKeys(["KEY_BACK"])
            time.sleep(20)
            self.logStepResults("STEP 6 -watch a PVR record with at last two audio language  ")
   
   
            '''step'''
            self.logStepBeginning("STEP 7 - checking a focused and selected automatically option (z lektorem) ")
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            time.sleep(2)
            self.assertTrue(self.page.goToMenu(), 'ERR: Don`t go to MENU ')
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myAccount), 'ERR: Not finding or no included in my account')
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.mySettings), 'ERR: Not finding or no included in my settings')
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.language), 'ERR: Not finding or no included in language settings')
            time.sleep(1)
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(2)
            self.assertTrue(self.page.findInPage("Obecnie: z lektorem"), 'ERR: Don`t focused witch reader (z lektorem) ')
            time.sleep(4)
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            self.logStepResults("STEP 7 - checking a focused and selected automatically option (z lektorem) ")
 
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("error occurred - %s" % e)
            self.logger.info("error occurred - %s - cleaning" % e)
            raise
 
        finally:
            self.logger.info("----------- cleaning -----------")
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            self.page.checkStbStatusIfKoReboot()
            self.page.cleanDeleteAllRecordings()
            self.page.deleteAllPvr()
            
    def recordChannel(self, channel):
        if not self.page.zapToChannel(channel):
            return False
        time.sleep(5)
        if not self.page.checkLive():
            return False
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(3)

        hasSubtitles = False
        hasLanguages = False

        if (self.page.findInList(Menu.toolboxNativeSoundtrack, True)):
            if self.page.actionSelect(Menu.toolboxNativeSoundtrack):
                if len(self.page.getList()) > 1:
                    hasSubtitles = True
                    self.rc.sendKeys(["KEY_BACK"])

        time.sleep(3)

        self.rc.sendKeys(["KEY_OK"])

        time.sleep(3)

        if (self.page.findInList(Menu.toolboxNoSubtitleLong, True)):
            if self.page.actionSelect(Menu.toolboxNoSubtitleLong):
                if len(self.page.getList()) > 1:
                    hasLanguages = True
                    self.rc.sendKeys(["KEY_BACK"])
        if hasLanguages and hasSubtitles:
            self.rc.sendKeys(["KEY_RECORD"])
            time.sleep(20)
            if self.page.actionInstantRecord():
                return True
            else:
                return False
        else:
            return False
