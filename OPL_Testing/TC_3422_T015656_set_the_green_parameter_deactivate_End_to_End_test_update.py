# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
import datetime
import time

class TC_3422_T015656_set_the_green_parameter_deactivate_End_to_End_test_update(TC_OPL_template):
    '''Implementation of the HP QC test ID - 3422- _set_the_green_parameter_deactive_End_to_End_test_update
    
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
            self.page.actionSelect(DialogBox.GreenEnergyOn)
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
        except:
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            self.page.goToTvSettings()
            self.page.actionSelect(Menu.greenMode)
            self.page.actionSelect(DialogBox.GreenEnergyOn)
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

            try:
                T3 = self.rc.sendUrl(Rpi.URL_RPI + 'StbGetDataModel.php?key=T3Timer&editMode=false&useRegExp=true&ignoreCase=true')
                T3 = T3.read()
                T3 = T3.rsplit('=')[1]
                T3 = int(T3)
                self.logger.debug("T3 set to:" + T3)
            except Exception, e:
                T3 = 300

            ''' step '''
            self.logStepBeginning("turn on green mode")
            self.assertTrue(self.page.goToTvSettings(), "   ERR    cannot go to tv settings")

            self.assertTrue(self.page.actionSelect(Menu.greenMode), "   ERR   cannot select " + Menu.greenMode)

            self.assertTrue(self.page.actionSelect(DialogBox.GreenEnergyOff), "   ERR   cant turn off green mode")

            time.sleep(15)
            self.page.driver.get(Rpi.DUMP)
            time.sleep(1)

            try:
                state = self.page.driver.find_elements_by_css_selector(".content .orange")[1].text.encode('utf-8')
            except:
                self.fail("   ERR   cannot get current green mode state")

            self.assertTrue(state == Menu.greenModeTurnedOff, "   ERR   incorrect message about current green mode state")

            self.logStepResults("turn off green mode")

            self.logStepBeginning("set future record and go to sleep T1 + T2 + T3 timers")
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_TV"])
            self.assertTrue(self.page.goToPvrMenu(), "   ERR   cannot go to pvr menu")
            self.assertTrue(self.page.actionSelect(Menu.pvrManualRecord), "   ERR   cannot select " + Menu.pvrManualRecord)
            time.sleep(5)

            start = datetime.datetime.now() + datetime.timedelta(seconds=T1 + T2 + T3)

            item = self.page.actionScheduleRecord(self.rc.getChannelTVPPolonia, start, 30)

            self.assertTrue(item, "   ERR   cannot set record")

            self.rc.sendKeys(["KEY_POWER"])

            self.page.sleep(T1 + T2 + T3 + 120)

            self.logStepResults("set future record and go to sleep T1 + T2 + T3 timers")

            self.logStepBeginning("wake up and check if record is made")
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

            self.assertTrue(self.page.goToPvrMyRecords(), "   ERR   cannot go to my records")
            self.rc.sendKeys(["KEY_OK"])
            time.sleep(3)

            record = self.page.getInfoFromRecordPage()
            if not record:
                self.fail("   ERR   cannot get info about the record")

            self.assertTrue(record.getRecording(), "   ERR   channel is not recording")
            self.assertTrue(self.page.actionSelect(Menu.pvrPlay), "   ERR   cannot select " + Menu.pvrPlay)
            time.sleep(15)
            self.assertTrue(self.page.checkLive(True), "   ERR   motion detection failed")
            self.rc.sendKeys(["KEY_BACK"])
            time.sleep(5)
            self.page.deletePvrRecord(True)

            self.logStepResults("wake up and check if record is made")

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

                if not self.page.cleanDeleteAllRecordings():
                    self.page.cleanDeleteAllRecordings()
