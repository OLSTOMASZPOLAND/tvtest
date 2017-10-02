# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import datetime
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
from NewTvTesting.Utils import *

class TC_3324_T015085_Check_if_user_can_get_personalized_recommendations_from_Main_Menu(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3324 - _T015085_Check if user can get personalized recommendations from Main Menu
    
    Purpose: the wake up screen is displayed with the last watched channel
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
        self.page.zapToChannel(self.rc.getChannelBBCHD)
        self.logStepResults("prerequisites")
        
        self.rc.sendKeys(["KEY_POWER"])
        time.sleep(30)

        ''' step '''
        self.logStepBeginning("STEP 3 - power on STB and wait for wake up screen")
        self.rc.sendKeys(["KEY_POWER"])

        time.sleep(3)

        currTime = datetime.datetime.now()

        while not self.page.findInCssSelectorElement("Orange TV", ".breadCrumb .path .first"):
            time.sleep(2)
            self.assertTrue((datetime.datetime.now() - currTime).seconds < 300, "   ERR   cannot find wake up screen with Orange TV welcome screen")

        self.logStepResults("STEP 3 - power on STB and wait for wake up screen")

        ''' step '''
        self.logStepBeginning("STEP 4,5,6 - focus and enter vod recommendation")

        self.rc.sendKeys(["KEY_DOWN", "KEY_RIGHT", "KEY_OK"])

        time.sleep(15)

        self.assertTrue(self.page.getInfoFromVodPage() is not None, "   ERR   cannot get VPS info")

        self.logStepResults("STEP 4,5,6 - focus and enter vod recommendation")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
