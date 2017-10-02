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
            self.logStepBeginning("Step 1 - Check live and go to standby")
            
            time.sleep(2)
            self.rc.sendKeys(["KEY_back"])
            time.sleep(1)
            self.rc.sendKeys(["KEY_back"])
            time.sleep(1)
            self.rc.sendKeys(["KEY_tv"])
            time.sleep(1)
            self.assertTrue(self.page.checkLive(), "ERR: no live") 
            time.sleep(1)
            self.rc.sendKeys(["KEY_power"])            
            time.sleep(25)
            
            
            self.logStepResults("Step 1 - Check live and go to standby")
            
            ''' Step 2 '''
            self.logStepBeginning("Step 2 - check if stb go to standby ")
            
            
            live =self.page.checkLive()
            if (live==True):
                self.assertTrue(False, "ERR: live after power button")
            time.sleep(25)
            self.rc.sendKeys(["KEY_power"])            

            self.logStepResults("Step 2 - check if stb go to standby ")
            

            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")
            
                
