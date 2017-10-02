# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData
from wheel.signatures import assertTrue

 

 

class TC_3396_T015183_consult_recommendation_implicite_profile_in_opt_in_mode_csa4_5(TC_OPL_template):

    """
    Implementation of the HP QC test ID 3396 T015183_consult_recommendation_implicite_profile_in_opt_in_mode_csa4_5
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
            self.assertTrue(self.page.setRecommendation('deactivate'),'ERR in set deactivate Recommendation')
            self.logStepResults("STEP 1- Set deactivate Recommendation ")
        
            ''' step '''
            self.logStepBeginning("STEP 2- Go to Recommendation")
            self.assertTrue(self.page.goToMenu(), 'ERR in Go to Menu')
            self.assertTrue(self.page.goToMySettings(), 'ERR in Go to My Preferences')
            self.assertTrue(self.page.actionSelect(Menu.personalizedSuggestion),'ERR in Go Recommendation')
            self.logStepResults("STEP 2- Go to Recommendation")
    
    
            ''' step '''
            self.logStepBeginning("STEP 3- check Description info")
            self.rc.sendKeys(["KEY_BACK"])
            assertTrue(self.page.findInPage(Description.IsDeactivatedRecommendation),"ERR in find >"+Description.IsActivatedRecommendation+"<")
            time.sleep(5)
            self.rc.sendKeys(["KEY_OK"])
            self.logStepResults("STEP 3- Go to Recommendation")
    
    
            ''' step '''
            self.logStepBeginning("STEP 4 - Check Recommendation popup")  
            time.sleep(5)   
            self.assertTrue(self.page.findInPage(Menu.legalInformation),'ERR in finding >'+Menu.legalInformation+"<")
            self.assertTrue(self.page.findInPage(Menu.myViewershipRecommendation),'ERR in finding >'+Menu.myViewershipRecommendation+"<")
            self.assertTrue(self.page.findInPage(Menu.activate),'ERR in finding >'+Menu.activate+"<")
            self.logStepResults("STEP 4 - Check Recommendation popup")
             
            ''' step '''
            self.logStepBeginning("STEP 5 - Check manage customer data")  
            ''
            time.sleep(5)
            self.assertTrue(self.page.actionSelect(Menu.activate),'ERR in Go to >'+Menu.activate+"<")
            time.sleep(5)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(15)
            self.assertTrue(self.page.actionSelect(Menu.personalizedSuggestion),'ERR in Go to >'+Menu.activate+"<")
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myViewershipRecommendation), 'ERR in Go to >'+Menu.myViewershipRecommendation+"<")
            time.sleep(10)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(2)
            moje = self.page.driver.find_elements_by_css_selector('html body div#manageDataDialog.dialog.question.datas div.wrapper div.box div.content div.recocontent div span.orange.recoresult')
            i=0
            while (i!=3):
                change = moje[i].text.encode('utf-8')
                if not change=='brak':
                    self.assertTrue(False, "  >>   ERR: No brak in >"+Menu.myViewershipRecommendation+"<")
                i=i+1
            time.sleep(5)
            self.logStepResults("STEP 5 - Check manage customer data")
                  
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
            self.page.setRecommendation('deactivate')
        