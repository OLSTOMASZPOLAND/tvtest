# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3372_Manual_T014518_Reload_prepaid_account_payment_control_not_actived_accept(TC_OPL_template):
    '''
    Coverage: HP QC test ID - TC_3372_Manual_T014518_Reload_prepaid_account_payment_control_not_actived_accept
    
    Added to Config.py:
    prepaidAccount = u"konto prepaid".encode('utf-8')
    prepaidRecharge1 = u"50zł + bonus 10zł".encode('utf-8')
    prepaidRecharge2 = u"100zł".encode('utf-8')
    prepaidRecharge3 = u"25zł + bonus 5zł".encode('utf-8')
    prepaidRecharge4 = u"19,99zł + bonus 4zł".encode('utf-8')
    
    @author: Tomasz Stasiuk
    
    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        try:
            
            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            
            ''' Initial State '''
            self.logStepBeginning("Initial State - User is in menu My Codes")
            
            self.page.setParentalControl(ParentalControl.SetDeactive)
            time.sleep(11)
            self.rc.sendKeys(["KEY_MENU"])
            time.sleep(15)
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "ERR: Entering My Account")
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(Menu.myPurchases), "ERR: Entering My Purchases")
            time.sleep(10)
            
            self.logStepResults("Initial State - User is in menu My Codes")
     
            ''' Step 3 '''
            self.logStepBeginning("STEP 3 - Select konto prepaid and validate")
             
            self.assertTrue(self.page.actionSelect(Menu.prepaidAccount), "ERR: Entering Prepaid Account")
            time.sleep(2)
            
            self.logStepResults("STEP 3 - Select konto prepaid and validate")
            
            
            ''' Step 4 '''
            self.logStepBeginning("STEP 4 - For each choice of reloading account check that")
            
            self.assertTrue(self.page.findInList(Menu.prepaidRecharge1))
            self.assertTrue(self.page.findInList(Menu.prepaidRecharge2))
            self.assertTrue(self.page.findInList(Menu.prepaidRecharge3))
            self.assertTrue(self.page.findInList(Menu.prepaidRecharge4))
            
            self.logStepResults("STEP 4 - For each choice of reloading account check that")
            
            ''' Step 5 '''
            self.logStepBeginning("STEP 5 - Choose amount to be credited and validate - 20zl")
            
            self.assertTrue(self.page.actionSelect(Menu.prepaidRecharge4), "ERR: Choosing Reload Account with 20zl")
                        
            self.assertTrue(self.page.findInDialogBox(Menu.prepaidRecharge4))
            
            self.rc.sendKeys(["KEY_BACK"])
            
            self.assertTrue(self.page.actionSelect(Menu.prepaidRecharge4), "ERR: Choosing Reload Account with 20zl")
            self.assertTrue(self.page.findInDialogBox(Menu.prepaidRecharge4))
            
            #NPK           
            
            if self.page.findInDialogBox(Menu.vodNPKlower):
                self.rc.sendKeys(["KEY_OK"])
                time.sleep(2)
                self.rc.sendKeys(["KEY_DOWN"])
                time.sleep(2)          
                self.rc.sendKeys(["KEY_OK"])
                if self.page.findInDialogBox(Menu.prepaidAccount):
                    self.fail("  >>   ERR: cannot add prepaid resources, prepaid limit might be reached")
                if self.page.findInDialogBox(Menu.vodNPKInfo):          
                #    self.rc.sendKeys(["KEY_OK"])
                    time.sleep(2)
                else:
                    self.fail("  >>   ERR: problem finding >" + Menu.vodNPKInfo + "<")

            
            self.logStepResults("STEP 5 - Choose amount to be credited and validate - 20zl")
                            
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")