# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData

 

 

class TC_3163_T014639_Navigate_into_tonight_programs(TC_OPL_template):

    """Implementation of the HP QC test ID - 3162 T014637_Navigate_into_EPG_all_program_grid
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

        self.rc.sendKeys(["KEY_BACK"]) 
        time.sleep(1)       
        self.rc.sendKeys(["KEY_TV"])
        time.sleep(1)
        self.rc.sendKeys(["KEY_GREEN"]) 
        time.sleep(1) 
        self.assertTrue(self.page.actionSelect(Menu.epg), "ERROR IN GO TO EPG(GREEN_BUTTON)")
        self.assertTrue(self.page.actionSelect(Menu.epgWeek), 'ERRPR IN GO TO EPG  Channels') 
        self.assertTrue(self.page.checkIfEpgIsAvalaible(), '>> ERROR  lack of EPG')
        self.logStepResults("STEP - Go To EPG all program channels")
        
        ''' step '''
        self.logStepBeginning("STEP -check working Key")
        self.assertTrue(self.page.checkWorkingEpgKey("KEY_LEFT", 'start'))
        self.assertTrue(self.page.checkWorkingEpgKey("KEY_RIGHT",'start'))
        self.assertTrue(self.page.checkWorkingEpgKey("KEY_DOWN","channelName"))
        self.assertTrue(self.page.checkWorkingEpgKey("KEY_UP","channelName"))
        self.assertTrue(self.page.checkWorkingEpgKey("KEY_FORWARD","channelName"))
        self.assertTrue(self.page.checkWorkingEpgKey("KEY_REWIND","channelName"))
        self.logStepResults("STEP - check working Key")
        


            
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        