# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_18561_T014529_Access_the_My_Video_list_when_the_package_is_rented(TC_OPL_template):
    '''
    Coverage: HP QC test ID - 18561 - T014529_Access the My Video list when the package is rented
    
    @author: Kamil Kulinski
    
    '''
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")
        
        try:
            
            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            self.page.setParentalControl(ParentalControl.SetDeactive)
     
            ''' A_1 - Prerequisites '''
            self.logStepBeginning("A_1 - Prerequisites - rent at least one package")
            
            self.rc.sendKeys(["KEY_VIDEO"])
            time.sleep(20)
            self.assertTrue(self.page.actionSelect(Menu.vodCatalog), "ERR: Entering VOD Catalog")
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(u'horror'.encode('utf-8')), "ERR: Entering VOD Catalog with test content")
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(u'Oscar'.encode('utf-8')), "ERR: Entering Package presentation screen")
            time.sleep(10)
            
            zamow=self.page.findInPage(u'zamów paczkę'.encode('utf-8'))
            if (zamow==True):
                self.assertTrue(self.page.actionSelect(u'zamów paczkę'.encode('utf-8')), "ERR: Renting package")
                time.sleep(3)            
                
                kontrola=self.page.findInPage(u'kontrola rodzicielska'.encode('utf-8'))
                if (kontrola==True):
                    self.rc.sendNumberSequence(Env.PARENTAL_CODE)
                    self.rc.sendKeys(["KEY_OK"])
                    
                #NPK            
                if self.page.findInDialogBox(Menu.vodNPK):
                    self.rc.sendKeys(["KEY_OK"])
                    time.sleep(2)
                    self.rc.sendKeys(["KEY_DOWN"])
                    time.sleep(2)          
                    self.rc.sendKeys(["KEY_OK"])
                    if self.page.findInDialogBox(Menu.vodNPKInfo):          
                        self.rc.sendKeys(["KEY_OK"])
                        time.sleep(2)
                    else:
                        self.fail("  >>   ERR: problem finding >" + Menu.vodNPKInfo + "<")
            
            self.rc.sendKeys(["KEY_VIDEO"])
            time.sleep(20)
            self.assertTrue(self.page.actionSelect(Menu.vodCatalog), "ERR: Entering VOD Catalog")
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(Menu.vodPolishMovies), "ERR: Entering VOD Catalog with test content")
            time.sleep(10)
            self.assertTrue(self.page.actionSelect(Menu.film), "ERR: Entering VOD VPS") 
            time.sleep(10)
            self.assertTrue(self.page.rentAndPlayOrPlayRentedVod(), "ERR: Renting VOD")
            time.sleep(10)
            
            self.rc.sendKeys(["KEY_STOP"])
            self.rc.sendKeys(["KEY_DOWN"])
            self.rc.sendKeys(["KEY_OK"])
            
            self.logStepResults("A_1 - Prerequisites - rent at least one package")
            
            ''' B - initial state '''
            self.logStepBeginning("B - initial state - VOD menu is displayed")
            
            self.rc.sendKeys(["KEY_VIDEO"])
            time.sleep(2)
                    
            self.logStepResults("B - initial state - VOD menu is displayed")
            
            ''' Step 1 '''
            self.logStepBeginning("Step 1 - moje zamowienia")
            
            self.assertTrue(self.page.actionSelect(Menu.vodMyVideos))
            time.sleep(2)
            self.assertTrue(self.page.findInList(u'Oscar'.encode('utf-8')), "ERR: Checking if Package is present on My Videos list")
            self.assertTrue(self.page.findInList(Menu.film), "ERR: Checking if VOD is present on My Videos list") 
            time.sleep(2)
             
            self.logStepResults("Step 1 - moje zamowienia")
    
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")