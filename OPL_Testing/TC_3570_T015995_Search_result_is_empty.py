# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData

 

 

class TC_3570_T015995_Search_result_is_empty(TC_OPL_template):


    """Implementation of the HP QC test ID - 3570_T015995_Search_result_is_empty
    @author: Tomasz Stasiuk
    """

       

    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)

   
    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''

        self.logStepResults("AT_THE_BEGINNING")
        time.sleep(1)

        
       
        ''' step '''

        self.logStepBeginning("STEP 1 - Go to Search menu")

        self.assertTrue(self.page.goToMenu(), "ERROR IN GO TO MENU")
        time.sleep(2)
        self.assertTrue(self.page.actionSelect(Menu.vodSearch), "ERROR IN GO TO Search")
        time.sleep(2)
        self.assertTrue(self.page.actionSelect(Menu.videoOnDemand), "ERROR IN GO TO VOD Search")
        self.logStepResults("STEP 1 - Go to Search menu")                
        
        ''' step '''
        self.logStepBeginning("STEP 2 - send word in vod search and check if popup")     
        time.sleep(2)
        self.rc.sendWord('xyzy2')
        time.sleep(2)
        self.assertTrue(self.page.findInPage(Description.vodSearchNone), "No found" + Description.vodSearchNone)
        time.sleep(2)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(2)
        self.assertTrue(self.page.findInPage(u"Spróbuj wpisać do wyszukiwarki inne słowo lub zamknij klawiaturę.".encode('utf-8')), "No found popup")
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(2)
        self.assertFalse(self.page.findInPage(Description.vodSearchNonePopup), " found popup")
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        self.logStepResults("STEP 2 - send word in vod search ")
        
        
        
            
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
