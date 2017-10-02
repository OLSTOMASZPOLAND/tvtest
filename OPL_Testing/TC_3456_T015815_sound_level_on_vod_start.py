# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import Menu, ParentalControl
import time

class TC_3456_T015815_sound_level_on_vod_start(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3456 sound_level_on_vod_start
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("check current sound level")

        self.rc.sendKeys(["KEY_MUTE"])
        time.sleep(0.5)
        self.rc.sendKeys(["KEY_MUTE"])
        vol = self.page.getVolumeLevel()

        if not vol or vol == -1:
            self.fail("   ERR    cannot get volume level")

        self.logStepResults("check current sound level")

        self.logStepBeginning("start vod and and check volume level")

        self.assertTrue(self.page.goToVodCatalog(Menu.vodCatalogWithTestContent), "   ERR   cannot go to vod catalog")
        self.assertTrue(self.page.goToVodToRentInCatalogByCsaCategory([ParentalControl.CssClassCsa1, ParentalControl.CssClassCsa2, \
                                                                       ParentalControl.CssClassCsa3, ParentalControl.CssClassCsa4]), \
                                                                       "   ERR   cannot find vod to rent")
        self.assertTrue(self.page.rentVodThenPlay(), "   ERR   cannot rent vod")
        self.rc.sendKeys(["KEY_MUTE"])
        time.sleep(0.5)
        self.rc.sendKeys(["KEY_MUTE"])
        vol2 = self.page.getVolumeLevel()
        
        self.assertTrue(vol == vol2, "   ERR   volume from live channel and vod differs")

        self.logStepResults("start vod and and check volume level")


        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")
