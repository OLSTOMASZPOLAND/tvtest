# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import Menu
import time

class TC_18687_TC_18689_TC_18688_RFC_2909d_remove_vod_package_from_moje_wybrane_add_package_to_moje_wybrane(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18687 - 18688 - 18689 - remove_vod_package_from_moje_wybrane & add_package_to_moje_wybrane
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("add and remove package from favorites")

        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogHorror), "   ERR   cannot go to " + Menu.vodCatalogHorror)
        self.assertTrue(self.page.actionSelect(Menu.vodPackage), "   ERR   cannot select " + Menu.vodPackage)

        if self.page.findInList(Menu.vodAddToFavorites, True):
            self.assertTrue(self.page.actionSelect(Menu.vodAddToFavorites), "   ERR   cannot select " + Menu.vodAddToFavorites)
            self.assertTrue(self.page.findInList(Menu.vodRemoveFromFavorites, True), "   ERR   cannot find " + Menu.vodRemoveFromFavorites)

        elif self.page.findInList(Menu.vodRemoveFromFavorites, True):
            self.assertTrue(self.page.actionSelect(Menu.vodRemoveFromFavorites), "   ERR   cannot select " + Menu.vodRemoveFromFavorites)
            self.assertTrue(self.page.findInList(Menu.vodAddToFavorites, True), "   ERR   cannot find " + Menu.vodAddToFavorites)
        else:
            self.fail("   ERR   cannot find " + Menu.vodRemoveFromFavorites + " or " + Menu.vodAddToFavorites)

        if self.page.findInList(Menu.vodAddToFavorites, True):
            self.page.actionSelect(Menu.vodAddToFavorites)

        self.rc.sendKeys(["KEY_TV", "KEY_MENU"])

        time.sleep(2)

        self.assertTrue(self.page.actionSelect(Menu.vodMyFavorites), "   ERR   cannot select " + Menu.vodMyFavorites)
        time.sleep(5)
        self.assertTrue(self.page.actionSelect(Menu.vodPackage), "   ERR   cannot select " + Menu.vodPackage)

        time.sleep(10)

        self.assertTrue(self.page.actionSelect(Menu.vodRemoveFromFavorites), "   ERR   cannot select " + Menu.vodRemoveFromFavorites)
        self.assertTrue(self.page.findInList(Menu.vodAddToFavorites, True), "   ERR   cannot find " + Menu.vodAddToFavorites)
        
        time.sleep(5)

        self.rc.sendKeys(["KEY_BACK"])

        time.sleep(10)

        self.assertFalse(self.page.findInList(Menu.vodPackage), "   ERR   Package is still in my favorites")

        self.logStepResults("add and remove package from favorites")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
