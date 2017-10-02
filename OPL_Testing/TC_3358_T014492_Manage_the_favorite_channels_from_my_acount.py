# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData

 

 

class TC_3358_T014492_Manage_the_favorite_channels_from_my_acount(TC_OPL_template):

    """
    Implementation of the HP QC test ID - 3358_T014492_Manage_the_favorite_channels_from_my_acount
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
            self.logStepBeginning("STEP 4 - Turn off channel 2 from favorite channels")
            self.rc.sendKeys(["KEY_MENU"])
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "ERROR IN GO TO MY ACCOUNT")
            self.assertTrue(self.page.actionSelect(Menu.mySettings), "ERROR IN GO TO MY Settings")
            self.assertTrue(self.page.actionSelect(Menu.myChannels), "ERROR IN GO TO MY Channels")
            self.rc.sendKeys(["KEY_BACK"]) 
            time.sleep(10)
            if not (self.page.findInPage(': 3')):
                self.assertTrue(False, '  >>  ERR none 3 favorite channels"')
            self.logger.debug("  >>  found 3 favorite channels ->OK")
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_BACK"]) 
            time.sleep(2)       
            if not (self.page.findInPage(': 2')):
                self.assertTrue(False, '  >>  ERR none 3 favorite channels"')
            self.logger.debug("  >>  found 2 favorite channels ->OK")
            self.logStepResults("STEP 4 - Turn off channel 2 from favorite channels")  
                      
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