# -*- coding: utf-8 -*-


from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import time

class TC_3340_T014471_modify_confidential_code_wrong_current_code(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3340 - _TC_T014471_modify_confidential_code_wrong_current_code
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        try:
            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            if not self.page.setParentalControl(ParentalControl.SetActiveCsa2):
                if self.page.cleanCodeParentalToDefault():
                    if not self.page.setParentalControl(ParentalControl.SetActiveCsa2):
                        self.fail("   ERR   cannot set parental control")
        except:
            pass
            ''' step '''
        try:
            self.logStepBeginning("STEP 3,4,5,6,7 - go to my codes and set new parental code")
            
            self.assertTrue(self.page.goToMenu(), "   ERR   not in Menu")
            self.assertTrue(self.page.actionSelect(Menu.myAccount), "   ERR   not in my account")
            self.assertTrue(self.page.actionSelect(Menu.myCodes), "   ERR   not in my codes")
            self.assertTrue(self.page.actionSelect(Menu.parentalCode), "   ERR   cannot find parental codes")
            time.sleep(5)
            self.rc.sendNumberSequence("4567")
            time.sleep(5)

            self.assertTrue(self.page.findInDialogBox(DialogBox.WrongParentalCode), "   ERR   no error message about code error")

            self.rc.sendNumberSequence(Env.PARENTAL_CODE)

            time.sleep(1)
            
            self.rc.sendNumberSequence("4321")

            time.sleep(1)

            self.rc.sendNumberSequence("4321")

            time.sleep(1)

            self.rc.sendKeys(["KEY_OK"]) 
            time.sleep(3)
            self.assertTrue(self.page.findInDialogBox(DialogBox.NewParentalCodeConfirmation), "   ERR   no new code confirmation popup")
            
            time.sleep(5)

            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

            self.logStepResults("STEP 3,4,5,6,7 - go to my codes and set new parental code")

            self.logStepBeginning("STEP 8 - enter vod area and enter previous code")

            self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot go to vod catalog")
            if not self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa2, ParentalControl.CssClassCsa3, ParentalControl.CssClassCsa4]):
                self.fail("   ERR   cannot find vod to rent")
            self.assertFalse(self.page.rentVodThenPlay(True, True), "   ERR:   vod rented with previous confidential code")
            self.rc.sendKeys(["KEY_BACK"])

            self.logStepResults("STEP 8 - enter vod area and enter previous code")

            self.logStepBeginning("STEP 9 - enter vod area and enter new code")

            Env.PARENTAL_CODE = "4321"

            self.assertTrue(self.page.rentVodThenPlay(True, True), "   ERR:   cannot rent vod with new parental code")

            self.logStepResults("STEP 9 - enter vod area and enter new code")

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
        except Exception, e:
            self.logStepResults("error occurred - %s" % e)
            self.logger.info("error occurred - %s - cleaning" % e)
            raise
        finally:
            if not self.page.cleanCodeParentalToDefault():
                self.page.cleanCodeParentalToDefault()
            try:    
                if not self.page.setParentalControl(ParentalControl.SetDeactive):
                    self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                    self.page.setParentalControl(ParentalControl.SetDeactive)
            except:
                pass