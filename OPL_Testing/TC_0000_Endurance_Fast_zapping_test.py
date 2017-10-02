# -*- coding: utf-8 -*-

from OPL_Testing.TC_OPL_template import TC_OPL_template
from NewTvTesting.Config import *
from NewTvTesting.StbtIntegration import motionDetection, screenshot
import time
import datetime
from NewTvTesting.Utils import writeStbLogsToFile, generateStbLogFilePath, \
    generateScreenFilePath, getReportsDirPath

class TC_0000_Endurance_Fast_zapping_test(TC_OPL_template):
    '''Implementation of the Endurance_TC100-01_Fast_zapping_test_HD-HD_5sec
    
        @author: Marcin Gmurczyk
    '''

    def __init__(self, methodName):
        TC_OPL_template.__init__(self, methodName)

    def test(self):
        self.logger.info("----- " + self.__class__.__name__ + " START -----")

        ''' prestep '''
        self.logStepResults("AT_THE_BEGINNING")

        self.delay = 0  # w godzinach
        self.interval = 10.0  # jako float
        self.firstChannel = 1
        self.secondChannel = 22
        self.testTime = 142  # w godzinach

        ''' step '''
        self.timeReportFile = open(getReportsDirPath() + "/" + self.reportsPath + "/times.txt", "a")

        self.logStepBeginning("step set favorite channels")

        self.page.setFavoriteChannels([self.firstChannel, self.secondChannel])
        time.sleep(5)

        self.logStepResults("step set favorite channels")

        ''' step '''
        self.logStepBeginning("start zapping - interval >%i< - firstChannel >%i< - secondChannel >%i< - testTime >%ih<" % (self.interval, self.firstChannel, self.secondChannel, self.testTime))

        self.assertTrue(self.page.zapToChannel(self.firstChannel), "   ERR   cannot zap to channel " + str(self.firstChannel))
        time.sleep(10)
        if Env.VIDEO:
            self.assertTrue(motionDetection(), "   ERR    motion detection is not working")

        self.assertTrue(self.page.zapToChannel(self.secondChannel), "   ERR   cannot zap to channel " + str(self.secondChannel))
        time.sleep(10)

        if Env.VIDEO:
            self.assertTrue(motionDetection(), "   ERR    motion detection is not working")

        self.rc.sendKeys(["KEY_LIST"])
        time.sleep(2)
        self.page.driver.get(Rpi.DUMP)
        time.sleep(1)

        try:
            item = self.page.driver.find_element_by_css_selector(".zappingList .titleContent")
            item = item.text.encode('utf-8')
            while item != Description.favoriteInList:
                self.rc.sendKeys(["KEY_RIGHT"])
                time.sleep(2)
                self.page.driver.get(Rpi.DUMP)
                time.sleep(1)
                item = self.page.driver.find_element_by_css_selector(".zappingList .titleContent")
                item = item.text.encode('utf-8')
        except Exception, e:
            self.fail("   ERR   cannot load favorite list: " + str(e))

        self.rc.sendKeys(["KEY_BACK"])

        if self.delay != 0:
            self.logger.info("sleeping for: " + str(self.delay * 3600 - 180) + " seconds")
            time.sleep(self.delay * 3600 - 180)
            self.resetSTB()

        self.foo = 60 / self.interval
        if self.foo % 2 == 0:
            self.foo += 1

        time.sleep(10)

        self.rc.sendKeys(["KEY_LIST"])
        time.sleep(2)
        self.page.driver.get(Rpi.DUMP)
        time.sleep(1)

        item = self.page.driver.find_element_by_css_selector(".zappingList .titleContent").text.encode('utf-8')
        self.assertTrue(Description.favoriteInList == item, "   ERR   cannot display list")

        start = datetime.datetime.now()
        end = datetime.datetime.now() + datetime.timedelta(hours=self.testTime)

        self.logger.info("Start time: " + str(start))
        self.logger.info("End time: " + str(end))

        while self.startZapping(start, end):
            pass

        self.timeReportFile.close()
        self.logStepResults("start zapping - interval >%i< - firstChannel >%i< - secondChannel >%i< - testTime >%ih<" % (self.interval, self.firstChannel, self.secondChannel, self.testTime))

        self.test_passed = True
        self.logger.info("----- " + self.__class__.__name__ + " END -----")

    def startZapping(self, start, end):
        self.logSave = 0
        try:
            while(start < end):
                log = self.page.findInLogs('stb.event> StbEvent> HANDLER: MEDIA - REASON: AREA_CHANGED - ATTRIBUTES: {"session_id":"LIVE"}', self.interval, False, repeats=1)
                log.start()
                self.rc.sendUrl(Rpi.URL_RPI_KEY + "KEY_CHANNELUP")
                signal = datetime.datetime.now()

                while log.working:
                    time.sleep(0.1)

                if not log.found:
                    self.timeReportFile.write(str(datetime.datetime.now()).split(".")[0] + ";0\n")
                    self.timeReportFile.flush()
                else:
                    self.timeReportFile.write(str(datetime.datetime.now()).split(".")[0] + ";" + str((datetime.datetime.now() - signal).total_seconds()) + "\n")
                    self.timeReportFile.flush()

                dream = self.interval - 2.0 - (datetime.datetime.now() - signal).total_seconds()

                if dream > 0:
                    time.sleep(dream)

                self.logSave += 1

                if self.logSave >= self.foo:
                    writeStbLogsToFile(self.rc.getLogs(), generateStbLogFilePath(self.reportsPath, str(start)))
                    if Env.VIDEO:
                        screenshot(generateScreenFilePath(self.reportsPath, "screenshot"))
                    self.logger.info("zapping...")
                    self.logSave = 0
                else:
                    time.sleep(2)
            return False
        except Exception, e:
            self.logger.info("   ERR   " + str(e))
            return True

    def resetSTB(self):
        self.logger.warning("Hard Reset")
        self.rc.hardReset()
        time.sleep(2)
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
