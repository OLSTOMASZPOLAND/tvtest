# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time

class TC_3395_T015182_consult_customized_recommendations_opt_in(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3395 - T015182_consult_customized_recommendations_opt_in
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")

            if not self.page.cleanCodeParentalToDefault():
                self.page.cleanCodeParentalToDefault()

            if not self.page.setParentalControl(ParentalControl.SetDeactive):
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                self.page.setParentalControl(ParentalControl.SetDeactive)

            ''' step '''
            self.logStepBeginning("turn on recommendations")

            self.assertTrue(self.page.goToMySettings(), "   ERR   cannot go to my settings")
            self.assertTrue(self.page.actionSelect(Menu.personalizedSuggestion), "   ERR   cannot select " + Menu.personalizedSuggestion)

            time.sleep(3)

            if self.page.findInList(Menu.activate, True):
                self.assertTrue(self.page.actionSelect(Menu.activate), "   ERR   cannot select " + Menu.activate)
                time.sleep(5)
                self.rc.sendKeys(["KEY_OK"])
                time.sleep(5)
                self.rc.sendKeys(["KEY_OK"])
                time.sleep(1)
                self.assertTrue(self.page.actionSelect(Menu.personalizedSuggestion), "   ERR   cannot select " + Menu.personalizedSuggestion)

            self.assertTrue(self.page.actionSelect(Menu.myViewershipRecommendation), "   ERR   cannot select " + Menu.myViewershipRecommendation)
            time.sleep(10)
            self.rc.sendKeys(["KEY_LEFT"])
            time.sleep(10)

            self.logStepResults("turn on recommendations")

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV", ])

            self.logStepBeginning("populate recommendations")

            self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR    cannot go to vod catalog")
            self.assertTrue(self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa1, ParentalControl.CssClassCsa2, ParentalControl.CssClassCsa3, ParentalControl.CssClassCsa4]), "   ERR   cannot find video to rent")
            vod = self.page.getInfoFromVodPage()

            if not vod:
                self.fail("   ERR   cannot get info from VPS")

            self.assertTrue(self.page.rentVodThenPlay(), "   ERR   cannot rent vod")

            time.sleep(vod.getLength().seconds / 2)

            self.assertTrue(self.page.checkLive(True), "   ERR   error in check live function")

            time.sleep(vod.getLength().seconds / 2 + 120)

            self.logStepResults("populate recommendations")

            self.logStepBeginning("check 'najczesciej ogladane'")

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV", ])
            self.assertTrue(self.page.goToMySettings(), "   ERR   cannot go to my settings")
            self.assertTrue(self.page.actionSelect(Menu.personalizedSuggestion), "   ERR   cannot select " + Menu.personalizedSuggestion)
            self.assertTrue(self.page.actionSelect(Menu.myViewershipRecommendation), "   ERR   cannot select " + Menu.myViewershipRecommendation)

            self.assertTrue(self.page.findInPage(vod.getTitle()), "   ERR   cannot find " + vod.getTitle())

            self.logStepResults("check 'najczesciej ogladane'")

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("error occurred - %s" % e)
            self.logger.info("error occurred - %s - cleaning" % e)
            raise

        finally:
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV", ])
            self.page.goToMySettings()
            self.page.actionSelect(Menu.personalizedSuggestion)
            self.page.actionSelect(Menu.deactivate)
            time.sleep(4)
            self.rc.sendKeys(["KEY_OK"])
