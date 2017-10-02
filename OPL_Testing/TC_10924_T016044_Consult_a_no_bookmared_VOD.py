# -*- coding: utf-8 -*-

import time

from NewTvTesting.Containers import *
from NewTvTesting.DataSet import *
from NewTvTesting.StbtIntegration import *
from OPL_Testing.TC_OPL_template import TC_OPL_template

from datetime import datetime, timedelta





class TC_10924_T016044_Consult_a_no_bookmared_VOD(TC_OPL_template):

    """             

    @author: Marek Szlachetka
    """



    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)



    def test(self):

        self.logger.info("----- " + self.__class__.__name__ + " START -----")


        ''' step 1 '''
        
        self.logStepBeginning("STEP 1 - Going to video presentation on VOD")
        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "ERR: Entering VOD Catalog" +Menu.vodCatalogWithTestContent)

        time.sleep(2)
        self.rc.sendKeys(["KEY_OK"])
        self.logStepResults("STEP 1 - Going to video presentation on VOD")


        ''' step 2 '''
        self.logStepBeginning("STEP 2 - Add to/Remove from favorites")
        time.sleep(4)
        status = self.page.findInPage(Menu.vodAddToFavorites)
        if status==False:
            self.assertTrue(self.page.actionSelect(Menu.vodRemoveFromFavorites), 'ERR: Don`t remove VOD to favorites')
            self.rc.sendKeys(["KEY_OK"])
        else:
            self.assertTrue(self.page.actionSelect(Menu.vodAddToFavorites), 'ERR: Don`t added VOD to favorites ')
            
        status = self.page.findInPage(Menu.vodRemoveFromFavorites)
        if status!=True:
            self.assertTrue(False, "  >>  Don`t finding  a video to remove... ")
        time.sleep(2)
        self.rc.sendKeys(["KEY_OK"])
        time.sleep(2)
        status = self.page.findInPage(Menu.vodAddToFavorites)
        if status!=True:
            self.assertTrue(False, "  >>  Don`t finding a video to add ")
            
        self.logStepResults("STEP 2 - Add to/Remove from favorites")


        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")