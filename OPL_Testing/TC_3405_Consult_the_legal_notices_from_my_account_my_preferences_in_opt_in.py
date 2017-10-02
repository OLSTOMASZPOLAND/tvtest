# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData
from wheel.signatures import assertTrue

 

 
class TC_3405_Consult_the_legal_notices_from_my_account_my_preferences_in_opt_in(TC_OPL_template):
    """
    Implementation of the HP QC test ID 3405 T0151211_consult_the_legal_notices_from_myy_account_my_preferences_in_opt_in
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
            self.logStepBeginning("STEP 1- Set deactivate Recommendation ")
            self.assertTrue(self.page.setRecommendation('activate'),'ERR in set deactivate Recommendation')
            self.logStepResults("STEP 1- Set deactivate Recommendation ")
        
            ''' step '''
            self.logStepBeginning("STEP 2- Go to Recommendation")
            self.assertTrue(self.page.goToMenu(), 'ERR in Go to Menu')
            self.assertTrue(self.page.goToMySettings(), 'ERR in Go to My Preferences')
            self.assertTrue(self.page.actionSelect(Menu.personalizedSuggestion),'ERR in Go Recommendation')
            self.logStepResults("STEP 2- Go to Recommendation")
    
    
            ''' step '''
            self.logStepBeginning("STEP 3- check Description info")
            time.sleep(4)
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(2)
            assertTrue(self.page.findInPage(Description.IsActivatedRecommendation),"ERR in find >"+Description.IsActivatedRecommendation+"<")
            time.sleep(5)
            self.rc.sendKeys(["KEY_OK"])
            self.logStepResults("STEP 3- Go to Recommendation")
    
    
            ''' step '''
            self.logStepBeginning("STEP 4 - Check Recommendation popup")  
            time.sleep(5)   
            self.assertTrue(self.page.findInPage(Menu.legalInformation),'ERR in finding >'+Menu.legalInformation+"<")
            self.assertTrue(self.page.findInPage(Menu.myViewershipRecommendation),'ERR in finding >'+Menu.myViewershipRecommendation+"<")
            self.assertTrue(self.page.findInPage(Menu.deactivate),'ERR in finding >'+Menu.activate+"<")
            self.logStepResults("STEP 4 - Check Recommendation popup")
             
            ''' step '''
            self.logStepBeginning("STEP 5 - Check legalInformation")  
            time.sleep(5)   
            self.assertTrue(self.page.actionSelect(Menu.legalInformation),'ERR in Go Recommendation')
            time.sleep(5)
            self.assertTrue(self.page.findInPage('pomiń'),'ERR in finding pomiń')
            time.sleep(2)
            self.rc.sendKeys(["KEY_BACK"])
            self.logStepResults("STEP 5 - Check legalInformation")
            
            
            ''' step '''
            self.logStepBeginning("STEP 6 - Check Recommendation popup")  
            time.sleep(5)   
            self.assertTrue(self.page.findInPage(Menu.legalInformation),'ERR in finding >'+Menu.legalInformation+"<")
            self.assertTrue(self.page.findInPage(Menu.myViewershipRecommendation),'ERR in finding >'+Menu.myViewershipRecommendation+"<")
            self.assertTrue(self.page.findInPage(Menu.deactivate),'ERR in finding >'+Menu.activate+"<")
            self.logStepResults("STEP 6 - Check Recommendation popup")
            
            ''' step '''
            self.logStepBeginning("STEP 6 - Check Recommendation popup secound time")  
            time.sleep(5)   
            self.assertTrue(self.page.findInPage(Menu.legalInformation),'ERR in finding >'+Menu.legalInformation+"<")
            self.assertTrue(self.page.findInPage(Menu.myViewershipRecommendation),'ERR in finding >'+Menu.myViewershipRecommendation+"<")
            self.assertTrue(self.page.findInPage(Menu.deactivate),'ERR in finding >'+Menu.activate+"<")
            self.logStepResults("STEP 6 - Check Recommendation secound time")
            
            ''' step '''
            self.logStepBeginning("STEP 6 - Check Recommendation popup secound time")  
            time.sleep(5)   
            self.rc.sendKeys(["KEY_BACK","KEY_BACK","KEY_TV"])
            time.sleep(20)
            self.assertTrue(self.page.goToMenu(), 'ERR in Go to Menu')
            self.assertTrue(self.page.goToMySettings(), 'ERR in Go to My Preferences')
            self.assertTrue(self.page.actionSelect(Menu.personalizedSuggestion),'ERR in Go Recommendation')
            self.assertTrue(self.page.findInPage(Menu.legalInformation),'ERR in finding >'+Menu.legalInformation+"<")
            self.assertTrue(self.page.findInPage(Menu.myViewershipRecommendation),'ERR in finding >'+Menu.myViewershipRecommendation+"<")
            self.assertTrue(self.page.findInPage(Menu.deactivate),'ERR in finding >'+Menu.activate+"<")
            self.rc.sendKeys(["KEY_BACK"])
            assertTrue(self.page.findInPage(Description.IsActivatedRecommendation),"ERR in find >"+Description.IsActivatedRecommendation+"<")
            self.logStepResults("STEP 6 - Check Recommendation secound time")
            
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")
            time.sleep(5)
            self.page.checkStbStatusIfKoReboot()
            self.page.setRecommendation('deactivate')
        