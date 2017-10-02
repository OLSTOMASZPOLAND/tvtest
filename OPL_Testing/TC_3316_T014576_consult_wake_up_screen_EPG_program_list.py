# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import datetime
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
from NewTvTesting.Utils import *

class TC_3316_T014576_consult_wake_up_screen_EPG_program_list(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3316 - _T014576_Consult Wake-up screen - EPG todays list
    
    Purpose: the wake up screen is displayed with EPG todays list
    @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("prerequisites")
        
        self.rc.sendKeys(["KEY_MENU"])
        self.page.actionSelect(Menu.myAccount)
        self.page.actionSelect(Menu.mySettings)
        self.page.actionSelect(Menu.myChannels)
        time.sleep(1)
        self.rc.sendKeys(["KEY_BACK"]) 
        time.sleep(5)
        if self.page.findInPage(Description.favoriteZeroChannels):
            self.rc.sendKeys(["KEY_OK"])
            self.page.turnOnFavouriteChannels(1)
            
        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        
        time.sleep(5)
        self.page.zapToChannel(self.rc.getChannelBBCHD)
        
        
        
        self.logStepResults("prerequisites")

        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(30)
        
        ''' step '''
        self.logStepBeginning("STEP 3 - power on STB and wait for wake up screen")
        
        self.rc.sendKeys(["KEY_POWER"])

        time.sleep(3)

        currTime = datetime.datetime.now()

        while not self.page.findInCssSelectorElement(Menu.epgTonight, ".wakeupEpg .titleText"):
            time.sleep(2)            
            self.assertTrue((datetime.datetime.now() - currTime).seconds < 300, "   ERR   cannot find wake up screen with watch today")

        self.logStepResults("STEP 3 - power on STB and wait for wake up screen")

        ''' step '''
        self.logStepBeginning("STEP 4,5,6 - move to EPG, press OK and check if EPG today displays")

        self.rc.sendKeys(["KEY_RIGHT"])
        time.sleep(2)
        self.rc.sendKeys(["KEY_OK"])

        time.sleep(3)

        self.assertTrue(self.page.findInCssSelectorElement(Menu.myChannels, ".first"), "   ERR    cannot find EPG today banner")

        self.logStepResults("STEP 4,5,6 - move to EPG, press OK and check if EPG today displays")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
