# -*- coding: utf-8 -*-

 

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta

 

 

class TC_3668_T014556_watch_the_trailers_of_a_VOD_maturite_level_VOD_AND_Parental_conttrol_activated(TC_OPL_template):

    """Implementation of the HP QC test id 3668 T014556_watch_the_trailers_of_a_VOD_maturite_level_VOD_AND_Parental_conttrol_activated
 
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
            self.logStepBeginning("step 1 -  ParentalControl set none ")
            
            self.rc.sendKeys(["KEY_BACK"])
            self.rc.sendKeys(["KEY_BACK"])
            self.rc.sendKeys(["KEY_TV"])
            self.assertTrue(self.page.setParentalControl(ParentalControl.SetActiveCsa4),'ERR: SET ParentalControl')
            
            self.logStepResults("step 1 -  ParentalControl set none ")
    
    
            ''' step '''
            
            self.logStepBeginning("step 2 -  go to VOD and search csa4 vod")
            
            self.assertTrue(self.page.goToMenu(),'ERR in goToMenu')
            time.sleep(2)
            self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "ERR: Entering VOD Catalog")
            time.sleep(10)
            self.assertTrue(self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa4, ParentalControl.CssClassCsa5],trailerActive=True,count_vod_max_search=60), "   ERR   cannot get VPS info")
            time.sleep(4)
            self.logStepResults("step 2 - go to VOD and search csa4 vod")


            self.logStepBeginning("step 3 -  rent vod")
            
            self.assertTrue(self.page.actionSelect(Menu.vodTrailer),'ERR in enter to ' +Menu.vodTrailer)
            time.sleep(10)
            self.assertTrue(self.page.findInDialogBox("wprowadź kod dostępu"),'ERR none popup with kod dostepu ')
            time.sleep(3)
            self.rc.sendNumberSequence('3333')
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2) 
            self.assertTrue(self.page.findInDialogBox("błędny kod dostępu"),'ERR none popup with wrong kod dostepu ')            
            time.sleep(2)
            self.rc.sendNumberSequence(Env.PARENTAL_CODE)
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"]) 
            i=0
            while self.page.findInDialogBox("zwiastun") and i!=100:
                i=i+1
                time.sleep(3)
            self.rc.sendKeys(["KEY_OK"]) 
            time.sleep(10)
            if self.page.findInDialogBox("kontrola zakupów"):
                self.rc.sendNumberSequence(Env.PARENTAL_CODE)
                time.sleep(2)
                self.rc.sendKeys(["KEY_OK"])
                time.sleep(4) 
            self.assertTrue(self.page.findInDialogBox("Orange Polska S.A."),'ERR trailer do not open')              
            
            self.logStepResults("step 3 - rent vod")
            
            
            self.logStepBeginning("step 4 -   search csa1/2/3 vod and check")
            
            time.sleep(4)
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(4)           
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(4)
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(4)     
            self.assertTrue(self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa1, ParentalControl.CssClassCsa2, ParentalControl.CssClassCsa3],trailerActive=True,count_vod_max_search=60), "   ERR   cannot get VPS info")
            time.sleep(4)
            self.assertTrue(self.page.actionSelect(Menu.vodTrailer),'ERR in enter to ' +Menu.vodTrailer)
            while self.page.findInDialogBox("zwiastun") and i!=100:
                i=i+1
                time.sleep(3)
            self.rc.sendKeys(["KEY_OK"]) 
            time.sleep(10)
            if self.page.findInDialogBox("kontrola zakupów"):
                self.rc.sendNumberSequence(Env.PARENTAL_CODE)
                time.sleep(2)
                self.rc.sendKeys(["KEY_OK"])
                time.sleep(4) 
            self.assertTrue(self.page.findInDialogBox("Orange Polska S.A."),'ERR trailer do not open')  
            time.sleep(4)
            self.rc.sendKeys(["KEY_BACK","KEY_BACK","KEY_TV"])

            self.logStepResults("step  4 - search csa1/2/3 vod and check")
           
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")
            self.page.checkStbStatusIfKoReboot()
            self.page.setParentalControl(ParentalControl.SetDeactive)
            
            