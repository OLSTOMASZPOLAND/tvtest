# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import Menu, Rpi
import time

class TC_11146_mute_Flash(TC_OPL_template):
    '''
        Purpose: Check if mute icon displays in diff mode on flash memory
    
        @author: Grzegorz Krolikowski
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            self.assertTrue(self.page.zapToChannel(8), "   ERR   Can't zap to channel 8")
            time.sleep(60)

            ''' step '''
            self.logStepBeginning("step 1")
            
            self.rc.sendKeys(["KEY_MUTE"])
            time.sleep(5)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(2)
            try:
                mute = self.page.driver.find_element_by_css_selector(".volume.muted.hidden")
                self.logger.info("--- Live strem is muted")
            except:
                self.fail("   ERR   There is no '.volume.muted.hidden' class or live stream is not muted")
        
            self.logStepResults("step 1")
            
            ''' step '''
            self.logStepBeginning("step 2")
            
            self.rc.sendKeys(["KEY_MUTE"])
            time.sleep(5)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(2)
            try:
                mute = self.page.driver.find_element_by_css_selector(".volume.hidden")
                self.logger.info("--- Live strem is muted")
            except:
                self.fail("   ERR   There is no '.volume.hidden' class or live stream is muted")
            
            self.logStepResults("step 2")

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
