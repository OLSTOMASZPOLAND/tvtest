# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time
from decimal import Decimal

class TC_3368_T014506_consult_prepaid_account(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3368 - _T014506_consult_prepaid_account
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")

            if not self.page.setParentalControl(ParentalControl.SetDeactive):
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                self.page.setParentalControl(ParentalControl.SetDeactive)

            ''' step '''
            self.logStepBeginning("check current prepaid account balance")
            self.assertTrue(self.page.goToMenu(), "   ERR   cannot go to menu")
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "   ERR   cannot go to my account")
            self.assertTrue(self.page.actionSelect(Menu.myPurchases), "   ERR   cannot go to my purchases")
            self.rc.sendKeys(["KEY_UP"])
            time.sleep(30)
            self.assertTrue(self.page.actionSelect(Menu.prepaidAccount), "   ERR   cannot go to prepaid account")
            time.sleep(3)
            try:
                self.page.driver.get(Rpi.DUMP)
                time.sleep(1)
                balance = self.page.driver.find_elements_by_css_selector(".content")[0].text.encode('utf-8')
                balance = Decimal(balance.split(': ')[1].split(' zł')[0].replace(",", "."))
            except Exception, e:
                self.logger.info("error occured: " + str(e))
                self.fail("   ERR   cannot read current account balance")

            self.assertTrue(self.page.actionSelect(Menu.prepaidRecharge4), "   ERR   cannot recharge prepaid account")
            time.sleep(10)

            self.rc.sendKeys(["KEY_OK"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_DOWN"])
            time.sleep(2)
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(1)
            if self.page.findInDialogBox(Menu.prepaidAccount):
                self.fail("  >>   ERR: cannot add prepaid resources, prepaid limit might be reached")
            if self.page.findInDialogBox(Menu.vodNPKInfo):
                pass
            else:
                self.fail("  >>   ERR: problem finding >" + Menu.vodNPKInfo + "<")

            time.sleep(15)
            
            try:
                self.page.driver.get(Rpi.DUMP)
                time.sleep(1)
                balance2 = self.page.driver.find_elements_by_css_selector(".content")[0].text.encode('utf-8')
                balance2 = Decimal(balance2.split(': ')[1].split(' zł')[0].replace(",", "."))
            except Exception, e:
                self.logger.info("error occured: " + str(e))
                self.fail("   ERR   cannot read current account balance after recharge")
            self.assertTrue(balance + Decimal('23.99') == balance2, "   ERR   balance after recharge is not correct")

            self.logStepResults("check current prepaid account balance")

            self.logStepBeginning("buy vod and check if prepaid account balance displays correctly")

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

            time.sleep(3)

            self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot go to vod catalog")
            if not self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa1, ParentalControl.CssClassCsa2, ParentalControl.CssClassCsa3, ParentalControl.CssClassCsa4]):
                self.fail("   ERR   cannot find vod to rent")
            price = self.page.getInfoFromVodPage()
            if not price:
                self.fail("   ERR   cannot get vod info")
            price = Decimal(price.getPrice())
            if not price:
                self.fail("   ERR   cannot get vod price")
            self.assertTrue(self.page.rentVodThenPlay(goBackToVodScreen=True), "   ERR:  cannot rent vod")

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

            self.assertTrue(self.page.goToMenu(), "   ERR   cannot go to menu")
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "   ERR   cannot go to my account")
            self.assertTrue(self.page.actionSelect(Menu.myPurchases), "   ERR   cannot go to my purchases")
            self.rc.sendKeys(["KEY_UP"])
            time.sleep(30)
            self.assertTrue(self.page.actionSelect(Menu.prepaidAccount), "   ERR   cannot go to prepaid account")

            try:
                self.page.driver.get(Rpi.DUMP)
                time.sleep(1)
                balance3 = self.page.driver.find_elements_by_css_selector(".content")[0].text.encode('utf-8')
                balance3 = Decimal(balance3.split(': ')[1].split(' zł')[0].replace(",", "."))
            except Exception, e:
                self.logger.info("error occured: " + str(e))
                self.fail("   ERR   cannot read current account balance")
            self.rc.sendKeys(["KEY_BACK"])
            self.assertTrue(balance2 - price == balance3, "   ERR   balance after recharge is not correct")

            self.logStepResults("buy vod and check if prepaid account balance displays correctly")


            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
