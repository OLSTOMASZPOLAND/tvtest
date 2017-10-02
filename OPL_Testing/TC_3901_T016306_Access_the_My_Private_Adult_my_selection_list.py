# -*- coding: utf-8 -*-

 

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta

 

 

class TC_3901_T016306_Access_the_My_Private_Adult_my_selection_list(TC_OPL_template):

    """Implementation of the HP QC test id 3901 T016306_Access_the_My_Private_Adult_my_selection_list
 
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
            
            self.logStepBeginning("step 1 -  Go to adult VOD and delete vods in my favorite")

            self.assertTrue(self.page.goToMenu(),'ERR: in go to Menu')
            time.sleep(5)
            self.assertTrue(self.page.actionSelect(Menu.videoOnDemand),'ERR: in go to VOD')
            time.sleep(5)
            self.assertTrue(self.page.goToVodAdults(fromVodMenu=True),'ERR: in go to adult VOD')
            time.sleep(5)
            self.assertTrue(self.page.actionSelect(Menu.vodMyFavorites),'ERR: in go to my favorite')
            time.sleep(10)
            myFavorite = self.page.findInList(Menu.vodMyFavorites)
            i=0
            time.sleep(1)
            while not (myFavorite):
                i=i+1
                if i==30:
                    self.assertTrue(False, '  >>  ERR more then 30 add adult vod in my favorite')
                self.rc.sendKeys(["KEY_OK"])
                self.assertTrue(self.page.actionSelect(Menu.vodRemoveFromFavorites),'ERR: in uncheck adult vod from my favorite')
                self.rc.sendKeys(["KEY_BACK"])
                time.sleep(5)
                myFavorite = self.page.findInList(Menu.vodMyFavorites)
            time.sleep(5)
            
            self.logStepResults("step 1 -  Go to adult VOD and delete vod in my favorite")
    
    
            ''' step '''
            
            self.logStepBeginning("step 2 -  add a adult vod to my favorite")
            
            self.assertTrue(self.page.actionSelect(Menu.vodAdultCatalogWithTestContent),'ERR: in go to VOD adult catalog')
            time.sleep(4)           
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)           
            self.assertTrue(self.page.actionSelect(Menu.vodAddToFavorites),'ERR: in select adult vod to my favorite')
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(4)           
            self.rc.sendKeys(["KEY_BACK"])            
            time.sleep(4)        
                       
            self.logStepResults("step 2 - add a adult vod to my favorite")


            self.logStepBeginning("step 3 -  go to VOD and check live")
            
            self.assertTrue(self.page.actionSelect(Menu.vodMyFavorites),'ERR: in go to my favorite')
            time.sleep(4)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(5)
            self.assertTrue(self.page.rentAndPlayOrPlayRentedVod(),'ERR: in play adult V0D')
            time.sleep(15)
            self.assertTrue(self.page.checkLive(pvrAndVod=True),'ERR: No live in VOD')
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(5)
            if self.page.findInDialogBox("Czy na pewno chcesz go zatrzymać"):
                self.assertTrue(self.page.actionSelect(Menu.vodStopWatching),'ERR: SET in selecting zatrzymaj')
            time.sleep(6)

            
            self.logStepResults("step 3 - go to VOD and check live ")
            
            
            self.logStepBeginning("step 4 - check VPS ")
            time.sleep(2)
            vodCatalog1 = self.page.getInfoFromVodPage()
            if not (type(vodCatalog1) is VodItem):
                self.assertTrue(False, '  >>  ERR wrong type of VPS ')
            vodTitle1 = vodCatalog1.title
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(4)           
            self.rc.sendKeys(["KEY_BACK"])            
            time.sleep(4)                
            self.logStepResults("step  4 - check VPS")  
            
            
                      
            self.logStepBeginning("step 5 - check if vod is in my selections ")
            self.assertTrue(self.page.actionSelect(Menu.vodMyFavorites),'ERR: in go to my favorite')
            time.sleep(4)           
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(6)    
            vodCatalog2 = self.page.getInfoFromVodPage()
            if not (type(vodCatalog2) is VodItem):
                self.assertTrue(False, '  >>  ERR wrong type of VPS ')
            vodTitle2 = vodCatalog2.title            
            
            if vodTitle1!=vodTitle2:
                self.assertTrue(False, '  >>other title of VOD  ')
            time.sleep(6)    
                                                
            self.logStepResults("step  5 - check if vod is in my selections")
            
            self.logStepBeginning("step 6 - uncheck vod from my selection and check folder my selection")

            self.assertTrue(self.page.actionSelect(Menu.vodRemoveFromFavorites),'ERR: in go to my favorite')
            time.sleep(4)           
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(10)
            if not self.page.findInList(Menu.vodMyFavorites):
                self.assertTrue(False, '  >>  ERR vod do not remove from my favorite')

            self.logStepResults("step  6 -uncheck vod from my selection and check folder my selection")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")
            
            if not self.test_passed:
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                
                self.page.checkStbStatusIfKoReboot()
                
                self.page.goToMenu()
                time.sleep(5)
                self.page.actionSelect(Menu.videoOnDemand)
                time.sleep(5)
                self.page.goToVodAdults(fromVodMenu=True)
                time.sleep(5)
                self.page.actionSelect(Menu.vodMyFavorites)
                time.sleep(10)
                myFavorite = self.page.findInList(Menu.vodMyFavorites)
                i=0
                time.sleep(1)
                while not (myFavorite):
                    i=i+1
                    if i==30:
                        break
                    self.rc.sendKeys(["KEY_OK"])
                    self.page.actionSelect(Menu.vodRemoveFromFavorites)
                    self.rc.sendKeys(["KEY_BACK"])
                    time.sleep(5)
                    myFavorite = self.page.findInList(Menu.vodMyFavorites)
                time.sleep(5)
            
            
            