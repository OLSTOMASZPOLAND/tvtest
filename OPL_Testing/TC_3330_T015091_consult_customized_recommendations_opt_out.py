# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time

class TC_3330_T015091_consult_customized_recommendations_opt_out(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3330 - consult_customized_recommendations_opt_out
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")

            ''' step '''
            self.logStepBeginning("turn off recommendations")

            self.assertTrue(self.page.goToMySettings(), "   ERR   cannot go to my settings")
            self.assertTrue(self.page.actionSelect(Menu.personalizedSuggestion), "   ERR   cannot select " + Menu.personalizedSuggestion)
            if self.page.findInList(Menu.deactivate, True):
                self.assertTrue(self.page.actionSelect(Menu.deactivate), "   ERR   cannot select " + Menu.deactivate)

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV", ])

            self.logStepResults("turn off recommendations")

            self.logStepBeginning("go to recommendations in main menu")

            self.assertTrue(self.page.goToMenu(), "   ERR   cannot go to menu")
            self.assertTrue(self.page.actionSelect(Menu.personalizedSuggestion), "   ERR   cannot select " + Menu.personalizedSuggestion)
            time.sleep(2)
            self.assertTrue(self.page.findInList(Menu.legalInformation, True), "   ERR   cannot find " + Menu.legalInformation)
            self.assertTrue(self.page.findInList(Menu.activate, True), "   ERR   cannot find " + Menu.activate)
            self.assertTrue(self.page.findInList(Menu.myViewershipRecommendation, True), "   ERR   cannot find " + Menu.myViewershipRecommendation)

            self.rc.sendKeys(["KEY_BACK"])

            time.sleep(3)

            self.assertTrue(self.page.findInCssSelectorElement("menu", ".breadcrumb .first") \
                                or self.page.findInCssSelectorElement(Menu.mySettings, ".breadcrumb .last"), "   ERR   not in main menu or my settings page")

            items = self.page.getList()

            for i in items:
                if i.selected:
                    self.assertTrue(i.text == Menu.personalizedSuggestion, "   ERR   %s is not highlighted" % Menu.personalizedSuggestion)
                    self.test_passed = True

            if self.test_passed:
                    self.logStepResults("go to recommendations in main menu")
                    self.logger.info("----- " + self.__class__.__name__ + " END -----")
            else:
                self.fail("   ERR   cannot find higlighted element")

        except Exception, e:
            self.logStepResults("error occurred - %s" % e)
            self.logger.info("error occurred - %s - cleaning" % e)
            raise

        finally:
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV", ])
            self.page.goToMySettings()
            self.page.actionSelect(Menu.personalizedSuggestion)
            if self.page.findInList(Menu.deactivate, True):
                self.page.actionSelect(Menu.deactivate)
