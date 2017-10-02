# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import Rpi
import time

class TC_11151_full_buffer_Flash(TC_OPL_template):
    '''Implementation of the HP QC test ID - 0000 - T999999
    
        Purpose: Check if recorded live is available and works properly after 1h diff
        
        @author: Grzegorz Krolikowski
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            
            self.logStepResults("AT_THE_BEGINNING")
            self.assertTrue(self.page.zapToChannel(8), "   Can't zap to channel 8")
            self.page.rc.sendKeys(["KEY_PLAY"])
            time.sleep(2)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(2)
            try:
                paused = self.page.driver.find_element_by_id("message")
                paused = paused.text
                self.logger.info("--- Live strem is paused")
            except:
                self.fail("   ERR   There is no '#message' id or live stream is not paused")
                
            checkText = paused.split(":")
            if(checkText[0] != "z zapisu"):
                self.fail("   ERR   'z zapisu' not found")
                    
            trickBar = self.page.getInfoFromTrickBar()
            self.assertTrue((trickBar), "   ERR   No trickBar obcject")
            if(trickBar.getTrickIcon() != "Pause"):
                self.fail("   ERR   No trickBar obcject or not in pause mode")
            
            ''' step '''
            
            self.logStepBeginning("step 1")
            
            time.sleep(3600)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(2)
            
            try:
                pausedAlert = self.page.driver.find_element_by_id("alert")
                pausedAlert = pausedAlert.text.encode('utf-8')
            except:
                self.fail("   ERR   There is no '.alert'")
                
            if(pausedAlert != "maksymalna długość nagrania z zapisu jest osiągnięta"):
                self.fail("   ERR   alert is not 'maksymalna długość nagrania z zapisu jest osiągnięta'")
            
            self.logStepResults("step 1")
            
            ''' step '''
            
            self.logStepBeginning("step 2")
            
            self.rc.sendKeys(["KEY_PLAY"])
            time.sleep(2)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(2)
            
            try:
                play = self.page.driver.find_element_by_css_selector("#message")
                play = play.get_attribute('innerHTML')
                self.logger.info("--- Live strem is playing")
            except:
                self.fail("   ERR   There is no '#message' id or live stream is not playing")
                
            trickBar = self.page.getInfoFromTrickBar()
            self.assertTrue((trickBar), "   ERR   No trickBar obcject")
            if(trickBar.getTrickIcon() != "Play"):
                self.fail("   ERR   No trickBar obcject or not in play mode")

            self.logStepResults("step 2")
            
            ''' step '''

            self.logStepBeginning("step 3")
            
            for x in range(4):
                self.rc.sendKeys(["KEY_FORWARD"])
                time.sleep(3)
            
            for x in range(4):
                self.page.driver.get(Rpi.DUMP)
                time.sleep(3)
                trickBar = self.page.getInfoFromTrickBar()
                self.assertTrue((trickBar), "   ERR   No trickBar obcject")
                if((trickBar.getTrickIcon() == "Play") or (trickBar.getTrickIcon() == "Forbidden")):
                    self.logger.debug("---Playing")
                    break
                else:
                    self.logger.debug("---Still forwarding")
                    time.sleep(15)
                    pass
            else:
                self.fail("   ERR   Device didn't turn to play mode after end of the buffor")
            
            time.sleep(3)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(3)
 
            try:
                playedLive = self.page.driver.find_element_by_css_selector("#message")
                playedLive = playedLive.get_attribute('innerHTML')
                self.logger.info("--- Live strem is paused")
            except:
                self.fail("   ERR   There is no '#message' id or live stream is not paused")
                
            if(playedLive.encode('utf-8') != "na żywo"):
                self.fail("   ERR   'na zywo' not found")
                
            self.logStepResults("step 3")
            
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
