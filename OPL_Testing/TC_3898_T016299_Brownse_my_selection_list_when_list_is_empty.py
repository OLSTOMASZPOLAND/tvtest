# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta





class TC_3898_T016299_Brownse_my_selection_list_when_list_is_empty(TC_OPL_template):

    """             

    @author: Marek Szlachetka
    """



    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)



    def test(self):

        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''

        self.logStepResults("AT_THE_BEGINNING")
        time.sleep(3)

        ''' step 1 '''
        self.logStepBeginning("STEP 1 - Go to VOD and select my favorite")     
        self.rc.sendKeys(["KEY_VIDEO"])
        time.sleep(8)
        self.assertTrue(self.page.actionSelect(Menu.vodMyFavorites), 'ERR: Do not entered to VOD my favorites')
        self.logStepResults("STEP 1 - Go to VOD and select my favorite")

        ''' step 2 '''
        self.logStepBeginning("STEP 2 - Check my favorite and if is VOD - remove ")   
        status = False  
        while (status == False):
            time.sleep(10)
            popup = self.page.actionSelect(Menu.vodMyFavorites)  
            if popup == True:
                status = True
            else:                
                self.rc.sendKeys(["KEY_OK"])
                time.sleep(3)
                self.assertTrue(self.page.actionSelect(Menu.vodRemoveFromFavorites), 'ERR: Problem with remove VOD from favorites')
                self.rc.sendKeys(["KEY_BACK"])
        self.logStepResults("STEP 2 - check my favorite and if is VOD - remove")

        ''' step 3 '''
        self.logStepBeginning("STEP 3 - Add to favorite VOD and check in my favorite")   
        time.sleep(2)
        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "ERR: Entering VOD Catalog")
        time.sleep(10)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(5)
        title1 = self.page.getInfoFromVodPage().title
        time.sleep(2)
        self.assertTrue(self.page.actionSelect(Menu.vodAddToFavorites),'ERR: Do not added VOD to favorites')
        time.sleep(4)
        self.rc.sendKeys(["KEY_VIDEO"])
        time.sleep(5)
        self.assertTrue(self.page.actionSelect(Menu.vodMyFavorites), 'ERR: Don`t entered to my favorites in VOD')
        time.sleep(3)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(2)
        title2 = self.page.getInfoFromVodPage().title
        if not (title1 == title2):
            self.assertTrue(False, "  >>   ERR: Wrong type mosaic program")
        self.logStepResults("STEP 3 - Add to favorite VOD and check in my favorite")


        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")