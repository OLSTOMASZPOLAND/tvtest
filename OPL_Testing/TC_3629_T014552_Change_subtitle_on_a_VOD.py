# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3629_T014552_Change_subtitle_on_a_VOD(TC_OPL_template):
    '''
    Coverage: HP QC test ID - 3629 - T014552_Change subtitle on a VOD
    
    @author: Tomasz Stasiuk
    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        try:
            
            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            
            ''' Initial State '''
            self.logStepBeginning("Initial State - User is watching a VOD")
            
            status=True
            
            self.page.setParentalControl(ParentalControl.SetDeactive)
            
            time.sleep(2)
            self.rc.sendKeys(["KEY_MENU"])
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "ERR: Entering My Account")
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.mySettings), "ERR: Entering My Settings")
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.subtitles), "ERR: Selecting Subtitles") 
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.noSubtitle), "ERR: Choosing 'brak' option in 'napisy' menu") 
            time.sleep(2)
            
            self.logStepResults("Initial State - User is watching a VOD")
            
            ''' Step 1 '''
            self.logStepBeginning("Step 1 - Enter VOD Catalog and rent VOD")
            
            time.sleep(2)
            self.assertTrue(self.page.goToVodMenu(), "ERR: Entering VOD menu")
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(Menu.vodAutomation), "ERR: Entering VOD automate catalog") 
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(Menu.VOD_subtitlesV2), "ERR: Entering VOD VPS") 
            time.sleep(5)
            
            self.assertTrue(self.page.rentAndPlayOrPlayRentedVod(), "ERR: Renting VOD") 
            time.sleep(20)
            
            status=False
            
            self.logStepResults("Step 1 - Enter VOD Catalog and rent VOD")
            
            ''' Step 2 '''
            self.logStepBeginning("Step 2 - Select Subtitles item and validate")
    
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.actionSelect(Menu.toolboxNoSubtitleLong), "ERR: Problem finding Subtitle submenu on list") 
            time.sleep(1)
            
            self.logStepResults("Step 2 - Select Subtitles item and validate")
            
            ''' Step 3 '''
            self.logStepBeginning("Step 3 - Select Subtitles by pressing OK")
            
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(1)         
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            
            self.logStepResults("Step 3 - Select Subtitles by pressing OK")
            
            ''' Step 4 '''
            self.logStepBeginning("Step 4 - Check if Subtitles have changed")
            
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.findInList(Menu.toolboxOriginalSubtitle), "ERR: Problem checking if subtitles have changed")
            
            self.logStepResults("Step 4 - Check if Subtitles have changed")
                    
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")
            
            if status==False:
                
                self.rc.sendKeys(["KEY_STOP"])
                if self.page.findInList("czy napewno"):
                    self.assertTrue(self.page.actionSelect(Menu.pvrYes), "ERR: Problem exite vod") 
                self.rc.sendKeys(["KEY_tv"])