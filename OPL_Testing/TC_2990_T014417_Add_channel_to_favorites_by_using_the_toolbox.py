# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData
from _ast import Return


 

 

class TC_2990_T014417_Add_channel_to_favorites_by_using_the_toolbox(TC_OPL_template):

    """Implementation of the HP QC test ID - 2990 - T014417_Add_channel_to_favorites_by_using_the_toolbox
 
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
            self.logStepBeginning("STEP 1- Turn off all favorite channels")
            self.page.cleanTurnOffAllFavoriteChannels()
            self.logStepResults("STEP 1- Turn off all favorite channels")
            
            ''' step '''
            self.logStepBeginning("STEP 2-Turn on favorite in channel 3 ")
            time.sleep(3)  
            self.rc.sendKeys(["KEY_3"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.actionSelect(Menu.toolboxFavouriteChannelsNo), 'Error in finding in toolbox favorite channel')
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.toolbox_2_favouriteChannelYes), 'Error in changing favorite channel')
            time.sleep(1)
            self.logStepResults("STEP 2- Turn on favorite in channel 3 ")
            
            
            ''' step '''
            self.logStepBeginning("STEP 3-check if channel 3 it is favorite channel (toolbox)")   
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.checkIfInToolboxIsHeartIcon(), 'Heart not found')
            self.assertTrue(self.page.findInPage(Menu.toolboxFavouriteChannelsYes), 'Error no "yes" in toolbox')
            time.sleep(1)
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(5)
            self.logStepResults("STEP 3- check if channel 3 it is favorite channel (toolbox)")
    
            ''' step '''
            self.logStepBeginning("STEP 4-check if channel 3 have heart in information banner")     
            self.rc.sendKeys(["KEY_INFO"])
            time.sleep(4)
            favoriteinchannels3 = self.page.getInfoFromLiveBanner().favorite
            #print favoriteinchannels3
            time.sleep(1)
            if favoriteinchannels3==True:
                self.logger.info("  >>  Heart is in information banner")
            else:
                self.assertTrue(False, "  >>   ERR: None heart in information banner")
            self.rc.sendKeys(["KEY_BACK"])
            self.logStepResults("STEP 4- check if channel 3 have heart in information banner")
            
            ''' step '''
            self.logStepBeginning("STEP 5-check if channel 3 have heart in LIST channels")     
            self.rc.sendKeys(["KEY_LIST"])
            time.sleep(4)
            lista = self.page.findInPage(Description.favoriteInList)
            l=1
            if not (lista==True):
                while (l<20):
                    l=l+1
                    self.rc.sendKeys(["KEY_LEFT"])
                    time.sleep(4)
                    lista = self.page.findInPage(Description.favoriteInList)
                    if (lista==True):
                        l=20
                    #print l
            time.sleep(5)
            listchannels3 = self.page.findInPage('3. ')
            #print listchannels3
            if not (listchannels3==True):
                self.assertTrue(False, "  >>  ERR channel 3 is not in favorite channel list  ")
            else:
                self.logger.info("  >> channel 3 is in favorite channel list ")
            #time.sleep(120)
            self.logStepResults("STEP 5- check if channel 3 have heart in LIST channels")
            
            ''' step '''
            self.logStepBeginning("STEP 6-check if channel 3 have heart in Favorite list")     
            self.rc.sendKeys(["KEY_MENU"])     
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "ERROR IN GO TO MY ACCOUNT")
            self.assertTrue(self.page.actionSelect(Menu.mySettings), "ERROR IN GO TO MY Settings")
            self.assertTrue(self.page.actionSelect(Menu.myChannels), "ERROR IN GO TO MY Channels")
            self.rc.sendKeys(["KEY_DOWN"])     
            time.sleep(2)
            self.rc.sendKeys(["KEY_DOWN"])     
            time.sleep(2)
            heart = self.page.getFavoriteChannelListItemOnList().favorite
           # heart = self.page.findInXPathElementClass("checked", "//div[contains(@class, 'slide')]")
            if not (heart==True):
                self.assertTrue(False, "  >>  ERR channel 3 isn't in favorite list")
            else:
                self.logger.info("  >>   channel 3 is in favorite list")
            self.logStepResults("STEP 6-check if channel 3 have heart in Favorite list")
            
            ''' step '''
            self.logStepBeginning("STEP 7-check if channel 3 in EPG(favorite) have heart")     
            self.rc.sendKeys(["KEY_BACK"]) 
            time.sleep(1)       
            self.rc.sendKeys(["KEY_TV"])
            time.sleep(1)
            self.rc.sendKeys(["KEY_GREEN"]) 
            time.sleep(3) 
            self.assertTrue(self.page.actionSelect(Menu.epg), "ERROR IN GO TO EPG(GREEN_BUTTON)")            
            self.assertTrue(self.page.actionSelect(Menu.epgMyChannels), 'ERRPR IN GO TO EPG Favourites Channels')
            self.assertTrue(self.page.checkIfEpgIsAvalaible())
            time.sleep(2)
            EPGLIST = self.page.findInPage('3. ') 
            if not (EPGLIST==True):
                self.assertTrue(False, "  >>  ERR channel 3 isn't in EPG(favorite) is heart")
            self.assertTrue(self.page.getInfoFromEpgFocus().favorite, "'ERR channel 3 don't have heart in EPG(favorite)")
            
            self.logStepResults("STEP 7- check if channel 3 in EPG(favorite) have heart")
            
            ''' step '''
            self.logStepBeginning("STEP 8-check if  channel 3 in EPG have heart")     
            self.rc.sendKeys(["KEY_BACK"]) 
            time.sleep(1)       
            self.rc.sendKeys(["KEY_TV"])
            time.sleep(1)
            self.rc.sendKeys(["KEY_GREEN"]) 
            time.sleep(1) 
            self.assertTrue(self.page.actionSelect(Menu.epg), "ERROR IN GO TO EPG(GREEN_BUTTON)")
            self.assertTrue(self.page.actionSelect(Menu.epgWeek), 'ERRPR IN GO TO EPG favorite Channels')
            self.rc.sendKeys(["KEY_3"]) 
            time.sleep(1) 
            EPGLIST = self.page.findInPage('3. ') 
            if not (EPGLIST==True):
                self.assertTrue(False, "  >>  ERR channel 3 isn't in EPG(favorite)")
            self.assertTrue(self.page.getInfoFromEpgFocus().favorite, "'ERR channel 3 don't have heart in EPG(favorite)")
            self.rc.sendKeys(["KEY_BACK"]) 
            time.sleep(1)       
            self.rc.sendKeys(["KEY_TV"])
            time.sleep(1)
            self.logStepResults("STEP 8- check if  channel 3 in EPG have heart")
             
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