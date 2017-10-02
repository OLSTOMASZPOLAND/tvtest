# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import datetime
import time

class TC_3391_T014692_set_the_green_parameter_update(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3391 - T014692 set_the_green_parameter_update
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        if not self.page.cleanDeleteAllRecordings():
            self.page.cleanDeleteAllRecordings()
        try:
            self.page.goToTvSettings()
            self.page.actionSelect(Menu.greenMode)
            self.page.actionSelect(DialogBox.GreenEnergyOff)
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        except:
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            self.page.goToTvSettings()
            self.page.actionSelect(Menu.greenMode)
            self.page.actionSelect(DialogBox.GreenEnergyOff)
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])

        try:
            self.logger.info("----- " + self.__class__.__name__ + " START -----")

            ''' prestep '''
            self.logStepResults("AT_THE_BEGINNING")
            try:
                T1 = self.rc.sendUrl(Rpi.URL_RPI + 'StbGetDataModel.php?key=T1Timer&editMode=false&useRegExp=true&ignoreCase=true')
                T1 = T1.read()
                T1 = T1.rsplit('=')[1]
                T1 = int(T1)
                self.logger.debug("T1 set to:" + T1)
            except Exception, e:
                T1 = 900

            try:
                T2 = self.rc.sendUrl(Rpi.URL_RPI + 'StbGetDataModel.php?key=T2Timer&editMode=false&useRegExp=true&ignoreCase=true')
                T2 = T2.read()
                T2 = T2.rsplit('=')[1]
                T2 = int(T2)
                self.logger.debug("T2 set to:" + T2)
            except Exception, e:
                T2 = 300
            self.rc.zap(self.rc.getChannelTVP1HD)
            ''' step '''
            self.logStepBeginning("turn on green mode")
            self.assertTrue(self.page.goToTvSettings(), "   ERR    cannot go to tv settings")

            self.assertTrue(self.page.actionSelect(Menu.greenMode), "   ERR   cannot select " + Menu.greenMode)

            self.assertTrue(self.page.findInDialogBox(DialogBox.GreenEnergyOff), "   ERR   cant find " + DialogBox.GreenEnergyOff)
            self.assertTrue(self.page.findInDialogBox(DialogBox.GreenEnergyOn), "   ERR   cant find " + DialogBox.GreenEnergyOn)

            self.assertTrue(self.page.actionSelect(DialogBox.GreenEnergyOn), "   ERR   cant turn on green mode")

            time.sleep(15)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)

            try:
                state = self.page.driver.find_elements_by_css_selector(".content .orange")[1].text.encode('utf-8')
            except:
                self.fail("   ERR   cannot get current green mode state")

            self.assertTrue(state == Menu.greenModeTurnedOn, "   ERR   incorrect message about current green mode state")

            self.logStepResults("turn on green mode")

            self.logStepBeginning("go to sleep T1 + T2 timers")

            self.rc.sendKeys(["KEY_POWER"])
            self.page.sleep(T1 + T2 + 60)

            self.logStepResults("go to sleep T1 + T2 timers")

            self.logStepBeginning("wake up, check current green mode state and deactivate")
            self.rc.sendKeys(["KEY_POWER"])

            try:
                currTime = datetime.datetime.now()
                status = False
                moje = None
                time.sleep(15)
                while (status == False):
                    datanow = datetime.datetime.now()
                    calc = datanow - currTime
                    calc = calc.seconds
                    if (calc > 240):
                        status = True
                    self.rc.sendKeys(["KEY_INFO"])
                    time.sleep(2)
                    moje = self.page.getInfoFromLiveBanner()
                    time.sleep(3)
                    if moje != None:
                        status = True
                time.sleep(3)
                self.rc.sendKeys(["KEY_BACK"])
            except:
                time.sleep(240)
                pass

            self.assertTrue(self.page.goToTvSettings(), "   ERR    cannot go to tv settings")

            self.assertTrue(self.page.actionSelect(Menu.greenMode), "   ERR   cannot select " + Menu.greenMode)

            self.assertTrue(self.page.findInDialogBox(DialogBox.GreenEnergyOff), "   ERR   cant find " + DialogBox.GreenEnergyOff)
            self.assertTrue(self.page.findInDialogBox(DialogBox.GreenEnergyOn), "   ERR   cant find " + DialogBox.GreenEnergyOn)

            self.assertTrue(self.page.actionSelect(DialogBox.GreenEnergyOff), "   ERR   cant turn on green mode")

            time.sleep(15)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)

            try:
                state = self.page.driver.find_elements_by_css_selector(".content .orange")[1].text.encode('utf-8')
            except:
                self.fail("   ERR   cannot get current green mode state")

            self.assertTrue(state == Menu.greenModeTurnedOff, "   ERR   incorrect message about current green mode state")

            self.logStepResults("wake up, check current green mode state and deactivate")

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
                try:
                    self.page.goToTvSettings()
                    self.page.actionSelect(Menu.greenMode)
                    self.page.actionSelect(DialogBox.GreenEnergyOff)
                except:
                    self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
                    self.page.goToTvSettings()
                    self.page.actionSelect(Menu.greenMode)
                    self.page.actionSelect(DialogBox.GreenEnergyOff)
