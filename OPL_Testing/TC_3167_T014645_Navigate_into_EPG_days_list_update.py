# -*- coding: utf-8 -*-



import time



from NewTvTesting.Config import *

from OPL_Testing.TC_OPL_template import TC_OPL_template

from NewTvTesting.DataSet import LiveData





class TC_3167_T014645_Navigate_into_EPG_days_list_update(TC_OPL_template):

    """Implementation of the HP QC test ID - 3167 T014645_Navigate_into_EPG_days_list_update
    @author: Tomasz Stasiuk
    """



    def __init__(self, methodName):

        TC_OPL_template.__init__(self, methodName)



    def test(self):

        self.logger.info("----- " + self.__class__.__name__ + " START -----")



        ''' prestep '''

        self.logStepResults("AT_THE_BEGINNING")
        time.sleep(3)


        ''' step '''
        self.logStepBeginning("STEP - go to Tomorrow EPG")
        self.rc.zap(1)
        self.rc.sendKeys(["KEY_GREEN"])
        time.sleep(5)
        self.assertTrue(self.page.actionSelect(Menu.epg), "ERROR IN GO TO EPG(GREEN_BUTTON)")
        time.sleep(2)
        self.assertTrue(self.page.actionSelect(Menu.epgDay), "Error in Go to EPG Tomorrow")  # epgDay
        time.sleep(2)
        self.assertTrue(self.page.actionSelect(Menu.epgDayTomorrow), "Error in Go to EPG Tomorrow")  # epgDay
        time.sleep(2)
        self.assertTrue(self.page.findInPage(Menu.epgDayTomorrow), 'Error of information of EPG Tomorrow')
        time.sleep(5)
        self.assertTrue(self.page.checkIfEpgIsAvalaible(), '>> ERROR  lack of EPG')
        self.logStepResults("STEP - go to Tomorrow EPG")

        ''' step '''
        self.logStepBeginning("STEP -check working Key")
        self.assertTrue(self.page.checkWorkingEpgKey("KEY_LEFT", 'start'))
        self.assertTrue(self.page.checkWorkingEpgKey("KEY_RIGHT", 'start'))
        self.assertTrue(self.page.checkWorkingEpgKey("KEY_DOWN", "channelName"))
        self.assertTrue(self.page.checkWorkingEpgKey("KEY_UP", "channelName"))
        self.assertTrue(self.page.checkWorkingEpgKey("KEY_FORWARD", "channelName"))
        self.assertTrue(self.page.checkWorkingEpgKey("KEY_REWIND", "channelName"))
        self.logStepResults("STEP - check working Key")

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

