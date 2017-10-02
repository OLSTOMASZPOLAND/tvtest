# -*- coding: utf-8 -*-

import time

from NewTvTesting.Config import *
from OPL_Testing.TC_OPL_template import TC_OPL_template


class TC_3432_T016029_Set_the_default_subtitle_polish_DTT_stream(TC_OPL_template):
    '''
    Coverage: HP QC test ID - 3432 - T016029_Set the default subtitle - polish - DTT stream
    
    @author: Kamil Kulinski
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        try:

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")

            if not self.page.cleanDeleteAllRecordings():
                self.page.cleanDeleteAllRecordings()

            ''' Initial State '''
            self.logStepBeginning("Initial State - User is in My account - My preferences screen")

            self.page.setParentalControl(ParentalControl.SetDeactive)
            self.assertTrue(self.page.setDTTChannels(True), "   ERR   cannot find DTT channels")
            time.sleep(2)
            self.rc.sendKeys(["KEY_MENU"])
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myAccount))
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.mySettings))
            time.sleep(2)

            self.logStepResults("Initial State - User is in My account - My preferences screen")

            ''' Step 3 '''
            self.logStepBeginning("Step 3 - Select subtitles item")

            self.assertTrue(self.page.actionSelect(Menu.subtitles))
            time.sleep(2)

            self.assertTrue(self.page.findInList(Menu.noSubtitle), "ERR: no 'brak' option in 'napisy' menu")
            self.assertTrue(self.page.findInList(Menu.nativeSubtitles), "ERR: no 'polskie' option in 'napisy' menu")
            self.assertTrue(self.page.findInList(Menu.hearingImpairedSubtitles), "ERR: no 'dla nieslyszacych' option in 'napisy' menu")
            time.sleep(2)

            self.logStepResults("STEP 3 - Select subtitles item")

            ''' Step 4 '''
            self.logStepBeginning("STEP 4 - Choose 'polskie' option and validate")

            self.assertTrue(self.page.actionSelect(Menu.nativeSubtitles))

            self.logStepResults("STEP 4 - Choose 'polskie' option and validate")

            ''' Step 5 '''
            self.logStepBeginning("STEP 5 - Watch a broadcasting DTT stream and check the subtitles")

            time.sleep(2)
            self.rc.sendKeys(["KEY_TV"])
            time.sleep(2)
            self.assertTrue(self.page.zapToChannel(self.rc.getChannelHBOHD), " ERR  cannot zap to channel  " + str(self.rc.getChannelHBOHD))
            time.sleep(8)
            self.rc.sendKeys(["KEY_OK"])

            self.assertTrue(self.page.findInList(Menu.toolboxNativeSubtitle), "ERR: Problem checking if subtitles in toolbox have changed or subtitles are currently unavailable")
            time.sleep(2)

            self.logStepResults("STEP 5 - Watch a broadcasting DTT stream and check the subtitles")

            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise
        finally:
            self.logger.info("----------- cleaning -----------")

            self.rc.sendKeys(["KEY_MENU"])
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.myAccount))
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.mySettings))
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.subtitles))
            time.sleep(2)
            self.assertTrue(self.page.findInList(Menu.nativeSubtitles))
            time.sleep(2)
            self.assertTrue(self.page.actionSelect(Menu.noSubtitle))
