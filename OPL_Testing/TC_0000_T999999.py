# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template

class TC_0000_T999999(TC_OPL_template):
    '''Implementation of the HP QC test ID - 0000 - T999999
    
        @author: XXX XXX
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")

            ''' step '''
            self.logStepBeginning("step 1")
            # step logic
            self.assertTrue(self.page.goToVodMenu())
            self.logStepResults("step 1")

            #===================================================================
            # ''' step '''
            # self.logStepBeginning("step 2")
            # # step logic
            # self.assertTrue(self.page.goToVodMenu())
            # self.logStepResults("step 2")
            #===================================================================

            # self.page.cleanFunction()

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
                # clean logic
                # self.page.cleanFunction()
