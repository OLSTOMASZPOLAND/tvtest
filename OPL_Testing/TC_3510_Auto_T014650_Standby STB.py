# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time
from NewTvTesting.StbtIntegration import motionDetection

class TC_3510_Auto_T014650_Standby_STB(TC_OPL_template):
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

            ''' Step 1 '''
            self.logStepBeginning("Step 1 - Enter VOD Catalog and rent VOD")
            
            time.sleep(2)
            self.assertTrue(self.rc.sendKeys(["KEY_back"]), "ERR: key back")
            time.sleep(1)
            self.assertTrue(self.rc.sendKeys(["KEY_back"]), "ERR: key back")
            time.sleep(1)
            self.assertTrue(self.rc.sendKeys(["KEY_tv"]), "ERR: key back")
            time.sleep(1)
            self.assertTrue(self.page.checkLive(), "ERR: check live") 
            time.sleep(1)
            self.assertTrue(self.rc.sendKeys(["KEY_power"]), "ERR: key back")            
            time.sleep(25)
            
            status=False
            
            self.logStepResults("Step 1 - Enter VOD Catalog and rent VOD")
            
            ''' Step 2 '''
            self.logStepBeginning("Step 2 - Select Subtitles item and validate")
    
            self.assertFalse(self.page.checkLive(), "ERR: check live") 
            
            self.logStepResults("Step 2 - Select Subtitles item and validate")
            

            
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
