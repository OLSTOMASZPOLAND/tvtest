# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import Rpi, Env
import datetime
import time
from NewTvTesting.Utils import getReportsDirPath, generateScreenFilePath, \
    generateStbLogFilePath, writeStbLogsToFile
from NewTvTesting.StbtIntegration import screenshot

class TC_0000_endurance_with_power_off(TC_OPL_template):
    '''Implementation
            Original test scenario (for UHD88) is as follows:
    
    -          Boot STB with PVR HDD and zap to channel 1 (start condition)
        
    -          Press P+ button
    
    -          Wait 60 seconds
    
    -          Press EPG button
    
    -          Wait 5 seconds
    
    -          Press OK button
    
    -          Wait 10 seconds
    
    -          Press BACK button
    
    -          Wait 5 seconds
    
    -          Press DOWN button
    
    -          Wait 5 seconds
    
    -          Press OK button
    
    -          Wait 10 seconds
    
    -          Press TV/Live button
    
    -          Wait 25 seconds
    
    -          REPEAT THE CYCLE (cycle length is 2 minutes)
    
    
    
    -          After every 3h and 20 minutes (so after 100 cycles) zap to channel 1 (step delayed by 10 seconds to perform during 60 seconds waiting gap) – step performed to zap not higher than channel 110 (service plan issue).

        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        self.logger.info("REMEMBER TO SET DATAMODEL T1 TIME TO 1800")

        self.logger.info("REMEMBER TO SET DATAMODEL T1 TIME TO 1800")

        self.logger.info("REMEMBER TO SET DATAMODEL T1 TIME TO 1800")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        ''' step '''
        self.logStepBeginning("start zapping")

        KANAL_STARTOWY = 266
        KANAL_KONCOWY = 326
        self.sleep_time_in_mins = 15
        self.shutdown_interval_in_hours = 24

        self.timeReportFile = open(getReportsDirPath() + "/" + self.reportsPath + "/times.txt", "a")

        keyup = Rpi.URL_RPI_KEY + "KEY_CHANNELUP"
        keyepg = Rpi.URL_RPI_KEY + "KEY_GUIDE"
        keyok = Rpi.URL_RPI_KEY + "KEY_OK"
        keyback = Rpi.URL_RPI_KEY + "KEY_BACK"
        keydown = Rpi.URL_RPI_KEY + "KEY_DOWN"
        keytv = Rpi.URL_RPI_KEY + "KEY_TV"
        keymwnu = Rpi.URL_RPI_KEY + "KEY_MENU"

        if not self.page.zapToChannel(KANAL_STARTOWY):
            self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_MENU", "KEY_BACK"])
            time.sleep(2)
            self.page.zapToChannel(KANAL_STARTOWY)

        self.rc.startLogs()
        time.sleep(15)
        self.set_next_shutdown()

        i = KANAL_STARTOWY

        while True:
            try:
                if datetime.datetime.now() > self.next_shutdown:
                    self.go_standby()

                try:
                    #if Env.STB_MODEL != "DAKOTA":
                    log = self.page.findInLogs('stb.event> StbEvent> HANDLER: MEDIA - REASON: AREA_CHANGED - ATTRIBUTES: {"session_id":"LIVE"}', 10, False, repeats=3)
                    log.start()
                    self.rc.sendUrl(keyup)
                    self.logger.info("P+ send")
                    signal = datetime.datetime.now()
                    while log.working:
                        time.sleep(0.1)

                    if not log.found:
                        self.timeReportFile.write(str(datetime.datetime.now()).split(".")[0] + ";0\n")

                    else:
                        self.timeReportFile.write(str(datetime.datetime.now()).split(".")[0] + ";" + str((datetime.datetime.now() - signal).total_seconds()) + "\n")

                    self.timeReportFile.flush()

                    if Env.VIDEO:
                        screenshot(generateScreenFilePath(self.reportsPath, "screenshot P+"))

                except Exception, e:
                    self.logger.error(str(e))

                finally:
                    dream = 15.0 - (datetime.datetime.now() - signal).total_seconds()
                    if dream > 0:
                        time.sleep(dream)

                self.rc.sendUrl(keyepg)
                time.sleep(5)

                self.rc.sendUrl(keyok)
                time.sleep(10)

                self.rc.sendUrl(keyback)
                time.sleep(5)

                self.rc.sendUrl(keydown)
                time.sleep(5)

                self.rc.sendUrl(keyok)
                time.sleep(10)

                self.rc.sendUrl(keyup)
                time.sleep(10)

                writeStbLogsToFile(self.rc.getLogs(), generateStbLogFilePath(self.reportsPath, "after single run"))

                if i > KANAL_KONCOWY:
                    if not self.page.zapToChannel(KANAL_STARTOWY):
                        self.rc.sendKeys(["KEY_BACK", "KEY_BACK", "KEY_MENU", "KEY_BACK"])
                        time.sleep(2)
                        self.page.zapToChannel(KANAL_STARTOWY)
                    i = KANAL_STARTOWY
                else:
                    i += 1

            except Exception, e:
                self.logger.error(str(e))
                try:
                    self.rc.stopLogs()
                    writeStbLogsToFile(self.rc.getLogs(), generateStbLogFilePath(self.reportsPath, "on exception"))
                    self.rc.startLogs()
                    if Env.VIDEO:
                        screenshot(generateScreenFilePath(self.reportsPath, "screenshot on exception"))
                    self.logger.error(str(e))
                except Exception, e:
                    self.logger.error(str(e))

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

    def go_standby(self):
        self.logger.info("Going to sleep...")
        key_power = Rpi.URL_RPI_KEY + "KEY_POWER"
        self.rc.sendUrl(key_power)
        time.sleep(10)
        if Env.VIDEO:
            screenshot(generateScreenFilePath(self.reportsPath, "on sleep"))
        self.page.sleep(self.sleep_time_in_mins * 60)
        self.rc.sendUrl(key_power)
        self.logger.info("Waking up...")

        time.sleep(5)
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
                self.rc.sendKeys(["KEY_CHANNELUP"])
                self.rc.sendKeys(["KEY_INFO"])
                time.sleep(2)
                moje = self.page.getInfoFromLiveBanner()
                time.sleep(3)
                if moje != None:
                    status = True
            print calc
            time.sleep(3)
            self.rc.sendKeys(["KEY_BACK"])
        except:
            time.sleep(240)
            self.logger.error("waking up timeout")
        self.set_next_shutdown()

    def set_next_shutdown(self):
        self.next_shutdown = datetime.datetime.now() + datetime.timedelta(hours=self.shutdown_interval_in_hours)
        self.logger.info("Next shutdown: {}".format(self.next_shutdown))
