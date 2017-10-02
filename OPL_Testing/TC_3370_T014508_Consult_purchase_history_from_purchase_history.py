# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import *
from NewTvTesting.Utils import *


class TC_3370_T014508_Consult_purchase_history_from_purchase_history(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3370 - T014508_Consult purchase history
    
        Purpose: Consult purchase history from my account/my purchases/purchase history
                 The portal displays the list of all purchases made by the user with a detailed description of the selected item.
                 The user can navigate in the list using up/down remote buttons.
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        if not self.page.cleanCodeAdultToDefault():
            self.page.cleanCodeAdultToDefault()
        if not self.page.cleanCodeParentalToDefault():
            self.page.cleanCodeParentalToDefault()
        if not self.page.setParentalControl(ParentalControl.SetDeactive):
            self.page.setParentalControl(ParentalControl.SetDeactive)

        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("PRESTEP - check for number of already bought content")

        self.assertTrue(self.page.goToMenu(), "   ERR >>> not in Menu")
        self.assertTrue(self.page.actionSelect(Menu.myAccount), "   ERR >>> not in my account")
        self.assertTrue(self.page.actionSelect(Menu.myPurchases), "   ERR >>> not in Menu")
        self.assertTrue(self.page.actionSelect(Menu.purchaseHistory), "   ERR >>> not in purchases history")

        self.rc.sendKeys(["KEY_BACK"])

        time.sleep(10)

        self.page.driver.get(Rpi.DUMP)
        time.sleep(1)
        
        try:
            boughtItemsNumberRegular = int(self.page.driver.find_element_by_css_selector(".orange").text)
        except:
            self.fail("   ERR   cannot read current purchases number")

        self.logStepResults("PRESTEP - check for number of already bought content")

        '''step'''
        self.logStepBeginning("STEP - buy adult and regular VOD")

        self.page.goToVodAdults()

        self.assertTrue(self.page.actionSelect(Menu.vodAdultCatalogWithTestContent), "   ERR >>> not in adult content")

        if self.page.goToVodToRentInCatalog(count_vod_max_search = 10):
            if not self.page.rentVodThenPlayAndBackToVodScreen():
                self.rc.sendKeys(["KEY_BACK"])
                self.assertTrue(self.page.rentVodThenPlayAndBackToVodScreen(True), "   ERR:   can't buy adult video")
        else:
            self.fail("   ERR:   can't find adult video to rent")

        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR:   not in VOD catalog")

        if(self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa4, ParentalControl.CssClassCsa3, ParentalControl.CssClassCsa2])):
            if not self.page.rentVodThenPlayAndBackToVodScreen():
                    self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                    self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR:   not in VOD catalog")
                    self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa4, ParentalControl.CssClassCsa3, ParentalControl.CssClassCsa2])
                    self.assertTrue(self.page.rentVodThenPlayAndBackToVodScreen(), "   ERR:   can't buy regular video")
        else:
            self.fail("   ERR:   can't find regular video to rent")

        self.logStepResults("STEP - buy adult and regular VOD")


        '''step'''
        self.logStepBeginning("check if order history displays updated data")

        self.assertTrue(self.page.goToMenu(), "   ERR >>> not in Menu")
        self.assertTrue(self.page.actionSelect(Menu.myAccount), "   ERR >>> not in my account")
        self.assertTrue(self.page.actionSelect(Menu.myPurchases), "   ERR >>> not in Menu")
        self.assertTrue(self.page.actionSelect(Menu.purchaseHistory), "   ERR >>> not in purchases history")

        for x in range(boughtItemsNumberRegular):  # TODO: better check of every information, if date is really a date etc
            self.page.driver.refresh()
            self.assertTrue(len(self.page.driver.find_elements_by_xpath("//span[@class='value']")) >= 4, "   ERR >>> not enough purchase details")
            self.rc.sendKeys(["KEY_DOWN"])

        self.rc.sendKeys(["KEY_BACK"])

        time.sleep(10)

        self.page.driver.refresh()

        try:
            self.assertTrue(boughtItemsNumberRegular + 1 == int(self.page.driver.find_element_by_css_selector(".description.dockCenter .content .orange").text), "   ERR:   incorrect bought movies value, should be %i" % (boughtItemsNumberRegular + 1))
        except:
            self.fail("   ERR   cannot read current purchases number")

        self.logStepResults("check if order history displays updated data")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
