# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData

 

 

class TC_9638_T015566_Navigate_Intu_EPG_Favourite_Grid(TC_OPL_template):


    """Implementation of the HP QC test ID - 9638 T015566_Navigate_Intu_EPG_Favourite_Grid
    @author: Tomasz Stasiuk
    """

       

    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)

   
    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")
    
            ''' prestep '''
    
            self.logStepResults("AT_THE_BEGINNING")
            time.sleep(1)
    
            
           
            ''' step '''
    
            self.logStepBeginning("STEP 1 - Switch ON k favorite channels from menu")
            k=9 #number of added favorite channels
    
            self.rc.sendKeys(["KEY_MENU"])     
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "ERROR IN GO TO MY ACCOUNT")
    
            self.assertTrue(self.page.actionSelect(Menu.mySettings), "ERROR IN GO TO MY Settings")
    
            self.assertTrue(self.page.actionSelect(Menu.myChannels), "ERROR IN GO TO MY Channels")
            
            self.assertTrue(self.page.turnOnFavouriteChannels(k), "ERROR IN Turn on k Favourite Channels")
            self.rc.sendKeys(["KEY_BACK"])
            if not (self.page.findInPage(Description.favoriteZeroChannels)):  
                self.rc.sendKeys(["KEY_OK"])
                time.sleep(2)
                self.rc.sendKeys(["KEY_DOWN"])
                time.sleep(1)
                self.rc.sendKeys(["KEY_UP"])
                time.sleep(1)
                heartt = self.page.getFavoriteChannelListItemOnList().favorite
                if (heartt==True):
                    time.sleep(1)
                else:
                    self.assertTrue(False, "No  channels in favorites list")
            else:
                self.logger.info("0 channels in favorites list")
            
            self.logStepResults("STEP 1 - Switch ON k favorite channels from menu")        
            
            
            ''' step '''
            self.logStepBeginning("STEP 2 - Go To EPG favorite channels")     
    
            self.rc.sendKeys(["KEY_BACK"]) 
            time.sleep(1)       
            self.rc.sendKeys(["KEY_TV"])
            time.sleep(1)
            self.rc.sendKeys(["KEY_GREEN"]) 
            time.sleep(1) 
            self.assertTrue(self.page.actionSelect(Menu.epg), "ERROR IN GO TO EPG(GREEN_BUTTON)")
            self.assertTrue(self.page.actionSelect(Menu.epgMyChannels), 'ERRPR IN GO TO EPG Favorites Channels') 
            self.assertTrue(self.page.checkIfEpgIsAvalaible(),'Lack of EPG')
            self.logStepResults("STEP 2 - Go To EPG favorite channels")
            
            
            ''' step '''
            self.logStepBeginning("STEP 3 -check working Key")
            self.assertTrue(self.page.checkWorkingEpgKey("KEY_LEFT", 'start'))
            self.assertTrue(self.page.checkWorkingEpgKey("KEY_RIGHT", 'start'))
            self.assertTrue(self.page.checkWorkingEpgKey("KEY_DOWN", 'channelName'))
            self.assertTrue(self.page.checkWorkingEpgKey("KEY_UP", 'channelName'))
            self.assertTrue(self.page.checkWorkingEpgKey("KEY_FORWARD", 'channelName'))
            self.assertTrue(self.page.checkWorkingEpgKey("KEY_REWIND", 'channelName'))
            self.logStepResults("STEP 3 - check working Key")
            ''' step '''
            
                
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
            self.page.cleanTurnOffAllFavoriteChannels()