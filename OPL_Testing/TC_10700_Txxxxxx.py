# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from NewTvTesting.Containers import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_10700_Txxxxxx(TC_OPL_template):
    """Implementation of the HP QC test ID - 10700 - Txxxxxx My Videos Adult content - add adult vod in catalog to favorites; remove adult vod in catalog from favorites.
    
    @author: Leszek Wawrzonkowski
    """
    
    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        vodiInfo = None
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")
            
            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            
            ''' step '''
            self.logStepBeginning("STEP - go to VOD adults catalog")
            self.assertTrue(self.page.goToVodAdults())
            self.assertTrue(self.page.actionSelect(Menu.vodAdultCatalogWithTestContent))
            self.logStepResults("STEP - go to VOD adults catalog")
            
            ''' step '''
            self.logStepBeginning("STEP - add VOD to favorites")
            if(not self.page.goToVodToAddToFavoritesInCatalog()):
                self.assertTrue(False, InfoMessages.ContentNotFound)
            time.sleep(2)
            vodiInfo = self.page.getInfoFromVodPage()
            self.assertTrue(type(vodiInfo) is VodItem, "  >>   ERR: wrong record data")
            self.assertTrue(self.page.actionSelect(Menu.vodAddToFavorites))
            self.logStepResults("STEP - add VOD to favorites")
            
            ''' step '''
            self.logStepBeginning("STEP - verify adults favorites list")
            self.assertTrue(self.page.goToVodFavorites(inAdults = True))
            self.assertTrue(self.page.findInList(vodiInfo.title, onlyActive = True))
            self.logStepResults("STEP - verify adults favorites list")
            
            ''' step '''
            self.logStepBeginning("STEP - go to VOD adults catalog")
            self.assertTrue(self.page.goToVodAdults())
            self.assertTrue(self.page.actionSelect(Menu.vodAdultCatalogWithTestContent))
            self.logStepResults("STEP - go to VOD adults catalog")
            
            ''' step '''
            self.logStepBeginning("STEP - remove VOD from favorites")
            self.assertTrue(self.page.actionSelect(vodiInfo.title))
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.vodRemoveFromFavorites))
            self.logStepResults("STEP - remove VOD from favorites")
            
            ''' step '''
            self.logStepBeginning("STEP - verify adults favorites list")
            self.assertTrue(self.page.goToVodFavorites(inAdults = True))
            self.assertFalse(self.page.findInList(vodiInfo.title, onlyActive = True))
            self.logStepResults("STEP - verify adults favorites list")
            
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")
            
        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise

        finally:
            if not self.test_passed and type(vodiInfo) is VodItem:
                self.logger.info("----------- cleaning -----------")
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                # clean logic
                try:            
                    self.assertTrue(self.page.goToVodAdults())
                    self.assertTrue(self.page.actionSelect(Menu.vodAdultCatalogWithTestContent))
                    self.assertTrue(self.page.actionSelect(vodiInfo.title))
                    time.sleep(2)
                    self.assertTrue(self.page.actionSelect(Menu.vodRemoveFromFavorites))
                except:
                    pass
