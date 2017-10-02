# -*- coding: utf-8 -*-
import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

class TC_E701_ParentalControlAndVodMenu(TC_OPL_template):
    """Endurance test - during 200 minutes it sets parental control and goes to specific VoD catalog in the loop
    
    @author: Leszek Wawrzonkowski
    """
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        testLengthInMinutes = 200
        self.logger.debug("----- testLengthInMinutes >" + str(testLengthInMinutes) + "< ----- ")
        
        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")
        
        testLength = testLengthInMinutes*60
        
        startTimestamp = time.time()
        while True:
            if (time.time() - startTimestamp > testLength):
                break
            
            ''' step '''
            self.logStepBeginning("STEP - set no parental control")
            self.assertTrue(self.page.setParentalControl(ParentalControl.SetDeactive))
            self.logStepResults("STEP - set no parental control")
        
            ''' step '''
            self.logStepBeginning("STEP - go to VOD catalog")
            self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent))
            self.logStepResults("STEP - go to VOD catalog")
            
            ''' step '''
            self.logStepBeginning("STEP - go to VOD adults catalog")
            self.assertTrue(self.page.goToVodAdults())
            self.assertTrue(self.page.actionSelect(Menu.vodAdultCatalogWithTestContent))
            self.logStepResults("STEP - go to VOD adults catalog")
        
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")