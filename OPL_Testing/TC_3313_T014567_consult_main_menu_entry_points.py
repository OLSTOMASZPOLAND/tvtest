# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.Config import *

class TC_3313_T014567_consult_main_menu_entry_points(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3313 - T014567_consult_main_menu_entry_points
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("go to menu and check every item")

        self.rc.sendKeys(["KEY_MENU"])

        self.assertTrue(self.page.actionSelect(Menu.tvChannels), "   ERR   cannot select " + Menu.tvChannels)
        time.sleep(2)
        item = self.page.getInfoFromMosaicFocus()
        if not item:
            self.fail("   ERR   not in mosaic page")

        self.rc.sendKeys(["KEY_MENU"])
        self.assertTrue(self.page.actionSelect(Menu.videoOnDemand), "   ERR   cannot select " + Menu.videoOnDemand)
        time.sleep(2)
        if not self.page.findInCssSelectorElement(Menu.videoOnDemand, ".breadcrumb .first"):
            self.fail("   ERR   not in the VoD menu")

        self.rc.sendKeys(["KEY_MENU"])
        self.assertTrue(self.page.actionSelect(Menu.personalizedSuggestion), "   ERR   cannot select " + Menu.personalizedSuggestion)
        time.sleep(5)

        if not (self.page.findInCssSelectorElement(Menu.personalizedSuggestion, ".breadcrumb .first") or self.page.findInDialogBox(Menu.personalizedSuggestion)):
            self.fail("   ERR   not in the presonalized menu")

        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV", "KEY_MENU"])

        self.assertTrue(self.page.actionSelect(Menu.epg), "   ERR   cannot select " + Menu.epg)
        time.sleep(2)

        if not self.page.findInCssSelectorElement(Menu.epg, ".breadcrumb .first"):
            self.fail("   ERR   not in the epg menu")

        self.rc.sendKeys(["KEY_MENU"])
        self.assertTrue(self.page.actionSelect(Menu.myAccount), "   ERR   cannot select " + Menu.myAccount)
        time.sleep(2)

        if not self.page.findInCssSelectorElement(Menu.myAccount, ".breadcrumb .first"):
            self.fail("   ERR   not in the my account menu")

        self.rc.sendKeys(["KEY_MENU"])
        self.assertTrue(self.page.actionSelect(Menu.vodSearch), "   ERR   cannot select " + Menu.vodSearch)
        time.sleep(2)

        if not self.page.findInCssSelectorElement(Menu.vodSearch, ".breadcrumb .first"):
            self.fail("   ERR   not in the search menu")

        self.rc.sendKeys(["KEY_MENU"])
        self.assertTrue(self.page.actionSelect(Menu.pvr), "   ERR   cannot select " + Menu.pvr)
        time.sleep(2)

        if not self.page.findInCssSelectorElement(Menu.pvr, ".breadcrumb .first"):
            self.fail("   ERR   not in the pvr menu")

        self.rc.sendKeys(["KEY_MENU"])
        if self.page.findInList(Menu.vodMyFavorites, True):
            self.page.actionSelect(Menu.vodMyFavorites)
            if not self.page.findInCssSelectorElement(Menu.vodMyFavorites, ".breadcrumb .last"):
                self.fail("   ERR   not in the vod my favorites menu")
        else:
            self.page.goToVodCatalog(Menu.vodCatalogWithTestContent)
            self.page.goToVodToAddToFavoritesInCatalog()
            if self.page.actionSelect(Menu.vodAddToFavorites):
                self.rc.sendKeys(["KEY_MENU"])
                self.page.actionSelect(Menu.vodMyFavorites)
                if not self.page.findInCssSelectorElement(Menu.vodMyFavorites, ".breadcrumb .last"):
                    self.fail("   ERR   not in the vod my favorites menu")

        self.rc.sendKeys(["KEY_MENU"])
        self.assertTrue(self.page.actionSelect(Menu.multimedia), "   ERR   cannot select " + Menu.multimedia)

        if not self.page.findInCssSelectorElement(Menu.multimedia, ".breadcrumb .first"):
            self.fail("   ERR   not in the multimedia menu")

        self.logStepResults("go to menu and check every item")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
