# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3386_T014538_Set_the_default_subtitle_hearing_impaired_VOD(TC_OPL_template):
    '''
    Coverage: HP QC test ID - 3386 - T014538_Set the default subtitle - hearing impaired - VOD
    
    @author: Kamil Kulinski
    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        try:
            
            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            
            ''' Initial State '''
            self.logStepBeginning("Initial State - User is in My account - My preferences screen")
            
            status=True
            
            self.page.setParentalControl(ParentalControl.SetDeactive)
            time.sleep(2)
            self.rc.sendKeys(["KEY_MENU"])
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "ERR: Entering My Account")
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.mySettings), "ERR: Entering My Settings")
            time.sleep(2)
            
            self.logStepResults("Initial State - User is in My account - My preferences screen")
            
            ''' Step 3 '''
            self.logStepBeginning("Step 3 - Select subtitles item")
            
            self.assertTrue(self.page.actionSelect(Menu.subtitles)) 
            time.sleep(2)
            
            self.assertTrue(self.page.findInList(Menu.noSubtitle), "ERR: no 'brak' option in 'napisy' menu")
            self.assertTrue(self.page.findInList(Menu.nativeSubtitles), "ERR: no 'polskie' option in 'napisy' menu")
            self.assertTrue(self.page.findInList(Menu.hearingImpairedSubtitles), "ERR: no 'dla nieslyszacych' option in 'napisy' menu")
            time.sleep(2)
            
            self.logStepResults("STEP 3 - Select subtitles item")
           
            ''' Step 4 '''
            self.logStepBeginning("STEP 4 - Choose 'dla nieslyszacych' option and validate")
            
            self.assertTrue(self.page.actionSelect(Menu.hearingImpairedSubtitles), "ERR: Choosing Hearing Impaired option in 'napisy' menu") 
                 
            self.logStepResults("STEP 4 - Choose 'dla nieslyszacych' option and validate")
    
            ''' Step 5 '''
            self.logStepBeginning("STEP 5 - Watch a VOD and check the subtitles")
            
            time.sleep(2)
            self.assertTrue(self.page.goToVodCatalog(Menu.vodPolishMovies), "ERR: Entering VOD Catalog")
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(Menu.VOD_subtitles), "ERR: Entering VOD VPS") 
            time.sleep(10)
            self.assertTrue(self.page.rentAndPlayOrPlayRentedVod(), "ERR: Renting VOD")
            time.sleep(10)
            
            status=False
            
            self.rc.sendKeys(["KEY_OK"])
    
            self.assertTrue(self.page.findInList(Menu.toolboxHearingImpairesSubtitles), "ERR: Problem checking if subtitles in VOD toolbox have changed")
            time.sleep(2)
            
            self.logStepResults("STEP 5 - Watch a VOD and check the subtitles")
     
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
                self.rc.sendKeys(["KEY_DOWN"])
                self.rc.sendKeys(["KEY_OK"])
                
                self.rc.sendKeys(["KEY_BACK"])
                self.rc.sendKeys(["KEY_BACK"])
                self.rc.sendKeys(["KEY_TV"])
                
                
                time.sleep(2)
                self.rc.sendKeys(["KEY_MENU"])
                time.sleep(2)
                self.assertTrue(self.page.actionSelect(Menu.myAccount), "ERR: Entering My Account")
                time.sleep(2)
                self.assertTrue(self.page.actionSelect(Menu.mySettings), "ERR: Entering My Settings")
                time.sleep(2)
                self.assertTrue(self.page.actionSelect(Menu.subtitles), "ERR: Entering Subtitles Menu")  
                time.sleep(2)
                self.assertTrue(self.page.findInList(Menu.hearingImpairedSubtitles)) 
                time.sleep(2)
                self.assertTrue(self.page.actionSelect(Menu.noSubtitle), "ERR: Choosing 'brak' option in 'napisy' menu")