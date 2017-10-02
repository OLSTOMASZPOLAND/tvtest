# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
import time
from NewTvTesting.Config import Env

class TC_18684_RFC_2904_interactive_banners_fast_shifting_mosaic_pages(TC_OPL_template):
    '''Implementation of the HP QC test ID - 18684 - RFC_2904_interactive_banners_fast_shifting_mosaic_pages
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        channelsDTH = [8, 14, 114, 111, 233, 236, 277]
        channelsIPTV = [8, 14, 114, 111, 233, 236, 277]
        channelsRFOG = [8, 14, 114, 111, 233, 236, 277]
        channels = None
        if Env.ZONE == 'DTH':
            channels = channelsDTH
        elif Env.ZONE == 'IPTV' or Env.ZONE == 'FTTH':
            channels = channelsIPTV
        elif Env.ZONE == 'RFTV':
            channels = channelsRFOG
        else:
            self.fail("   ERR   environment not recognized, aborting")
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")

            ''' step '''
            self.logStepBeginning("step 1")
            self.rc.zap(1)
            time.sleep(5)
            self.rc.zap(0)
            time.sleep(5)
            self.rc.sendKeys(["KEY_DOWN", "KEY_DOWN", "KEY_RIGHT"])
            time.sleep(3)
            item = self.page.getInfoFromMosaicFocus()
            self.assertIsNotNone(item, "   ERR   cannot get value from mosaic focus")

            self.assertTrue(item.getLcn() == channels[0], "   ERR   wrong channel highlighted")

            self.rc.sendKeys(["KEY_DOWN", "KEY_RIGHT"])
            time.sleep(5)
            item = self.page.getInfoFromMosaicFocus()
            self.assertIsNotNone(item, "   ERR   cannot get value from mosaic focus")
            self.assertTrue(item.getLcn() == channels[1], "   ERR   wrong channel highlighted")

            self.rc.sendKeys(["KEY_FORWARD"])
            time.sleep(5)
            self.rc.sendKeys(["KEY_Left"])
            time.sleep(5)
            item = self.page.getInfoFromMosaicFocus()
            self.assertIsNotNone(item, "   ERR   cannot get value from mosaic focus")
            self.assertTrue(item.getLcn() == channels[2], "   ERR   wrong channel highlighted")

            self.rc.sendKeys(["KEY_UP", "KEY_RIGHT", "KEY_RIGHT"])
            time.sleep(5)
            item = self.page.getInfoFromMosaicFocus()
            self.assertIsNotNone(item, "   ERR   cannot get value from mosaic focus")

            self.assertTrue(item.getLcn() == channels[3], "   ERR   wrong channel highlighted")

            self.rc.sendKeys(["KEY_FORWARD"])
            time.sleep(5)
            item = self.page.getInfoFromMosaicFocus()
            self.assertIsNotNone(item, "   ERR   cannot get value from mosaic focus")

            self.assertTrue(item.getLcn() == channels[4], "   ERR   wrong channel highlighted")

            self.rc.sendKeys(["KEY_LEFT", "KEY_LEFT", "KEY_DOWN"])
            time.sleep(5)
            item = self.page.getInfoFromMosaicFocus()
            self.assertIsNotNone(item, "   ERR   cannot get value from mosaic focus")

            self.assertTrue(item.getLcn() == channels[5], "   ERR   wrong channel highlighted")

            self.rc.sendKeys(["KEY_FORWARD"])
            time.sleep(5)
            item = self.page.getInfoFromMosaicFocus()
            self.assertIsNotNone(item, "   ERR   cannot get value from mosaic focus")

            self.assertTrue(item.getLcn() == channels.pop(6), "   ERR   wrong channel highlighted")

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
