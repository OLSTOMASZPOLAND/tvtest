# -*- coding: utf-8 -*-

 

import time

 

from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData
from _ast import Return


 

 

class TC_3004_T014447_Zapping_list_no_favorite_channel(TC_OPL_template):

    """Implementation of the HP QC test ID - 3004 - T014447_Zapping_list_no_favorite_channel
 
    @author: Tomasz Stasiuk
    """


       

    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)

   

    def test(self):
        
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

       

        ''' prestep '''

        self.logStepResults("AT_THE_BEGINNING")
        time.sleep(3)
             
        ''' step '''
        self.logStepBeginning("STEP 1- Turn off all favorite channels")
        self.page.cleanTurnOffAllFavoriteChannels()
        self.logStepResults("STEP 1- Turn off all favorite channels")
        
        ''' step '''
        self.logStepBeginning('STEP 2 -check if in favorite channel list is message "no favorite channels"')
        self.rc.sendKeys(["KEY_3"])
        time.sleep(4)    
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
        time.sleep(5)
        listchannels3 = self.page.findInPage(Menu.noFavoriteChannelsInChannelsList)
        if not (listchannels3==True):
            self.assertTrue(False, '  >>  ERR other message then "no favorite channels"')
        else:
            self.logger.info('  >> message "no favorite channels"')  
        self.rc.sendKeys(["KEY_BACK"])
        self.logStepResults('STEP 2 - check if in favorite channel list is message "no favorite channels"')
        
         
        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
        
        