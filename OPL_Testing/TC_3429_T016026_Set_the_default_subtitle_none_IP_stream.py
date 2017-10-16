# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3429_T016026_Set_the_default_subtitle_none_IP_stream(TC_OPL_template):
    '''
    Coverage: HP QC test ID - 3429 - T016026_Set the default subtitle - none - IP stream
    
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
            
            self.page.setParentalControl(ParentalControl.SetDeactive)
            time.sleep(2)
            self.rc.sendKeys(["KEY_MENU"])
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myAccount))
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.mySettings))
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
            self.logStepBeginning("STEP 4 - Choose 'brak' option and validate")
            
            self.assertTrue(self.page.actionSelect(Menu.noSubtitle)) 
                 
            self.logStepResults("STEP 4 - Choose 'brak' option and validate")
     
            ''' Step 5 '''
            self.logStepBeginning("STEP 5 - Watch a broadcasting DTT stream and check the subtitles")
            
            time.sleep(2)
            self.rc.sendKeys(["KEY_TV"])
            time.sleep(2)
            self.assertTrue(self.page.zapToChannel(self.rc.getChannelTVP1HD_dtt), " >> ERR in Zap to TVP1 DTT")
            time.sleep(8)
            self.rc.sendKeys(["KEY_OK"])
    
            self.assertTrue(self.page.findInList(Menu.toolboxNoSubtitleLong), "ERR: Problem checking if subtitles in toolbox have changed")
            
            self.logStepResults("STEP 5 - Watch a broadcasting DTT stream and check the subtitles")
     
            ''' Step 6 '''
            self.logStepBeginning("STEP 6 - Reaccess My account/My preferences/Subtitles and check subtitles")
            
            time.sleep(2)
            self.rc.sendKeys(["KEY_MENU"])
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myAccount))
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.mySettings))
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.subtitles)) 
            time.sleep(2)
            self.assertTrue(self.page.findInList(Menu.noSubtitle)) 
                 
            self.logStepResults("STEP 6 - Reaccess My account/My preferences/Subtitles and check subtitles")
     
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")
