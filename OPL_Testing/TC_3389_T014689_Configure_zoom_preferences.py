# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData
from _ast import Return
from datetime import datetime, timedelta
from NewTvTesting.StbtIntegration import *

 

 

class TC_3389_T014689_Configure_zoom_preferences(TC_OPL_template):

    """Implementation of the HP QC test ID - 3389 T014689_Configure_zoom_preferences
 
    @author: Tomasz Stasiuk
    """


       

    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)

   

    def test(self):
        
        
        
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")
    
           
    
            ''' prestep '''
    
            self.logStepResults("AT_THE_BEGINNING")
            time.sleep(3)
    
    
    
            ''' step '''
            
            self.logStepBeginning("step 1 - go to accessibiliy ")
            
            self.assertTrue(self.page.goToMenu(),'ERR:  GotoMenu')
            self.assertTrue(self.page.actionSelect(Menu.myAccount),'ERR:  GotoMenu>'+Menu.myAccount+'<')
            self.assertTrue(self.page.actionSelect(Menu.accessibiliy),'ERR:  GotoMenu>'+Menu.accessibiliy+'<')
            
            self.logStepResults("step 1 - go to accessibiliy")
            
            ''' step '''
            
            self.logStepBeginning("STEP 2 - check accessibilityIcon off ")
            find = self.page.findAccessibilityIcon()
            if find==None:
                time.sleep(1)
            else:
                try:
                    self.assertTrue(self.page.actionSelect(Menu.zoomNo),'ERR: select>'+Menu.zoomNo+'<')
                except:
                    self.assertTrue(self.page.actionSelect(Menu.zoomYes),'ERR: select>'+Menu.zoomYes+'<')
                time.sleep(3)
                self.assertTrue(self.page.actionSelect(Menu.deactivate),'ERR: select>'+Menu.deactivate+'<')
                time.sleep(5)
                self.assertTrue(self.page.actionSelect(Menu.confirm),'ERR: select>'+Menu.confirm+'<')
                time.sleep(5)
                try:
                    self.assertTrue(self.page.actionSelect(Menu.audioDescriptionNo),'ERR: select>'+Menu.audioDescriptionNo+'<')
                except:
                    self.assertTrue(self.page.actionSelect(Menu.audioDescriptionYes),'ERR: select>'+Menu.audioDescriptionYes+'<')
                time.sleep(3)
                self.assertTrue(self.page.actionSelect(Menu.deactivate),'ERR: select>'+Menu.deactivate+'<')

                time.sleep(20)
           
            self.logStepResults("STEP 2 - check accessibilityIcon off")
            
            ''' step '''
            self.logStepBeginning("STEP 3 - select zoom and check popup")
            self.assertTrue(self.page.actionSelect(Menu.zoomNo),'ERR: select>'+Menu.zoomNo+'<')
            self.assertTrue(self.page.findInPage(Menu.activate),'ERR:  find>'+Menu.activate+'<')
            self.assertTrue(self.page.findInPage(Menu.deactivate),'ERR:  find>'+Menu.deactivate+'<')
            self.logStepResults("STEP 3 - select zoom and check popup")
            
            ''' step '''
            self.logStepBeginning("STEP 4 - Turn off pop-up after 30 sec")
            self.assertTrue(self.page.actionSelect(Menu.activate),'ERR: select>'+Menu.activate+'<')
            time.sleep(40)
            self.assertFalse(self.page.findInPage(Menu.confirm),'ERR: find>'+Menu.confirm+'<')
            self.logStepResults("STEP 4 - Turn off pop-up after 30 sec")
        
            ''' step '''
            self.logStepBeginning('STEP 5 -Turn On zoom')
            self.assertTrue(self.page.actionSelect(Menu.zoomNo),'ERR: select>'+Menu.zoom+'<')
            time.sleep(3)
            self.assertTrue(self.page.actionSelect(Menu.activate),'ERR: select>'+Menu.activate+'<')
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(Menu.confirm),'ERR: select>'+Menu.confirm+'<')
            time.sleep(2)
            self.logStepResults('STEP 5  - Turn On zoom')
            
            ''' step '''
            self.logStepBeginning('STEP 6 -check zoom')
            find = self.page.findAccessibilityIcon()
            if find==True:
                time.sleep(1)
            else:
                self.assertTrue(False, "  >>  ERR: None active zoom")
            time.sleep(2)
            self.logStepResults('STEP 6 -check zoom')
     
            
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")
            time.sleep(5)
            self.page.checkStbStatusIfKoReboot()
            self.rc.sendKeys(["KEY_BACK","KEY_BACK","KEY_TV"])
            self.page.goToMenu()
            self.page.actionSelect(Menu.myAccount)
            self.page.actionSelect(Menu.accessibiliy)
            a=self.page.actionSelect(Menu.zoomNo)
            if a==False:
                self.page.actionSelect(Menu.zoomYes)
            time.sleep(3)
            self.page.actionSelect(Menu.deactivate)
            try:
                self.page.actionSelect(Menu.confirm)
            except:
                time.sleep(5)
            time.sleep(20)
            self.rc.sendKeys(["KEY_BACK","KEY_BACK","KEY_TV"])     