# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData


 

 

class TC_3150_TC_3151_T014616_T014617_Add_and_Remove_an_alarts(TC_OPL_template):

    """Implementation of the HP QC test ID - 3150 and 3151 -    T014616_Add_an_alarts
                                                                T014617_Remove_an_alarts
 
    @author: Tomasz Stasiuk
    """

       

    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)

   

    def test(self):
        
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

       

        ''' prestep '''

        self.logStepResults("AT_THE_BEGINNING")
        time.sleep(3)
             
        
        
        ''' step '''
        self.logStepBeginning("STEP - Go To EPG all program channels")     

        self.rc.sendKeys(["KEY_GREEN"]) 
        time.sleep(1) 
        self.assertTrue(self.page.actionSelect(Menu.epg), "ERROR IN GO TO EPG(GREEN_BUTTON)")
        self.assertTrue(self.page.actionSelect(Menu.epgWeek), 'ERRPR IN GO TO EPG all program Channels') 

        self.logStepResults("STEP - Go To EPG all program channels")

        ''' step '''
        self.logStepBeginning("STEP - Go To  channel 3 in EPG and go to future")
        
        self.assertTrue(self.page.checkIfEpgIsAvalaible(), '>> ERROR  lack of EPG')
        time.sleep(2)
        self.rc.sendKeys(["KEY_3"])
        time.sleep(3)
        self.rc.sendKeys(["KEY_RIGHT"])
        time.sleep(3)
        self.rc.sendKeys(["KEY_RIGHT"])
        time.sleep(3)
        self.rc.sendKeys(["KEY_RIGHT"])
        time.sleep(10)
        self.logStepResults("STEP - Go To  channel 3 in EPG and go to future")
        ''' step '''
        
        
        ''' step '''
        self.logStepBeginning("STEP - Set alert ON")     
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(3)
        self.assertTrue(self.page.actionSelect(Menu.epgAlertOn), 'Error in set alert on')
        time.sleep(15)
        self.logStepResults("STEP - set alert ON")
        ''' step '''

        ''' step '''
        self.logStepBeginning("STEP - check alert ON")     
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(3)
        self.rc.sendKeys(["KEY_RIGHT"])
        time.sleep(3)
        self.rc.sendKeys(["KEY_LEFT"])
        time.sleep(5)
        self.assertTrue(self.page.getInfoFromEpgFocus().reminder, 'Bell not found')

        self.logStepResults("STEP - check alert ON")
        ''' step '''
        
        ''' step '''
        self.logStepBeginning("STEP - Set alert OFF")     
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(3)
        self.page.actionSelect(Menu.epgAlertOff)
        time.sleep(5)
        self.logStepResults("STEP - set alert OFF")
        ''' step '''
        
        ''' step '''
        self.logStepBeginning("STEP - check alert OFF")     
        self.rc.sendKeys(["KEY_BACK"])
        time.sleep(3)
        self.rc.sendKeys(["KEY_RIGHT"])
        time.sleep(3)
        self.rc.sendKeys(["KEY_LEFT"])
        time.sleep(5)
        self.assertFalse(self.page.getInfoFromEpgFocus().reminder, 'Bell found')

        self.logStepResults("STEP - check alert OFF")
        ''' step '''
         
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        