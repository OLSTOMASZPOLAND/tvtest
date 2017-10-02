# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import Menu, Rpi
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TC_11157_Always_record_HDD(TC_OPL_template):
    '''
        Purpose: If tricbar changes it state when video goes to the end/beginning of the buffor.
        When video stops, pauses, ect.
    
        @author: Grzegorz Krolikowski
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            self.assertTrue(self.page.zapToChannel(self.rc.findChannelByName("TVP Polonia")), "   ERR   Can't zap to channel 8")
            
            ''' step '''
            self.logStepBeginning("step 1")
            
            time.sleep(600)
            
            self.rc.sendKeys(["KEY_REWIND"])        
            time.sleep(3)
             
            trick = self.page.getInfoFromTrickBar()
            self.assertTrue(trick, "   ERR   Can't get trickbar")
            icon = trick.getTrickIcon()
            self.logger.debug(icon)
            self.assertTrue(icon, "   ERR   Can't get trickbar icon")
            self.assertTrue(icon == "Rewind4", "   ERR   Trickbar is different than 'Rewind4'")
            
            for x in range(4):
                self.rc.sendKeys(["KEY_REWIND"])
                time.sleep(3)
            
            self.logStepResults("step 1")

            ''' step '''
            self.logStepBeginning("step 2")
            
            time.sleep(5)
            
            for x in range(4):
                trick = self.page.getInfoFromTrickBar()
                self.assertTrue(trick, "   ERR   Can't get trickbar")
                icon = trick.getTrickIcon()
                self.logger.debug(icon)
                self.assertTrue(icon, "   ERR   Can't get trickbar icon")
                time.sleep(3)
                if(icon == "Play"):
                    self.logger.debug("---Playing")
                    break
                else:
                    time.sleep(15)
                    self.logger.debug("---Still rewinding")
                    pass
            else:
                self.fail("   ERR   Device didn't turn to play mode after end of the buffor")
                
            time.sleep(3)
            self.rc.sendKeys(["KEY_PLAY"])
            time.sleep(3)
            
            trick = self.page.getInfoFromTrickBar()
            self.assertTrue(trick, "   ERR   Can't get trickbar")
            icon = trick.getTrickIcon()
            self.logger.debug(icon)
            self.assertTrue(icon, "   ERR   Can't get trickbar icon")
            self.assertTrue(icon == "Pause", "   ERR   Trickbar is different than 'Pause'")
            
            messageSedcondRow = trick.getMessageSecondRow()
            self.logger.debug(messageSedcondRow)
            
            self.logStepResults("step 2")
            
            ''' step '''
            self.logStepBeginning("step 3")
            
            self.rc.sendKeys(["KEY_FORWARD"])
            time.sleep(15)
            
            trick = self.page.getInfoFromTrickBar()
            self.assertTrue(trick, "   ERR   Can't get trickbar")
            icon = trick.getTrickIcon()
            self.assertTrue(icon, "   ERR   Can't get trickbar icon")
            self.assertTrue(icon == "Forward4", "   ERR   Trickbar is different than 'Forward4'")
            
            for x in range(4):
                time.sleep(3)
                self.rc.sendKeys(["KEY_PLAY"])
                time.sleep(3)
                self.rc.sendKeys(["KEY_PLAY"])
                time.sleep(3)
            
                trick = self.page.getInfoFromTrickBar()
                self.assertTrue(trick, "   ERR   Can't get trickbar")
                icon = trick.getTrickIcon()
                self.logger.debug(icon)
                self.assertTrue(icon, "   ERR   Can't get trickbar icon")
                self.assertTrue(icon == "Pause", "   ERR   Trickbar is different than 'Pause'")
            
                messageSedcondRow2 = trick.getMessageSecondRow()
                self.logger.debug(messageSedcondRow2)
                
                if(messageSedcondRow != messageSedcondRow2):
                    self.logger.debug("---messageSecondRow != messageSecondRow2")
                    self.logger.debug(messageSedcondRow)
                    self.logger.debug(messageSedcondRow2)
                    break
                else:
                    self.rc.sendKeys(["KEY_FORWARD"])
                    time.sleep(15)
            else:
                self.fail("   ERR   Time doesn't change")
            
            self.logStepResults("step 3")
            
            ''' step '''
            self.logStepBeginning("step 4")
            
            for x in range(4):
                self.rc.sendKeys(["KEY_FORWARD"])
                time.sleep(3)
                
            for x in range(4):
                trick = self.page.getInfoFromTrickBar()
                self.assertTrue(trick, "   ERR   Can't get trickbar")
                icon = trick.getTrickIcon()
                self.logger.debug(icon)
                self.assertTrue(icon, "   ERR   Can't get trickbar icon")
                time.sleep(3)
                if(icon == "Play"):
                    self.logger.debug("---Playing")
                    break
                else:
                    time.sleep(15)
                    self.logger.debug("---Still forwarding")
                    pass
            else:
                self.fail("   ERR   Device didn't turn to play mode after end of the buffor")
            
            self.logStepResults("step 4")
            
            ''' step '''
            self.logStepBeginning("step 5")

            self.rc.sendKeys(["KEY_REWIND"])
            time.sleep(3)
            
            trick = self.page.getInfoFromTrickBar()
            self.assertTrue(trick, "   ERR   Can't get trickbar")
            icon = trick.getTrickIcon()
            self.assertTrue(icon, "   ERR   Can't get trickbar icon")
            self.assertTrue(icon == "Rewind4", "   ERR   Trickbar is different than 'Rewind4'")
            
            for x in range(4):
                self.rc.sendKeys(["KEY_REWIND"])
                time.sleep(3)
            
            self.rc.sendKeys(["KEY_PLAY"])
            time.sleep(3)
            self.rc.sendKeys(["KEY_PLAY"])
            
            trick = self.page.getInfoFromTrickBar()
            self.assertTrue(trick, "   ERR   Can't get trickbar")
            icon = trick.getTrickIcon()
            self.logger.debug(icon)
            self.assertTrue(icon, "   ERR   Can't get trickbar icon")
            self.assertTrue(icon == "Pause", "   ERR   Trickbar is different than 'Pause'")
            
            messageSedcondRow= trick.getMessageSecondRow()
            self.assertTrue(messageSedcondRow, "   ERR   Can't find 'z zapisu'")
            self.logger.debug(messageSedcondRow)
            
            self.logStepResults("step 5")
            
            ''' step '''
            self.logStepBeginning("step 6")
            
            self.rc.sendKeys(["KEY_STOP"])
            time.sleep(3)
            
            trick = self.page.getInfoFromTrickBar()
            self.assertTrue(trick, "   ERR   Can't get trickbar")
            icon = trick.getTrickIcon()
            self.logger.debug(icon)
            self.assertTrue(icon, "   ERR   Can't get trickbar icon")
            self.assertTrue(icon == "Play", "   ERR   Device is not playing live")
            
            self.logStepResults("step 6")
            
            self.test_passed = True
            self.logger.info("----- " + self.__class__.__name__ + " END -----")

        except Exception, e:
            self.logStepResults("Error occurred - %s" % e)
            self.logger.info("   ERR:   Error occurred - %s" % e)
            raise

        finally:
            if not self.test_passed:
                self.logger.info("----------- cleaning -----------")
                #self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
