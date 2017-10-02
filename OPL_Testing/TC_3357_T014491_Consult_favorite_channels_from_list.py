# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.DataSet import LiveData
from _ast import Return
from datetime import datetime, timedelta
from NewTvTesting.StbtIntegration import *
from NewTvTesting.Containers import FavoriteChannelListItem

 

 

class TC_3357_T014491_Consult_favorite_channels_from_list(TC_OPL_template):

    """Implementation of the HP QC test ID 3357 T014491_Consult_favorite_channels_from_list
 
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
            self.logStepBeginning("STEP 2 - Go to LIVE ")     
            self.rc.sendKeys(["KEY_BACK"]) 
            time.sleep(1)
            self.rc.sendKeys(["KEY_BACK"]) 
            time.sleep(1)              
            self.rc.sendKeys(["KEY_TV"])
            time.sleep(1)
            self.logStepResults("STEP 2 - Go To LIVE ")
              
             
            ''' step '''
            self.logStepBeginning("STEP 3 - add Favorite channels (1,2,3)")   
            self.rc.sendKeys(["KEY_1"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.actionSelect(Menu.toolboxFavouriteChannelsNo),'Go to toolbox in channel 1')
            self.assertTrue(self.page.actionSelect(Menu.toolbox_2_favouriteChannelYes), 'Add channel 1 to favorite channels')
            time.sleep(3)
            self.rc.sendKeys(["KEY_2"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.actionSelect(Menu.toolboxFavouriteChannelsNo), 'Go to toolbox in channel 1')
            self.assertTrue(self.page.actionSelect(Menu.toolbox_2_favouriteChannelYes), 'Add channel 1 to favorite channels')
            time.sleep(3)
            self.rc.sendKeys(["KEY_3"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            self.assertTrue(self.page.actionSelect(Menu.toolboxFavouriteChannelsNo), 'Go to toolbox in channel 1')
            self.assertTrue(self.page.actionSelect(Menu.toolbox_2_favouriteChannelYes), 'Add channel 1 to favorite channels')
            time.sleep(3)
            self.logStepResults("STEP 3 - add Favorite channels (1,2,3)")
    
    
            ''' step '''
            self.logStepBeginning("STEP 4 - Go in toolbox to my favorites channels") 
            time.sleep(2)
            self.rc.sendKeys(["KEY_1"]) 
            time.sleep(2)
            self.rc.sendKeys(["KEY_LIST"])
            time.sleep(2)
             
            status = self.page.findInPage(Description.favoriteInList)
            i=1
            if (status==False):
                while (i<9):
                    i=i+1
                    self.rc.sendKeys(["KEY_LEFT"])
                    time.sleep(4)
                    status = self.page.findInPage(Description.favoriteInList)
                    time.sleep(1)
                    if (status==True):
                        i=9
            self.logStepResults("STEP 4 - Go in toolbox to my favorites channels ")
            
            
            
            ''' step '''
            self.logStepBeginning("STEP 5 - Checking number of channel in toolbox - favorite channel")            
            time.sleep(5)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(2)
            favoriteHightligt = self.page.driver.find_element_by_css_selector(".menuList .list .container .listItem.highlight").text.encode('utf-8').split(u'. ')
            favoriteHightligt = favoriteHightligt[0]
            if not favoriteHightligt=="1":
                self.assertTrue(False, "  >>  Doesn`t match the channel number ")
                
            time.sleep(5)
            self.rc.sendKeys(["KEY_DOWN"])
            self.page.driver.get(Rpi.DUMP)
            time.sleep(2)
            favoriteHightligt = self.page.driver.find_element_by_css_selector(".menuList .list .container .listItem.highlight").text.encode('utf-8').split(u'. ')
            favoriteHightligt = favoriteHightligt[0]
            if not favoriteHightligt=="2":
                self.assertTrue(False, "  >>  Doesn`t match the channel number ")
            
            time.sleep(5)
            self.rc.sendKeys(["KEY_DOWN"])
            self.page.driver.get(Rpi.DUMP)
            time.sleep(2)
            favoriteHightligt = self.page.driver.find_element_by_css_selector(".menuList .list .container .listItem.highlight").text.encode('utf-8').split(u'. ')
            favoriteHightligt = favoriteHightligt[0]
            if not favoriteHightligt=="3":
                self.assertTrue(False, "  >>  Doesn`t match the channel number ")
            
            time.sleep(5)
            self.rc.sendKeys(["KEY_DOWN"])
            self.page.driver.get(Rpi.DUMP)
            time.sleep(2)
            favoriteHightligt = self.page.driver.find_element_by_css_selector(".menuList .list .container .listItem.highlight").text.encode('utf-8').split(u'. ')
            favoriteHightligt = favoriteHightligt[0]
            if not favoriteHightligt=="1":
                self.assertTrue(False, "  >>  Doesn`t match the channel number ")
       
            self.logStepResults("STEP 5 - Checking number of channel in toolbox - favorite channel")
        
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
