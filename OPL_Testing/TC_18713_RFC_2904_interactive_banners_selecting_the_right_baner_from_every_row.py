# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.Config import *

class TC_18713_RFC_2904_interactive_banners_selecting_the_right_baner_from_every_row(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18713 - RFC_2904_interactive_banners_selecting_the_right_baner_from_every_row
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        valueDTH = 128
        valueIPTV = 461
        valueRFOG = 146
        value = None
        if Env.ZONE == 'DTH':
            value = valueDTH
        elif Env.ZONE == 'IPTV' or Env.ZONE == 'FTTH':
            value = valueIPTV
        elif Env.ZONE == 'RFTV':
            value = valueRFOG
        else:
            self.fail("   ERR   environment not recognized, aborting")

        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")

            ''' step '''
            self.logStepBeginning("step 1")

            self.rc.zap(0)

            time.sleep(2)

            self.rc.sendKeys(["KEY_RIGHT"] * 4)
            if Env.ZONE == 'RFTV':
                self.rc.sendKeys(["KEY_RIGHT"])

            time.sleep(4)

            self.rc.sendKeys(["KEY_DOWN"] * 6)

            time.sleep(10)

            self.rc.sendKeys(["KEY_LEFT"])

            item = self.page.getInfoFromMosaicFocus()
            
            self.assertIsNotNone(item, "   ERR   cannot get value from mosaic focus")

            self.assertTrue(item.getLcn() == value, "   ERR   wrong channel highlighted")

            self.rc.sendKeys(["KEY_RIGHT"])

            time.sleep(2)

            self.rc.sendKeys(["KEY_OK"])

            time.sleep(10)

            self.assertTrue(self.page.getInfoFromVodPage(), "   ERR   not in VPS")

            self.logStepResults("step 1")

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise

        finally:
            if not self.test_passed:
                self.logger.info("----------- cleaning -----------")
                self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
